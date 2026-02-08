from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError

from .models import Transaction
from .forms import TransactionForm, TransactionFilterForm
from .services import (
    create_transaction,
    update_transaction,
    delete_transaction,
    get_user_transactions,
)


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

    context = {
        'transactions': transactions,
        'filter_form': filter_form,
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
