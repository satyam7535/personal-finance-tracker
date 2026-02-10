"""
Bank statement import service.

Supports CSV file upload with:
- Auto-categorization based on description keyword matching
- Duplicate detection (same date + amount + description)
- Multi-currency support
- Dry-run preview before committing
"""

import csv
import io
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, date

from django.db.models import Q

from finance.models import Transaction, Category, Currency


# Common keywords → category type mapping for auto-categorization
CATEGORY_KEYWORDS = {
    'EXPENSE': [
        'grocery', 'groceries', 'supermarket', 'walmart', 'target',
        'restaurant', 'food', 'dining', 'cafe', 'coffee', 'starbucks',
        'gas', 'fuel', 'petrol', 'uber', 'lyft', 'taxi', 'transport',
        'rent', 'mortgage', 'utilities', 'electric', 'water', 'internet',
        'insurance', 'medical', 'pharmacy', 'doctor', 'hospital',
        'shopping', 'amazon', 'ebay', 'store', 'mall',
        'subscription', 'netflix', 'spotify', 'gym', 'membership',
        'phone', 'mobile', 'telecom',
    ],
    'INCOME': [
        'salary', 'payroll', 'wage', 'deposit', 'transfer in',
        'interest', 'dividend', 'refund', 'reimbursement', 'bonus',
        'freelance', 'payment received', 'credit',
    ],
    'INVESTMENT': [
        'investment', 'stock', 'mutual fund', 'etf', 'trading',
        'crypto', 'bitcoin', 'portfolio', 'brokerage',
    ],
}


def _guess_category_type(description):
    """Guess transaction type from description keywords."""
    desc_lower = description.lower()
    for tx_type, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return tx_type
    return 'EXPENSE'  # default to expense


def _find_or_suggest_category(user, description, tx_type):
    """
    Try to find a matching user category based on description.
    Returns (category, is_new_suggestion).
    """
    desc_lower = description.lower()

    # First, try exact match with user's existing categories
    user_categories = Category.objects.filter(user=user, type=tx_type)
    for cat in user_categories:
        if cat.name.lower() in desc_lower or desc_lower in cat.name.lower():
            return cat, False

    # Check keywords in description against category names
    for cat in user_categories:
        cat_words = cat.name.lower().split()
        for word in cat_words:
            if len(word) > 3 and word in desc_lower:
                return cat, False

    # Return the first category of the matching type, or None
    default_cat = user_categories.first()
    return default_cat, default_cat is None


def _detect_duplicate(user, tx_date, amount, description):
    """
    Check if a similar transaction already exists.
    Matches on date + amount + description (fuzzy).
    """
    return Transaction.objects.filter(
        user=user,
        date=tx_date,
        amount=amount,
        description__iexact=description.strip(),
    ).exists()


def parse_csv_statement(file, user, currency_code='INR', date_format='%Y-%m-%d'):
    """
    Parse a CSV bank statement and return preview data.

    Expected CSV columns (flexible naming):
        date, description, amount
    OR:
        date, description, debit, credit

    Args:
        file: uploaded CSV file
        user: authenticated user
        currency_code: default currency code for imports
        date_format: date format string for parsing

    Returns:
        dict with:
            - rows: list of parsed transactions with status
            - total_rows: total count
            - duplicates: count of detected duplicates
            - new_count: count of new transactions to import
            - errors: list of row-level errors
            - currency: Currency object
    """
    try:
        currency = Currency.objects.get(code=currency_code, is_active=True)
    except Currency.DoesNotExist:
        currency = Currency.objects.filter(is_active=True).first()

    # Read CSV content
    try:
        content = file.read().decode('utf-8-sig')  # handle BOM
    except UnicodeDecodeError:
        file.seek(0)
        content = file.read().decode('latin-1')

    reader = csv.DictReader(io.StringIO(content))

    # Normalize header names
    if reader.fieldnames:
        reader.fieldnames = [f.strip().lower().replace(' ', '_') for f in reader.fieldnames]

    rows = []
    errors = []
    duplicates = 0
    new_count = 0

    # Common date formats to try
    date_formats = [date_format, '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y',
                    '%d-%m-%Y', '%m-%d-%Y', '%Y/%m/%d', '%d %b %Y',
                    '%b %d, %Y', '%d %B %Y']

    for i, raw_row in enumerate(reader, start=2):  # start at 2 (header is row 1)
        # Find date column
        tx_date = None
        date_val = raw_row.get('date') or raw_row.get('transaction_date') or raw_row.get('value_date')
        if date_val:
            date_val = date_val.strip()
            for fmt in date_formats:
                try:
                    tx_date = datetime.strptime(date_val, fmt).date()
                    break
                except ValueError:
                    continue

        if not tx_date:
            errors.append(f'Row {i}: Could not parse date "{date_val}"')
            continue

        # Find description
        description = (
            raw_row.get('description') or raw_row.get('narration') or
            raw_row.get('details') or raw_row.get('particulars') or
            raw_row.get('memo') or ''
        ).strip()

        # Find amount (handle debit/credit columns or single amount)
        amount = None
        try:
            if 'debit' in raw_row and 'credit' in raw_row:
                debit = raw_row.get('debit', '').strip().replace(',', '')
                credit = raw_row.get('credit', '').strip().replace(',', '')
                if debit and debit != '0' and debit != '0.00':
                    amount = -abs(Decimal(debit))  # negative for expenses
                elif credit and credit != '0' and credit != '0.00':
                    amount = abs(Decimal(credit))
            else:
                amt_str = (
                    raw_row.get('amount') or raw_row.get('transaction_amount') or '0'
                ).strip().replace(',', '')
                amount = Decimal(amt_str)
        except (InvalidOperation, ValueError):
            errors.append(f'Row {i}: Could not parse amount')
            continue

        if amount is None or amount == 0:
            errors.append(f'Row {i}: Amount is zero or missing')
            continue

        # Quantize
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Determine type and category
        if amount > 0:
            tx_type = _guess_category_type(description)
        else:
            tx_type = 'EXPENSE'

        category, is_uncategorized = _find_or_suggest_category(user, description, tx_type)

        # Check for duplicates
        is_duplicate = _detect_duplicate(user, tx_date, abs(amount), description)
        if is_duplicate:
            duplicates += 1

        if not is_duplicate:
            new_count += 1

        rows.append({
            'row_num': i,
            'date': tx_date,
            'description': description,
            'amount': abs(amount),
            'original_amount': amount,
            'type': tx_type,
            'category': category,
            'category_name': category.name if category else 'Uncategorized',
            'is_duplicate': is_duplicate,
            'is_uncategorized': is_uncategorized,
        })

    return {
        'rows': rows,
        'total_rows': len(rows),
        'duplicates': duplicates,
        'new_count': new_count,
        'errors': errors,
        'currency': currency,
    }


def import_transactions(user, parsed_rows, currency, skip_duplicates=True):
    """
    Import parsed CSV rows as Transaction objects.

    Args:
        user: authenticated user
        parsed_rows: list of row dicts from parse_csv_statement
        currency: Currency object
        skip_duplicates: whether to skip duplicate transactions

    Returns:
        dict with imported count and skipped count
    """
    imported = 0
    skipped = 0

    for row in parsed_rows:
        if skip_duplicates and row['is_duplicate']:
            skipped += 1
            continue

        if row['category'] is None:
            skipped += 1
            continue

        tx = Transaction(
            user=user,
            category=row['category'],
            amount=row['amount'],
            currency=currency,
            date=row['date'],
            description=row['description'],
        )
        tx.save()
        imported += 1

    return {
        'imported': imported,
        'skipped': skipped,
    }
