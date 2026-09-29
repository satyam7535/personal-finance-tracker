"""
Aggregation selectors for the reports / dashboard layer.

All monetary totals are converted to the user's preferred currency
via USD as the intermediary (amount × from_rate / target_rate).

These selectors are the ONLY place where report-level queries live.
Views call selectors — never raw ORM aggregation.

Usage:
    from reports.selectors import get_dashboard_summary, get_monthly_report
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import date

from django.db.models import Sum, F, Value, DecimalField, Count, Subquery, OuterRef
from django.db.models.functions import TruncMonth, Coalesce, ExtractYear, ExtractMonth

from finance.models import Transaction, Category, Budget
from finance.currency_utils import get_user_preferred_currency


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _to_preferred(qs, target_rate):
    """
    Aggregate a queryset's amount to a single total in the user's
    preferred currency.

    Formula per row: amount * currency.exchange_rate_to_usd / target_rate
    aggregate(Sum(...)) → single Decimal.
    """
    if not target_rate or target_rate <= 0:
        target_rate = Decimal('1')
        
    total = qs.annotate(
        converted=F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')) / Value(
            target_rate, output_field=DecimalField(max_digits=18, decimal_places=6)
        )
    ).aggregate(
        total=Coalesce(Sum('converted'), Value(Decimal('0.00')))
    )['total']
    return Decimal(str(total)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def _base_qs(user, date_from=None, date_to=None):
    """Base queryset scoped to user + optional date range."""
    qs = Transaction.objects.filter(user=user)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    return qs


# ─── Single-figure selectors ─────────────────────────────────────────────────

def get_total_income(user, date_from=None, date_to=None):
    """Total income in the user's preferred currency."""
    target = get_user_preferred_currency(user)
    qs = _base_qs(user, date_from, date_to).filter(type='INCOME')
    return _to_preferred(qs, target.exchange_rate_to_usd), target


def get_total_expense(user, date_from=None, date_to=None):
    """Total expenses in the user's preferred currency."""
    target = get_user_preferred_currency(user)
    qs = _base_qs(user, date_from, date_to).filter(type='EXPENSE')
    return _to_preferred(qs, target.exchange_rate_to_usd), target


def get_total_investment(user, date_from=None, date_to=None):
    """Total investments in the user's preferred currency."""
    target = get_user_preferred_currency(user)
    qs = _base_qs(user, date_from, date_to).filter(type='INVESTMENT')
    return _to_preferred(qs, target.exchange_rate_to_usd), target


def get_net_savings(user, date_from=None, date_to=None):
    """Net savings = income − expense − investment, in preferred currency."""
    income, cur = get_total_income(user, date_from, date_to)
    expense, _ = get_total_expense(user, date_from, date_to)
    investment, _ = get_total_investment(user, date_from, date_to)
    return income - expense - investment, cur


# ─── Breakdown selectors ─────────────────────────────────────────────────────

def get_category_breakdown(user, txn_type=None, date_from=None, date_to=None):
    """
    Per-category totals in the user's preferred currency.

    Returns a list of dicts:
        [{ 'category': str, 'category_id': int, 'type': str, 'total': Decimal }, ...]
    Sorted by total descending.
    """
    target = get_user_preferred_currency(user)
    target_rate = target.exchange_rate_to_usd
    if not target_rate or target_rate <= 0:
        target_rate = Decimal('1')

    qs = _base_qs(user, date_from, date_to)
    if txn_type:
        qs = qs.filter(type=txn_type)

    rows = (
        qs
        .values('category__id', 'category__name', 'type')
        .annotate(
            raw_total=Sum(
                F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')) / Value(
                    target_rate, output_field=DecimalField(max_digits=18, decimal_places=6)
                )
            )
        )
        .order_by('-raw_total')
    )

    results = []
    for row in rows:
        results.append({
            'category_id': row['category__id'],
            'category': row['category__name'],
            'type': row['type'],
            'total': Decimal(str(row['raw_total'])).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ),
        })
    return results, target


def get_monthly_trend(user, txn_type=None, months=6):
    """
    Monthly totals for the last N months in preferred currency.

    Returns:
        [{ 'month': date, 'total': Decimal }, ...]
    Ordered chronologically.
    """
    target = get_user_preferred_currency(user)
    target_rate = target.exchange_rate_to_usd
    if not target_rate or target_rate <= 0:
        target_rate = Decimal('1')

    today = date.today()
    # Start from N months ago (1st of that month)
    start_month = today.month - months
    start_year = today.year
    while start_month <= 0:
        start_month += 12
        start_year -= 1
    cutoff = date(start_year, start_month, 1)

    qs = _base_qs(user, date_from=cutoff)
    if txn_type:
        qs = qs.filter(type=txn_type)

    rows = (
        qs
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            raw_total=Coalesce(
                Sum(
                    F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')) / Value(
                        target_rate,
                        output_field=DecimalField(max_digits=18, decimal_places=6)
                    )
                ),
                Value(Decimal('0.00')),
            )
        )
        .order_by('month')
    )

    results = []
    for row in rows:
        results.append({
            'month': row['month'],
            'total': Decimal(str(row['raw_total'])).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ),
        })
    return results, target


# ─── Monthly report selector ─────────────────────────────────────────────────

def get_monthly_report(user, year, month):
    """
    Full monthly report for a given year/month.

    Returns a dict with:
        income, expense, investment, savings,
        expense_breakdown (list), income_breakdown (list),
        investment_breakdown (list), budget_status (list),
        currency (Currency instance)
    """
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1)
    else:
        last_day = date(year, month + 1, 1)
    # last_day is exclusive; use date_to = last_day - 1 day
    from datetime import timedelta
    end = last_day - timedelta(days=1)

    income, cur = get_total_income(user, first_day, end)
    expense, _ = get_total_expense(user, first_day, end)
    investment, _ = get_total_investment(user, first_day, end)
    savings = income - expense - investment

    expense_bkdn, _ = get_category_breakdown(user, 'EXPENSE', first_day, end)
    income_bkdn, _ = get_category_breakdown(user, 'INCOME', first_day, end)
    investment_bkdn, _ = get_category_breakdown(user, 'INVESTMENT', first_day, end)

    # Budget status for this month
    spent_usd_sq = Transaction.objects.filter(
        user=user,
        type='EXPENSE',
        category=OuterRef('category_id'),
        date__year=year,
        date__month=month,
    ).values('category_id').annotate(
        total=Sum(F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')))
    ).values('total')

    budgets = Budget.objects.filter(
        user=user,
        month__year=year,
        month__month=month,
    ).select_related('category').annotate(
        spent_usd=Coalesce(Subquery(spent_usd_sq, output_field=DecimalField(max_digits=18, decimal_places=6)), Value(Decimal('0.00')))
    )

    budget_status = []
    for b in budgets:
        budget_rate = b._budget_currency().exchange_rate_to_usd or Decimal('1')
        spent = (b.spent_usd / budget_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        pct = (spent / b.limit_amount * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) if b.limit_amount > 0 else Decimal('0.0')
        is_overrun = spent > b.limit_amount
        
        budget_status.append({
            'category': b.category.name,
            'limit': b.limit_amount,
            'spent': spent,
            'percentage': pct,
            'is_overrun': is_overrun,
            'remaining': b.limit_amount - spent,
        })

    return {
        'year': year,
        'month': month,
        'month_name': first_day.strftime('%B %Y'),
        'income': income,
        'expense': expense,
        'investment': investment,
        'savings': savings,
        'expense_breakdown': expense_bkdn,
        'income_breakdown': income_bkdn,
        'investment_breakdown': investment_bkdn,
        'budget_status': budget_status,
        'currency': cur,
    }


# ─── Dashboard selector ──────────────────────────────────────────────────────

def get_dashboard_summary(user):
    """
    All data needed for the dashboard view, aggregated in one call.

    Returns a dict with:
        - totals (income, expense, investment, savings) for current month
        - category breakdowns for current month
        - 6-month income/expense trend
        - recent transactions (last 5)
        - budget alerts (overrun / >80%)
        - currency (Currency instance)
    """
    today = date.today()
    first_of_month = today.replace(day=1)

    # Current-month totals
    income, cur = get_total_income(user, first_of_month, today)
    expense, _ = get_total_expense(user, first_of_month, today)
    investment, _ = get_total_investment(user, first_of_month, today)
    savings = income - expense - investment

    # Category breakdowns (current month)
    expense_bkdn, _ = get_category_breakdown(user, 'EXPENSE', first_of_month, today)
    income_bkdn, _ = get_category_breakdown(user, 'INCOME', first_of_month, today)

    # 6-month trends
    income_trend, _ = get_monthly_trend(user, 'INCOME', months=6)
    expense_trend, _ = get_monthly_trend(user, 'EXPENSE', months=6)

    # Recent transactions
    recent = (
        Transaction.objects
        .filter(user=user)
        .select_related('category', 'currency')
        [:5]
    )

    # Budget alerts
    spent_usd_sq = Transaction.objects.filter(
        user=user,
        type='EXPENSE',
        category=OuterRef('category_id'),
        date__year=today.year,
        date__month=today.month,
    ).values('category_id').annotate(
        total=Sum(F('amount') * Coalesce(F('exchange_rate_at_time'), F('currency__exchange_rate_to_usd')))
    ).values('total')

    budgets = Budget.objects.filter(
        user=user,
        month__year=today.year,
        month__month=today.month,
    ).select_related('category').annotate(
        spent_usd=Coalesce(Subquery(spent_usd_sq, output_field=DecimalField(max_digits=18, decimal_places=6)), Value(Decimal('0.00')))
    )

    budget_alerts = []
    for b in budgets:
        budget_rate = b._budget_currency().exchange_rate_to_usd or Decimal('1')
        spent = (b.spent_usd / budget_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        pct = (spent / b.limit_amount * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) if b.limit_amount > 0 else Decimal('0.0')
        is_overrun = spent > b.limit_amount
        
        if pct >= 80:
            budget_alerts.append({
                'category': b.category.name,
                'limit': b.limit_amount,
                'spent': spent,
                'percentage': pct,
                'is_overrun': is_overrun,
            })

    return {
        'income': income,
        'expense': expense,
        'investment': investment,
        'savings': savings,
        'expense_breakdown': expense_bkdn,
        'income_breakdown': income_bkdn,
        'income_trend': income_trend,
        'expense_trend': expense_trend,
        'recent_transactions': recent,
        'budget_alerts': budget_alerts,
        'currency': cur,
    }


# ─── Insights ────────────────────────────────────────────────────────────────

def get_insights(user):
    """
    Generate simple financial insights / tips based on the user's data.

    Returns a list of insight strings.
    """
    today = date.today()
    first_of_month = today.replace(day=1)
    insights = []

    income, cur = get_total_income(user, first_of_month, today)
    expense, _ = get_total_expense(user, first_of_month, today)
    investment, _ = get_total_investment(user, first_of_month, today)

    # Savings rate
    if income > 0:
        savings_rate = ((income - expense - investment) / income * 100).quantize(
            Decimal('0.1'), rounding=ROUND_HALF_UP
        )
        if savings_rate >= 30:
            insights.append(
                f"Great job! You're saving {savings_rate}% of your income this month."
            )
        elif savings_rate >= 10:
            insights.append(
                f"You're saving {savings_rate}% of your income. "
                f"Try to push it above 30% for long-term wealth building."
            )
        elif savings_rate > 0:
            insights.append(
                f"Your savings rate is only {savings_rate}%. "
                f"Review your expenses for areas to cut back."
            )
        else:
            insights.append(
                "You're spending more than you earn this month. "
                "Consider reducing discretionary expenses."
            )

    # Top expense category
    expense_bkdn, _ = get_category_breakdown(user, 'EXPENSE', first_of_month, today)
    if expense_bkdn:
        top = expense_bkdn[0]
        if expense > 0:
            pct = (top['total'] / expense * 100).quantize(
                Decimal('0.1'), rounding=ROUND_HALF_UP
            )
            insights.append(
                f"Your biggest expense category is \"{top['category']}\" "
                f"at {cur.symbol}{top['total']} ({pct}% of total expenses)."
            )

    # Investment check
    if investment == 0 and income > 0:
        insights.append(
            "You haven't made any investments this month. "
            "Consider allocating at least 10-20% of income to investments."
        )

    # Budget overruns
    budgets = Budget.objects.filter(
        user=user,
        month__year=today.year,
        month__month=today.month,
    ).select_related('category')

    overruns = [b for b in budgets if b.is_overrun]
    if overruns:
        names = ', '.join(b.category.name for b in overruns)
        insights.append(
            f"Budget overrun in: {names}. Review spending in these categories."
        )

    # No data fallback
    if not insights:
        insights.append(
            "Start adding transactions to get personalised financial insights!"
        )

    return insights
