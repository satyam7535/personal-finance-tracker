"""
Anomaly Detection for spending patterns.

Uses statistical analysis (mean + standard deviation) to identify
transactions that deviate significantly from the user's normal
spending in each category.

A transaction is flagged as anomalous if its amount exceeds
mean + 2 * std_dev for its category (Z-score > 2).
"""

import math
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict

from django.db.models import Avg, StdDev, Count, Q

from finance.models import Transaction
from finance.currency_utils import get_user_preferred_currency, convert_amount


def get_anomalies(user, sensitivity=2.0):
    """
    Detect spending anomalies across all expense categories.

    Args:
        user: The authenticated user.
        sensitivity: Number of standard deviations above the mean
                     to flag as anomalous (default: 2.0).

    Returns:
        dict with:
            - anomalies: list of flagged transactions with stats
            - category_stats: per-category mean/std/threshold
            - total_flagged: count of anomalous transactions
            - preferred_currency: user's preferred currency
    """
    preferred = get_user_preferred_currency(user)
    target_rate = preferred.exchange_rate_to_usd

    # Get all expense transactions for this user
    expenses = Transaction.objects.filter(
        user=user,
        type='EXPENSE',
        amount__gt=0,  # exclude refunds
    ).select_related('category', 'currency')

    if not expenses.exists():
        return {
            'anomalies': [],
            'category_stats': [],
            'total_flagged': 0,
            'preferred_currency': preferred,
        }

    # Convert all transactions to preferred currency for comparison
    tx_data = []
    for tx in expenses:
        converted = convert_amount(tx.amount, tx.currency, preferred)
        tx_data.append({
            'tx': tx,
            'converted_amount': converted,
            'category_name': tx.category.name,
            'category_id': tx.category_id,
        })

    # Group by category and compute stats
    category_groups = defaultdict(list)
    for item in tx_data:
        category_groups[item['category_id']].append(item)

    anomalies = []
    category_stats = []

    for cat_id, items in category_groups.items():
        amounts = [float(item['converted_amount']) for item in items]
        n = len(amounts)
        cat_name = items[0]['category_name']

        if n < 3:
            # Need at least 3 data points for meaningful statistics
            category_stats.append({
                'category': cat_name,
                'count': n,
                'mean': Decimal(str(sum(amounts) / n)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'std_dev': Decimal('0.00'),
                'threshold': None,
                'note': 'Insufficient data (need 3+ transactions)',
            })
            continue

        mean = sum(amounts) / n
        variance = sum((x - mean) ** 2 for x in amounts) / n
        std_dev = math.sqrt(variance)

        threshold = mean + sensitivity * std_dev

        mean_dec = Decimal(str(mean)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        std_dec = Decimal(str(std_dev)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        threshold_dec = Decimal(str(threshold)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        category_stats.append({
            'category': cat_name,
            'count': n,
            'mean': mean_dec,
            'std_dev': std_dec,
            'threshold': threshold_dec,
            'note': None,
        })

        # Flag transactions exceeding the threshold
        for item in items:
            amt = float(item['converted_amount'])
            if amt > threshold and std_dev > 0:
                z_score = (amt - mean) / std_dev
                anomalies.append({
                    'tx': item['tx'],
                    'converted_amount': item['converted_amount'],
                    'category': cat_name,
                    'z_score': round(z_score, 2),
                    'threshold': threshold_dec,
                    'mean': mean_dec,
                    'deviation_pct': round(((amt - mean) / mean) * 100, 1),
                })

    # Sort anomalies by z-score descending (most unusual first)
    anomalies.sort(key=lambda x: x['z_score'], reverse=True)

    return {
        'anomalies': anomalies,
        'category_stats': sorted(category_stats, key=lambda x: x['category']),
        'total_flagged': len(anomalies),
        'preferred_currency': preferred,
    }
