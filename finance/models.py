from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Currency(models.Model):
    """
    Supported currencies with exchange rates relative to USD.
    Exchange rates are stored as multipliers: amount_in_usd = amount / rate.
    """
    code = models.CharField(max_length=3, unique=True, help_text='ISO 4217 code')
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate_to_usd = models.DecimalField(
        max_digits=12, decimal_places=6, default=Decimal('1.000000'),
        help_text='1 unit of this currency = X USD'
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Currencies'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Category(models.Model):
    """
    User-defined categories for income, expense, or investment transactions.
    Each category belongs to exactly one user.
    """
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('INVESTMENT', 'Investment'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['type', 'name']
        unique_together = ['user', 'name', 'type']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValidationError({'name': 'Category name cannot be blank.'})


class Transaction(models.Model):
    """
    Single source of truth for all financial transactions.
    - Positive amount = normal income/expense/investment
    - Negative amount on EXPENSE = refund
    - Amount stored with 2 decimal precision

    NOTE: `type` is intentionally denormalized from Category.type for
    reporting/aggregation performance. It is auto-set from category.type
    and marked non-editable to prevent inconsistency.
    """
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('INVESTMENT', 'Investment'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name='transactions',
        help_text='Cannot delete a category that has transactions.'
    )
    # Denormalized from category.type for query performance — auto-set, not user-editable
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, editable=False)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Positive for normal, negative for refunds (expense only).'
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT,
        related_name='transactions',
        help_text='Currency of this transaction.'
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, default='')
    receipt = models.FileField(
        upload_to='receipts/%Y/%m/', blank=True, null=True,
        help_text='Upload receipt image or PDF.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'type']),
        ]

    def __str__(self):
        return f"{self.get_type_display()}: {self.currency.symbol}{self.amount} on {self.date}"

    def clean(self):
        super().clean()
        errors = {}

        # Auto-set type from category (single source of truth)
        if self.category_id:
            try:
                cat = Category.objects.get(pk=self.category_id)
                self.type = cat.type
                # Ensure category belongs to the same user
                if cat.user_id != self.user_id:
                    errors['category'] = 'You cannot use another user\'s category.'
            except Category.DoesNotExist:
                errors['category'] = 'Selected category does not exist.'

        # Quantize amount to 2 decimal places
        if self.amount is not None:
            self.amount = Decimal(str(self.amount)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

        # Negative amounts only allowed for expense (refund)
        if self.amount is not None and self.amount < 0 and self.type != 'EXPENSE':
            errors['amount'] = 'Negative amounts are only allowed for expense refunds.'

        # Zero amount not allowed
        if self.amount is not None and self.amount == 0:
            errors['amount'] = 'Amount cannot be zero.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-set type from category and validate before every save
        if self.category_id:
            self.type = self.category.type
        if self.amount is not None:
            self.amount = Decimal(str(self.amount)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def amount_in_usd(self):
        """Convert amount to USD using stored exchange rate."""
        if self.currency and self.currency.exchange_rate_to_usd:
            return (self.amount * self.currency.exchange_rate_to_usd).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        return self.amount


class Budget(models.Model):
    """
    Monthly budget limit for a specific expense category.
    Only one budget per user + category + month.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='budgets',
        help_text='Only expense categories can have budgets.'
    )
    limit_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text='Maximum spending limit for this category in a month.'
    )
    month = models.DateField(
        help_text='First day of the budget month (e.g., 2026-02-01).'
    )
    last_notified_at = models.DateTimeField(
        null=True, blank=True,
        help_text='When the user was last notified about overrun.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category', 'month']
        ordering = ['-month', 'category__name']

    def __str__(self):
        return f"Budget: {self.category.name} - {self.month.strftime('%b %Y')}"

    def clean(self):
        super().clean()
        errors = {}

        # Budget only for expense categories
        if self.category_id:
            try:
                cat = Category.objects.get(pk=self.category_id)
                if cat.type != 'EXPENSE':
                    errors['category'] = 'Budgets can only be set for expense categories.'
                if cat.user_id != self.user_id:
                    errors['category'] = 'You cannot set a budget for another user\'s category.'
            except Category.DoesNotExist:
                errors['category'] = 'Selected category does not exist.'

        # Limit must be positive
        if self.limit_amount is not None and self.limit_amount <= 0:
            errors['limit_amount'] = 'Budget limit must be a positive amount.'

        # Quantize
        if self.limit_amount is not None:
            self.limit_amount = Decimal(str(self.limit_amount)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

        # Month must be first of month
        if self.month and self.month.day != 1:
            self.month = self.month.replace(day=1)

        if errors:
            raise ValidationError(errors)

    @property
    def spent(self):
        """
        Total spent in this category for this budget's month,
        normalised to the user's preferred currency via USD.

        Each transaction's amount is multiplied by its own
        currency.exchange_rate_to_usd, then divided by the
        target (preferred) currency's rate — giving a correct
        cross-currency total.
        """
        from django.db.models import Sum, F
        from finance.currency_utils import get_user_preferred_currency

        target = get_user_preferred_currency(self.user)
        target_rate = target.exchange_rate_to_usd or Decimal('1')

        # Sum(amount * from_rate) gives total in USD
        total_usd = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='EXPENSE',
            date__year=self.month.year,
            date__month=self.month.month,
        ).aggregate(
            total=Sum(F('amount') * F('currency__exchange_rate_to_usd'))
        )['total'] or Decimal('0.00')

        # Convert USD total to preferred currency
        return (total_usd / target_rate).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    @property
    def percentage_used(self):
        """Percentage of budget used."""
        if self.limit_amount and self.limit_amount > 0:
            return ((self.spent / self.limit_amount) * 100).quantize(
                Decimal('0.1'), rounding=ROUND_HALF_UP
            )
        return Decimal('0.0')

    @property
    def is_overrun(self):
        """Whether spending has exceeded the budget."""
        return self.spent > self.limit_amount

    @property
    def currency_symbol(self):
        """Return the user's preferred currency symbol for display."""
        from finance.currency_utils import get_user_preferred_currency
        return get_user_preferred_currency(self.user).symbol


class Notification(models.Model):
    """
    In-app notifications for budget overruns and other alerts.
    One notification per budget breach (tracked via budget FK + unique logic).
    """
    TYPE_CHOICES = [
        ('BUDGET_WARNING', 'Budget Warning (80%+)'),
        ('BUDGET_OVERRUN', 'Budget Overrun'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications'
    )
    budget = models.ForeignKey(
        'Budget', on_delete=models.CASCADE,
        related_name='notifications',
        null=True, blank=True,
    )
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.message[:50]}"
