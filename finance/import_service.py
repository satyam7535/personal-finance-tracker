"""
Bank statement import service.

Supports CSV and PDF file upload with:
- Auto-categorization based on description keyword matching
- Duplicate detection (same date + amount + description)
- Multi-currency support
- Dry-run preview before committing
"""

import csv
import io
import re
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


def _get_or_create_fallback_category(user, tx_type):
    """
    Get or create a fallback 'Uncategorized' category so no rows are lost.
    """
    cat, _ = Category.objects.get_or_create(
        user=user,
        name='Uncategorized',
        type=tx_type,
        defaults={'description': 'Auto-created for imported transactions'},
    )
    return cat


def _find_or_suggest_category(user, description, tx_type):
    """
    Try to find a matching user category based on description.
    Falls back to an auto-created 'Uncategorized' category (never returns None).
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

    # Try the first category of the matching type
    default_cat = user_categories.first()
    if default_cat:
        return default_cat, False

    # Auto-create a fallback 'Uncategorized' category
    fallback = _get_or_create_fallback_category(user, tx_type)
    return fallback, True


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
    Import parsed rows as Transaction objects.

    Sets the transaction type (INCOME/EXPENSE/INVESTMENT) and triggers
    budget overrun checks for expenses.

    Args:
        user: authenticated user
        parsed_rows: list of row dicts from parse_csv_statement or parse_pdf_statement
        currency: Currency object
        skip_duplicates: whether to skip duplicate transactions

    Returns:
        dict with imported count and skipped count
    """
    from .services import _check_budget_overrun

    imported = 0
    skipped = 0

    for row in parsed_rows:
        if skip_duplicates and row.get('is_duplicate'):
            skipped += 1
            continue

        if row.get('category') is None:
            skipped += 1
            continue

        tx = Transaction(
            user=user,
            type=row.get('type', 'EXPENSE'),
            category=row['category'],
            amount=row['amount'],
            currency=currency,
            date=row['date'],
            description=row['description'],
        )
        tx.save()
        imported += 1

        # Trigger budget overrun check for expenses
        if tx.type == 'EXPENSE':
            try:
                _check_budget_overrun(user, tx)
            except Exception:
                pass  # Budget check failure should never block import

    return {
        'imported': imported,
        'skipped': skipped,
    }


def parse_pdf_statement(file, user, currency_code='INR', date_format='%Y-%m-%d'):
    """
    Parse a PDF bank statement using pdfplumber table extraction.

    Looks for tables with date, description, and amount/debit/credit columns.
    Falls back to line-by-line text extraction if no tables are found.

    Args:
        file: uploaded PDF file
        user: authenticated user
        currency_code: default currency code
        date_format: preferred date format

    Returns:
        Same dict structure as parse_csv_statement.
    """
    import pdfplumber

    try:
        currency = Currency.objects.get(code=currency_code, is_active=True)
    except Currency.DoesNotExist:
        currency = Currency.objects.filter(is_active=True).first()

    rows = []
    errors = []
    duplicates = 0
    new_count = 0

    date_formats = [date_format, '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y',
                    '%d-%m-%Y', '%m-%d-%Y', '%Y/%m/%d', '%d %b %Y',
                    '%b %d, %Y', '%d %B %Y']

    # Amount pattern: optional minus, digits with optional commas, decimal
    amount_re = re.compile(r'^-?[\d,]+\.?\d*$')
    # Date pattern: anything that looks like a date
    date_re = re.compile(r'\d{1,4}[/\-\s]\w{1,9}[/\-\s]\d{1,4}')

    try:
        pdf = pdfplumber.open(file)
    except Exception as e:
        return {
            'rows': [],
            'total_rows': 0,
            'duplicates': 0,
            'new_count': 0,
            'errors': [f'Could not read PDF: {str(e)}'],
            'currency': currency,
        }

    row_num = 1

    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()

        if tables:
            for table in tables:
                if not table or len(table) < 2:
                    continue

                # Use first row as headers
                headers = [str(h).strip().lower().replace(' ', '_') if h else '' for h in table[0]]

                # Find column indices
                date_col = None
                desc_col = None
                amount_col = None
                debit_col = None
                credit_col = None

                for idx, h in enumerate(headers):
                    if h in ('date', 'transaction_date', 'value_date', 'txn_date'):
                        date_col = idx
                    elif h in ('description', 'narration', 'details', 'particulars', 'memo'):
                        desc_col = idx
                    elif h in ('amount', 'transaction_amount'):
                        amount_col = idx
                    elif h in ('debit', 'withdrawal', 'dr'):
                        debit_col = idx
                    elif h in ('credit', 'deposit', 'cr'):
                        credit_col = idx

                if date_col is None:
                    continue

                for table_row in table[1:]:
                    row_num += 1
                    if not table_row or len(table_row) <= max(filter(lambda x: x is not None, [date_col, desc_col, amount_col, debit_col, credit_col])):
                        continue

                    result = _process_pdf_row(
                        table_row, date_col, desc_col, amount_col,
                        debit_col, credit_col, date_formats, row_num,
                        user, errors
                    )
                    if result:
                        is_dup = _detect_duplicate(user, result['date'], result['amount'], result['description'])
                        if is_dup:
                            duplicates += 1
                        else:
                            new_count += 1
                        rows.append({**result, 'is_duplicate': is_dup, 'row_num': row_num})

        else:
            # Fallback: extract text lines
            text = page.extract_text()
            if not text:
                continue
            for line in text.split('\n'):
                line = line.strip()
                if not line or not date_re.search(line):
                    continue

                row_num += 1
                result = _process_text_line(line, date_formats, amount_re, row_num, user, errors)
                if result:
                    is_dup = _detect_duplicate(user, result['date'], result['amount'], result['description'])
                    if is_dup:
                        duplicates += 1
                    else:
                        new_count += 1
                    rows.append({**result, 'is_duplicate': is_dup, 'row_num': row_num})

    pdf.close()

    return {
        'rows': rows,
        'total_rows': len(rows),
        'duplicates': duplicates,
        'new_count': new_count,
        'errors': errors,
        'currency': currency,
    }


def _process_pdf_row(table_row, date_col, desc_col, amount_col,
                     debit_col, credit_col, date_formats, row_num,
                     user, errors):
    """Process a single row from a PDF table."""
    # Parse date
    date_val = str(table_row[date_col] or '').strip()
    tx_date = None
    for fmt in date_formats:
        try:
            tx_date = datetime.strptime(date_val, fmt).date()
            break
        except (ValueError, TypeError):
            continue
    if not tx_date:
        errors.append(f'Row {row_num}: Could not parse date "{date_val}"')
        return None

    # Parse description
    description = ''
    if desc_col is not None and desc_col < len(table_row):
        description = str(table_row[desc_col] or '').strip()

    # Parse amount
    amount = None
    try:
        if debit_col is not None and credit_col is not None:
            debit = str(table_row[debit_col] or '').strip().replace(',', '')
            credit = str(table_row[credit_col] or '').strip().replace(',', '')
            if debit and debit not in ('0', '0.00', '-', ''):
                amount = -abs(Decimal(debit))
            elif credit and credit not in ('0', '0.00', '-', ''):
                amount = abs(Decimal(credit))
        elif amount_col is not None:
            amt_str = str(table_row[amount_col] or '').strip().replace(',', '')
            if amt_str and amt_str not in ('-', ''):
                amount = Decimal(amt_str)
    except (InvalidOperation, ValueError):
        errors.append(f'Row {row_num}: Could not parse amount')
        return None

    if amount is None or amount == 0:
        return None

    amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    tx_type = _guess_category_type(description) if amount > 0 else 'EXPENSE'
    category, is_uncategorized = _find_or_suggest_category(user, description, tx_type)

    return {
        'date': tx_date,
        'description': description,
        'amount': abs(amount),
        'original_amount': amount,
        'type': tx_type,
        'category': category,
        'category_name': category.name if category else 'Uncategorized',
        'is_uncategorized': is_uncategorized,
    }


def _process_text_line(line, date_formats, amount_re, row_num, user, errors):
    """Process a single text line from PDF (fallback when no tables found)."""
    parts = re.split(r'\s{2,}', line)  # split on 2+ spaces
    if len(parts) < 2:
        return None

    # Try first part as date
    tx_date = None
    for fmt in date_formats:
        try:
            tx_date = datetime.strptime(parts[0].strip(), fmt).date()
            break
        except (ValueError, TypeError):
            continue
    if not tx_date:
        return None

    # Last part should be amount
    amt_str = parts[-1].strip().replace(',', '')
    amount = None
    try:
        if amount_re.match(amt_str):
            amount = Decimal(amt_str)
    except (InvalidOperation, ValueError):
        return None
    if amount is None or amount == 0:
        return None

    amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Middle parts are description
    description = ' '.join(parts[1:-1]).strip()

    tx_type = _guess_category_type(description) if amount > 0 else 'EXPENSE'
    category, is_uncategorized = _find_or_suggest_category(user, description, tx_type)

    return {
        'date': tx_date,
        'description': description,
        'amount': abs(amount),
        'original_amount': amount,
        'type': tx_type,
        'category': category,
        'category_name': category.name if category else 'Uncategorized',
        'is_uncategorized': is_uncategorized,
    }
