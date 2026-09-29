from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import ProtectedError
from django.http import FileResponse, Http404
import mimetypes

from .models import Transaction, Category, Budget, Notification
from .forms import TransactionForm, TransactionFilterForm, CategoryForm, BudgetForm
from .services import (
    create_transaction,
    update_transaction,
    delete_transaction,
    get_user_transactions,
)
from .currency_utils import get_user_preferred_currency, convert_amount


@login_required
def transaction_list(request):
    """List all transactions with optional filters."""
    filter_form = TransactionFilterForm(request.GET, user=request.user)

    filters = {}
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('type'):
            filters['type'] = filter_form.cleaned_data['type']
        if filter_form.cleaned_data.get('category'):
            filters['category_id'] = filter_form.cleaned_data['category'].id
        if filter_form.cleaned_data.get('date_from'):
            filters['date_from'] = filter_form.cleaned_data['date_from']
        if filter_form.cleaned_data.get('date_to'):
            filters['date_to'] = filter_form.cleaned_data['date_to']

    transactions = get_user_transactions(request.user, filters)

    # Preferred-currency conversion
    preferred = get_user_preferred_currency(request.user)
    enriched = []
    for tx in transactions:
        enriched.append({
            'tx': tx,
            'converted': convert_amount(tx.amount, tx.currency, preferred),
        })

    context = {
        'transactions': enriched,
        'filter_form': filter_form,
        'preferred_currency': preferred,
    }
    return render(request, 'finance/transaction_list.html', context)


@login_required
def transaction_create(request):
    """Create a new transaction."""
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                transaction = create_transaction(request.user, form.cleaned_data)
                messages.success(request, f'Transaction of {transaction.currency.symbol}{transaction.amount} added.')
                return redirect('finance:transaction_list')
            except ValidationError as e:
                for field, errs in e.message_dict.items():
                    for err in errs:
                        form.add_error(field if field != '__all__' else None, err)
    else:
        form = TransactionForm(user=request.user)

    return render(request, 'finance/transaction_form.html', {
        'form': form,
        'title': 'Add Transaction',
    })


@login_required
def transaction_edit(request, pk):
    """Edit an existing transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)

    if transaction.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction, user=request.user)
        if form.is_valid():
            try:
                update_transaction(request.user, pk, form.cleaned_data)
                messages.success(request, 'Transaction updated.')
                return redirect('finance:transaction_list')
            except ValidationError as e:
                for field, errs in e.message_dict.items():
                    for err in errs:
                        form.add_error(field if field != '__all__' else None, err)
    else:
        form = TransactionForm(instance=transaction, user=request.user)

    return render(request, 'finance/transaction_form.html', {
        'form': form,
        'title': 'Edit Transaction',
        'transaction': transaction,
    })


@login_required
def transaction_detail(request, pk):
    """View transaction details including receipt."""
    transaction = get_object_or_404(
        Transaction.objects.select_related('category', 'currency'),
        pk=pk,
    )
    if transaction.user_id != request.user.id:
        raise PermissionDenied

    preferred = get_user_preferred_currency(request.user)
    converted = convert_amount(transaction.amount, transaction.currency, preferred)
    is_image = False
    if transaction.receipt:
        is_image = transaction.receipt.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))

    return render(request, 'finance/transaction_detail.html', {
        'transaction': transaction,
        'converted': converted,
        'preferred_currency': preferred,
        'is_image': is_image,
    })


@login_required
def transaction_delete(request, pk):
    """Delete a transaction with confirmation."""
    transaction = get_object_or_404(Transaction, pk=pk)

    if transaction.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        delete_transaction(request.user, pk)
        messages.success(request, 'Transaction deleted.')
        return redirect('finance:transaction_list')

    return render(request, 'finance/transaction_confirm_delete.html', {
        'transaction': transaction,
    })


@login_required
def transaction_receipt_download(request, pk):
    """Securely serve transaction receipts only to the owner."""
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if transaction.user_id != request.user.id:
        raise PermissionDenied
        
    if not transaction.receipt:
        raise Http404("Receipt not found")
        
    content_type, _ = mimetypes.guess_type(transaction.receipt.name)
    return FileResponse(transaction.receipt.open(), content_type=content_type)


# ─── Category Views ──────────────────────────────────────────────────────────

@login_required
def category_list(request):
    """List all categories for the current user."""
    categories = Category.objects.filter(user=request.user).order_by('type', 'name')
    # Count transactions per category
    from django.db.models import Count
    categories = categories.annotate(transaction_count=Count('transactions'))
    return render(request, 'finance/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            try:
                category.full_clean()
                category.save()
                messages.success(request, f'Category "{category.name}" created.')
                return redirect('finance:category_list')
            except ValidationError as e:
                for field, errs in e.message_dict.items():
                    for err in errs:
                        form.add_error(field if field != '__all__' else None, err)
    else:
        form = CategoryForm()

    return render(request, 'finance/category_form.html', {
        'form': form,
        'title': 'Add Category',
    })


@login_required
def category_delete(request, pk):
    """Delete a category — blocked if it has transactions (PROTECT)."""
    category = get_object_or_404(Category, pk=pk)

    if category.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, f'Category "{category.name}" deleted.')
        except ProtectedError:
            tx_count = category.transactions.count()
            messages.error(
                request,
                f'Cannot delete "{category.name}" — it has {tx_count} transaction(s). '
                f'Delete or reassign those transactions first.'
            )
        return redirect('finance:category_list')

    return render(request, 'finance/category_confirm_delete.html', {
        'category': category,
    })


# ─── Budget Views ────────────────────────────────────────────────────────────

@login_required
def budget_list(request):
    """List all budgets for the current user with progress."""
    budgets = list(Budget.objects.filter(user=request.user).select_related('category', 'currency'))
    preferred = get_user_preferred_currency(request.user)

    # Pre-calculate expenses to avoid N+1 queries
    from django.db.models import Sum, F
    from django.db.models.functions import Coalesce, TruncMonth
    from decimal import Decimal, ROUND_HALF_UP
    
    expenses = Transaction.objects.filter(
        user=request.user, 
        type='EXPENSE',
        category__in={b.category_id for b in budgets} if budgets else []
    ).annotate(
        month_trunc=TruncMonth('date')
    ).values('category_id', 'month_trunc').annotate(
        total_usd=Sum(F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')))
    )
    expense_map = {(e['category_id'], e['month_trunc']): e['total_usd'] for e in expenses}

    # Enrich with computed properties for template
    budget_data = []
    target_rate = preferred.exchange_rate_to_usd or Decimal('1')
    
    for budget in budgets:
        spent_usd = expense_map.get((budget.category_id, budget.month), Decimal('0.00'))
        budget_cur = budget._budget_currency()
        budget_rate = budget_cur.exchange_rate_to_usd or Decimal('1')
        
        limit_usd = budget.limit_amount * budget_rate
        limit_display = (limit_usd / target_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        spent_display = (spent_usd / target_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        spent_in_budget_currency = (spent_usd / budget_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        percentage = (spent_in_budget_currency / budget.limit_amount * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) if budget.limit_amount > 0 else Decimal('0.0')
        is_overrun = spent_in_budget_currency > budget.limit_amount
        
        budget_data.append({
            'budget': budget,
            'spent': spent_display,
            'limit': limit_display,
            'percentage': percentage,
            'is_overrun': is_overrun,
            'remaining': limit_display - spent_display,
        })

    return render(request, 'finance/budget_list.html', {
        'budget_data': budget_data,
        'preferred_currency': preferred,
    })


@login_required
def budget_create(request):
    """Create a new monthly budget."""
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.full_clean()
                budget.save()
                messages.success(
                    request,
                    f'Budget of {budget.limit_amount} set for "{budget.category.name}" '
                    f'({budget.month.strftime("%b %Y")}).'
                )
                return redirect('finance:budget_list')
            except ValidationError as e:
                for field, errs in e.message_dict.items():
                    for err in errs:
                        form.add_error(field if field != '__all__' else None, err)
    else:
        form = BudgetForm(user=request.user)

    return render(request, 'finance/budget_form.html', {
        'form': form,
        'title': 'Set Budget',
    })


@login_required
def budget_edit(request, pk):
    """Edit an existing budget."""
    budget = get_object_or_404(Budget, pk=pk)

    if budget.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            try:
                budget.full_clean()
                budget.save()
                messages.success(request, 'Budget updated.')
                return redirect('finance:budget_list')
            except ValidationError as e:
                for field, errs in e.message_dict.items():
                    for err in errs:
                        form.add_error(field if field != '__all__' else None, err)
    else:
        form = BudgetForm(instance=budget, user=request.user)

    return render(request, 'finance/budget_form.html', {
        'form': form,
        'title': 'Edit Budget',
        'budget': budget,
    })


@login_required
def budget_delete(request, pk):
    """Delete a budget."""
    budget = get_object_or_404(Budget, pk=pk)

    if budget.user_id != request.user.id:
        raise PermissionDenied

    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted.')
        return redirect('finance:budget_list')

    return render(request, 'finance/budget_confirm_delete.html', {
        'budget': budget,
    })


# ─── Notification Views ──────────────────────────────────────────────────────

@login_required
def notification_list(request):
    """List all notifications for the current user."""
    notifications = Notification.objects.filter(user=request.user)

    # Mark all as read on page visit
    unread = notifications.filter(is_read=False)
    if unread.exists():
        unread.update(is_read=True)

    return render(request, 'finance/notification_list.html', {
        'notifications': notifications,
    })


@login_required
def notification_mark_read(request, pk):
    """Mark a single notification as read."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return redirect('finance:notification_list')


@login_required
def notification_clear_all(request):
    """Delete all read notifications."""
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=True).delete()
        messages.success(request, 'Cleared all read notifications.')
    return redirect('finance:notification_list')


@login_required
def import_statement(request):
    """Upload and import a bank statement CSV or PDF."""
    from .import_forms import BankStatementForm
    from .import_service import parse_csv_statement, parse_pdf_statement, import_transactions

    if request.method == 'POST':
        # Step 3: Confirm import
        if request.POST.get('confirm_import'):
            session_key = request.POST.get('session_key')
            parsed_data = request.session.get(session_key)
            if parsed_data:
                from .models import Currency
                currency = Currency.objects.get(pk=parsed_data['currency_id'])

                # Reconstruct row objects with category references
                from .models import Category
                rows = []
                for row in parsed_data['rows']:
                    cat = None
                    if row['category_id']:
                        try:
                            cat = Category.objects.get(pk=row['category_id'])
                        except Category.DoesNotExist:
                            pass
                    rows.append({
                        **row,
                        'category': cat,
                        'date': __import__('datetime').datetime.strptime(row['date'], '%Y-%m-%d').date(),
                        'amount': __import__('decimal').Decimal(row['amount']),
                    })

                result = import_transactions(request.user, rows, currency)
                del request.session[session_key]

                return render(request, 'finance/import_statement.html', {
                    'step': 'done',
                    'imported': result['imported'],
                    'skipped': result['skipped'],
                })

        # Step 2: Upload & parse
        form = BankStatementForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            currency_code = form.cleaned_data['currency'].code
            date_format = form.cleaned_data['date_format']

            # Route to CSV or PDF parser based on file extension
            if uploaded_file.name.lower().endswith('.pdf'):
                parsed = parse_pdf_statement(
                    uploaded_file,
                    request.user,
                    currency_code=currency_code,
                    date_format=date_format,
                )
            else:
                parsed = parse_csv_statement(
                    uploaded_file,
                    request.user,
                    currency_code=currency_code,
                    date_format=date_format,
                )

            # Store parsed data in session for confirmation
            import uuid
            session_key = f'import_{uuid.uuid4().hex[:8]}'
            session_data = {
                'currency_id': parsed['currency'].pk,
                'rows': [
                    {
                        'row_num': r['row_num'],
                        'date': r['date'].isoformat(),
                        'description': r['description'],
                        'amount': str(r['amount']),
                        'original_amount': str(r['original_amount']),
                        'type': r['type'],
                        'category_id': r['category'].pk if r['category'] else None,
                        'category_name': r['category_name'],
                        'is_duplicate': r['is_duplicate'],
                        'is_uncategorized': r.get('is_uncategorized', False),
                    }
                    for r in parsed['rows']
                ],
            }
            request.session[session_key] = session_data

            return render(request, 'finance/import_statement.html', {
                'step': 'preview',
                'rows': parsed['rows'],
                'total_rows': parsed['total_rows'],
                'new_count': parsed['new_count'],
                'duplicates': parsed['duplicates'],
                'errors': parsed['errors'],
                'currency': parsed['currency'],
                'session_key': session_key,
            })
    else:
        form = BankStatementForm()

    return render(request, 'finance/import_statement.html', {
        'step': 'upload',
        'form': form,
    })


@login_required
def download_sample_csv(request):
    """Serve a sample CSV file for bank statement import."""
    from django.http import HttpResponse

    content = (
        'date,description,amount\n'
        '2026-01-15,Grocery Store - Weekly Shopping,45.99\n'
        '2026-01-16,Salary Deposit,5000.00\n'
        '2026-01-17,Netflix Subscription,15.99\n'
        '2026-01-18,Uber Ride to Airport,28.50\n'
        '2026-01-19,Freelance Payment Received,1200.00\n'
        '2026-01-20,Amazon Shopping,89.99\n'
        '2026-01-21,Electric Bill Payment,120.00\n'
        '2026-01-22,Coffee Shop,4.50\n'
        '2026-01-23,Gym Membership,35.00\n'
        '2026-01-24,Restaurant Dinner,62.00\n'
    )
    response = HttpResponse(content, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_bank_statement.csv"'
    return response
