"""
Multi-Signal Anomaly & Fraud Detection for spending patterns.

Employs multiple detection methods for robust anomaly identification:

1. Z-Score Analysis  — flags transactions > 2σ above category mean
2. IQR (Interquartile Range) — robust outlier detection for skewed data
3. Frequency Spike  — detects unusual bursts of transactions per day
4. Round Number Flag — suspicious round-amount transactions (fraud indicator)
5. Velocity Check   — multiple transactions to same category within short period

Each transaction receives a composite risk score (0-100) based on
how many signals it triggers.
"""

import math
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict, Counter

from finance.models import Transaction
from finance.currency_utils import get_user_preferred_currency, convert_amount


def _zscore_flag(amount, mean, std_dev, threshold=2.0):
    """Z-score based detection: amount > mean + threshold * σ."""
    if std_dev == 0:
        return None
    z = (amount - mean) / std_dev
    if z > threshold:
        return round(z, 2)
    return None


def _iqr_flag(amount, amounts_sorted):
    """IQR-based robust outlier detection (resistant to skewed distributions)."""
    n = len(amounts_sorted)
    if n < 4:
        return False
    q1 = amounts_sorted[n // 4]
    q3 = amounts_sorted[(3 * n) // 4]
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    return amount > upper_fence


def _round_number_flag(amount):
    """Flag suspiciously round amounts (common in fraud)."""
    amt = float(amount)
    if amt >= 1000 and amt % 1000 == 0:
        return 'exact_thousand'
    if amt >= 500 and amt % 500 == 0:
        return 'exact_500'
    if amt >= 100 and amt % 100 == 0:
        return 'exact_hundred'
    return None


def _frequency_spike(tx_date, date_counts, avg_daily):
    """Flag if the transaction day has unusually many transactions."""
    day_count = date_counts.get(tx_date, 0)
    if avg_daily > 0 and day_count >= max(3, avg_daily * 3):
        return day_count
    return None


def _velocity_flag(tx, same_cat_txs):
    """Flag if multiple transactions in same category within 24 hours."""
    count = 0
    for other in same_cat_txs:
        if other['tx'].pk == tx.pk:
            continue
        if other['tx'].date == tx.date:
            count += 1
    return count if count >= 2 else None


def _compute_risk_score(signals):
    """
    Compute composite risk score (0-100) from triggered signals.
    Each signal contributes a weighted score.
    """
    score = 0
    weights = {
        'zscore': 35,       # strongest statistical signal
        'iqr': 25,          # robust outlier confirmation
        'round_number': 15, # mild fraud indicator
        'frequency': 15,    # unusual activity pattern
        'velocity': 10,     # same-category clustering
    }
    for signal, weight in weights.items():
        if signals.get(signal):
            score += weight
    return min(score, 100)


def get_anomalies(user, sensitivity=2.0):
    """
    Multi-signal anomaly detection across all expense categories.

    Detection Methods:
        1. Z-Score (>2σ) — statistical outlier
        2. IQR fence — robust for non-normal distributions
        3. Round numbers — fraud pattern indicator
        4. Frequency spike — unusual daily transaction volume
        5. Velocity — same-category clustering

    Returns:
        dict with anomalies, category_stats, detection_summary,
        total_flagged, and preferred_currency.
    """
    preferred = get_user_preferred_currency(user)

    expenses = Transaction.objects.filter(
        user=user,
        type='EXPENSE',
        amount__gt=0,
    ).select_related('category', 'currency').order_by('date')

    if not expenses.exists():
        return {
            'anomalies': [],
            'category_stats': [],
            'total_flagged': 0,
            'preferred_currency': preferred,
            'detection_summary': {
                'zscore': 0, 'iqr': 0, 'round_number': 0,
                'frequency': 0, 'velocity': 0,
            },
        }

    # Convert all transactions to preferred currency
    tx_data = []
    date_counter = Counter()
    for tx in expenses:
        converted = convert_amount(tx.amount, tx.currency, preferred)
        tx_data.append({
            'tx': tx,
            'converted_amount': converted,
            'category_name': tx.category.name,
            'category_id': tx.category_id,
        })
        date_counter[tx.date] += 1

    # Average daily transaction count
    if date_counter:
        avg_daily = sum(date_counter.values()) / len(date_counter)
    else:
        avg_daily = 0

    # Group by category
    category_groups = defaultdict(list)
    for item in tx_data:
        category_groups[item['category_id']].append(item)

    anomalies = []
    category_stats = []
    detection_counts = {
        'zscore': 0, 'iqr': 0, 'round_number': 0,
        'frequency': 0, 'velocity': 0,
    }

    for cat_id, items in category_groups.items():
        amounts = [float(item['converted_amount']) for item in items]
        amounts_sorted = sorted(amounts)
        n = len(amounts)
        cat_name = items[0]['category_name']

        mean = sum(amounts) / n
        mean_dec = Decimal(str(mean)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if n < 3:
            category_stats.append({
                'category': cat_name,
                'count': n,
                'mean': mean_dec,
                'std_dev': Decimal('0.00'),
                'threshold_zscore': None,
                'threshold_iqr': None,
                'note': 'Insufficient data (need 3+ transactions)',
            })
            continue

        variance = sum((x - mean) ** 2 for x in amounts) / n
        std_dev = math.sqrt(variance)
        threshold_z = mean + sensitivity * std_dev

        # IQR bounds
        q1 = amounts_sorted[n // 4]
        q3 = amounts_sorted[(3 * n) // 4]
        iqr = q3 - q1
        threshold_iqr = q3 + 1.5 * iqr

        std_dec = Decimal(str(std_dev)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        tz_dec = Decimal(str(threshold_z)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        ti_dec = Decimal(str(threshold_iqr)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        category_stats.append({
            'category': cat_name,
            'count': n,
            'mean': mean_dec,
            'std_dev': std_dec,
            'threshold_zscore': tz_dec,
            'threshold_iqr': ti_dec,
            'note': None,
        })

        # Analyze each transaction against all signals
        for item in items:
            amt = float(item['converted_amount'])
            tx = item['tx']
            signals = {}

            # Signal 1: Z-Score
            z = _zscore_flag(amt, mean, std_dev, sensitivity)
            if z:
                signals['zscore'] = z
                detection_counts['zscore'] += 1

            # Signal 2: IQR outlier
            if _iqr_flag(amt, amounts_sorted):
                signals['iqr'] = True
                detection_counts['iqr'] += 1

            # Signal 3: Round number
            rnd = _round_number_flag(item['converted_amount'])
            if rnd:
                signals['round_number'] = rnd
                detection_counts['round_number'] += 1

            # Signal 4: Frequency spike
            freq = _frequency_spike(tx.date, date_counter, avg_daily)
            if freq:
                signals['frequency'] = freq
                detection_counts['frequency'] += 1

            # Signal 5: Velocity (same-category same-day)
            vel = _velocity_flag(tx, items)
            if vel:
                signals['velocity'] = vel
                detection_counts['velocity'] += 1

            # Only flag if at least one signal triggered
            if signals:
                risk_score = _compute_risk_score(signals)
                anomalies.append({
                    'tx': tx,
                    'converted_amount': item['converted_amount'],
                    'category': cat_name,
                    'signals': signals,
                    'risk_score': risk_score,
                    'signal_count': len(signals),
                    'z_score': signals.get('zscore', 0),
                    'threshold': tz_dec,
                    'mean': mean_dec,
                    'deviation_pct': round(((amt - mean) / mean) * 100, 1) if mean > 0 else 0,
                })

    # Sort by risk score descending
    anomalies.sort(key=lambda x: x['risk_score'], reverse=True)

    return {
        'anomalies': anomalies,
        'category_stats': sorted(category_stats, key=lambda x: x['category']),
        'total_flagged': len(anomalies),
        'preferred_currency': preferred,
        'detection_summary': detection_counts,
    }
