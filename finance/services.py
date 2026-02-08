"""
Service layer for financial transactions.
Views call these functions — never ORM directly.
This ensures business logic is centralized and testable.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Transaction, Category, Budget


def create_transaction(user, cleaned_data):
    """
    Create a new transaction for the given user.
    `cleaned_data` comes from the validated form.
    Returns the created Transaction instance.
    """
    transaction = Transaction(
        user=user,
        category=cleaned_data['category'],
        amount=cleaned_data['amount'],
        currency=cleaned_data['currency'],
        date=cleaned_data['date'],
        description=cleaned_data.get('description', ''),
        receipt=cleaned_data.get('receipt'),
    )
    # full_clean() is called inside save() — validates and auto-sets type
    transaction.save()

    # Check budget overrun after creating an expense
    if transaction.type == 'EXPENSE':
        _check_budget_overrun(user, transaction)

    return transaction


def update_transaction(user, transaction_id, cleaned_data):
    """
    Update an existing transaction.
    Enforces ownership — raises PermissionDenied if not owner.
    Returns the updated Transaction instance.
    """
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if transaction.user_id != user.id:
        raise PermissionDenied('You do not have permission to edit this transaction.')

    transaction.category = cleaned_data['category']
    transaction.amount = cleaned_data['amount']
    transaction.currency = cleaned_data['currency']
    transaction.date = cleaned_data['date']
    transaction.description = cleaned_data.get('description', '')

    # Handle receipt: keep existing if not provided
    new_receipt = cleaned_data.get('receipt')
    if new_receipt:
        transaction.receipt = new_receipt

    transaction.save()

    # Check budget overrun after updating an expense
    if transaction.type == 'EXPENSE':
        _check_budget_overrun(user, transaction)

    return transaction


def delete_transaction(user, transaction_id):
    """
    Delete a transaction.
    Enforces ownership — raises PermissionDenied if not owner.
    """
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if transaction.user_id != user.id:
        raise PermissionDenied('You do not have permission to delete this transaction.')

    transaction.delete()


def get_user_transactions(user, filters=None):
    """
    Retrieve transactions for a user with optional filters.
    `filters` is a dict with optional keys: type, category_id, date_from, date_to, currency_id
    """
    qs = Transaction.objects.filter(user=user).select_related('category', 'currency')

    if filters:
        if filters.get('type'):
            qs = qs.filter(type=filters['type'])
        if filters.get('category_id'):
            qs = qs.filter(category_id=filters['category_id'])
        if filters.get('date_from'):
            qs = qs.filter(date__gte=filters['date_from'])
        if filters.get('date_to'):
            qs = qs.filter(date__lte=filters['date_to'])
        if filters.get('currency_id'):
            qs = qs.filter(currency_id=filters['currency_id'])

    return qs


def _check_budget_overrun(user, transaction):
    """
    After an expense transaction, check if it causes a budget overrun.
    If so, flag the budget for notification (handled elsewhere).
    """
    budgets = Budget.objects.filter(
        user=user,
        category=transaction.category,
        month__year=transaction.date.year,
        month__month=transaction.date.month,
    )
    for budget in budgets:
        if budget.is_overrun:
            # Mark for notification — actual email sending in Phase 11
            budget.save(update_fields=['updated_at'])
