"""
Multi-currency conversion utilities.

All conversions go through USD as the intermediary:
    source → USD → target

Usage:
    from finance.currency_utils import convert_amount, get_user_preferred_currency

    target = get_user_preferred_currency(user)
    converted = convert_amount(Decimal('100.00'), from_currency, target)
"""

from decimal import Decimal, ROUND_HALF_UP

from .models import Currency


def convert_amount(amount, from_currency, to_currency):
    """
    Convert an amount between two currencies using USD as intermediary.

    Args:
        amount: Decimal amount in from_currency
        from_currency: Currency instance (source)
        to_currency: Currency instance (target)

    Returns:
        Decimal amount in to_currency, rounded to 2 decimal places.
    """
    if amount is None:
        return Decimal('0.00')

    amount = Decimal(str(amount))

    # Same currency — no conversion needed
    if from_currency.pk == to_currency.pk:
        return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Step 1: Convert to USD
    amount_in_usd = amount * from_currency.exchange_rate_to_usd

    # Step 2: Convert from USD to target
    if to_currency.exchange_rate_to_usd <= 0:
        return Decimal('0.00')

    converted = amount_in_usd / to_currency.exchange_rate_to_usd
    return converted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def convert_to_usd(amount, from_currency):
    """Shorthand: convert any amount to USD."""
    if amount is None:
        return Decimal('0.00')
    amount = Decimal(str(amount))
    result = amount * from_currency.exchange_rate_to_usd
    return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def get_currency(code):
    """
    Get an active Currency instance by ISO 4217 code.
    Returns None if not found or inactive.
    """
    try:
        return Currency.objects.get(code=code.upper(), is_active=True)
    except Currency.DoesNotExist:
        return None


def get_user_preferred_currency(user):
    """
    Resolve the user's preferred currency to a Currency model instance.
    Falls back to USD if the preference is invalid.
    """
    preferred_code = getattr(user, 'profile', None)
    if preferred_code:
        preferred_code = user.profile.preferred_currency
    else:
        preferred_code = 'USD'

    currency = get_currency(preferred_code)
    if currency is None:
        currency = Currency.objects.filter(code='USD').first()
    return currency


def convert_queryset_to_currency(transactions, target_currency):
    """
    Take an iterable of Transaction objects and annotate each with
    `converted_amount` in the target currency.

    Returns a list of dicts: [{transaction, converted_amount, target_symbol}, ...]
    """
    results = []
    for txn in transactions:
        results.append({
            'transaction': txn,
            'converted_amount': convert_amount(txn.amount, txn.currency, target_currency),
            'target_symbol': target_currency.symbol,
            'target_code': target_currency.code,
        })
    return results
