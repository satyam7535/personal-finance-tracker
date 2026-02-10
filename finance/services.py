"""
Service layer for financial transactions.
Views call these functions — never ORM directly.
This ensures business logic is centralized and testable.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Transaction, Category, Budget, Notification


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
    After an expense transaction, check if it causes a budget overrun
    or nears the limit (80%+). Creates in-app notifications and sends
    email alerts via Resend SDK (one per breach, tracked via last_notified_at).
    """
    from django.utils import timezone
    from django.conf import settings
    import resend
    import logging

    logger = logging.getLogger(__name__)
    resend.api_key = settings.RESEND_API_KEY

    budgets = Budget.objects.filter(
        user=user,
        category=transaction.category,
        month__year=transaction.date.year,
        month__month=transaction.date.month,
    )
    for budget in budgets:
        pct = budget.percentage_used

        if budget.is_overrun:
            ntype = 'BUDGET_OVERRUN'
            msg = (
                f'Budget overrun! You have spent {budget.currency_symbol}'
                f'{budget.spent} of your {budget.currency_symbol}'
                f'{budget.limit_amount} budget for "{budget.category.name}" '
                f'in {budget.month.strftime("%B %Y")} ({pct}% used).'
            )
        elif pct >= 80:
            ntype = 'BUDGET_WARNING'
            msg = (
                f'Budget warning: You have used {pct}% of your '
                f'"{budget.category.name}" budget for '
                f'{budget.month.strftime("%B %Y")}.'
            )
        else:
            continue

        # Avoid duplicate notifications for the same budget+type
        # But allow escalation: if a WARNING exists and now it's OVERRUN, create it
        existing = Notification.objects.filter(
            user=user,
            budget=budget,
            notification_type=ntype,
        ).exists()
        if existing:
            # Update the latest notification message with fresh numbers
            Notification.objects.filter(
                user=user,
                budget=budget,
                notification_type=ntype,
            ).order_by('-created_at').update(message=msg, is_read=False)
            continue

        # Create in-app notification
        Notification.objects.create(
            user=user,
            budget=budget,
            message=msg,
            notification_type=ntype,
        )

        # Send email alert via Resend SDK
        if user.email and settings.RESEND_API_KEY:
            try:
                resend.Emails.send({
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": [user.email],
                    "subject": f'[Finance Tracker] {budget.category.name} — {ntype.replace("_", " ").title()}',
                    "html": f'<p>{msg}</p>',
                })
            except Exception as e:
                logger.warning(f'Email to {user.email} failed: {e}')

            budget.last_notified_at = timezone.now()
            budget.save(update_fields=['last_notified_at'])
