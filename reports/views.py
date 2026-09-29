import json
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .selectors import get_dashboard_summary, get_monthly_report, get_insights
from finance.currency_utils import get_user_preferred_currency


@login_required
def dashboard_view(request):
    """Full dashboard with stat cards, charts, recent transactions, alerts."""
    data = get_dashboard_summary(request.user)
    insights = get_insights(request.user)

    # Prepare chart data as JSON for Chart.js
    income_trend_labels = [
        m['month'].strftime('%b %Y') for m in data['income_trend']
    ]
    income_trend_values = [float(m['total']) for m in data['income_trend']]
    expense_trend_labels = [
        m['month'].strftime('%b %Y') for m in data['expense_trend']
    ]
    expense_trend_values = [float(m['total']) for m in data['expense_trend']]

    # Merge labels for trend chart (union of months, ordered)
    all_labels_set = dict()
    for m in data['income_trend']:
        all_labels_set[m['month']] = m['month'].strftime('%b %Y')
    for m in data['expense_trend']:
        all_labels_set[m['month']] = m['month'].strftime('%b %Y')
    sorted_months = sorted(all_labels_set.keys())
    trend_labels = [all_labels_set[m] for m in sorted_months]

    income_map = {m['month']: float(m['total']) for m in data['income_trend']}
    expense_map = {m['month']: float(m['total']) for m in data['expense_trend']}
    trend_income = [income_map.get(m, 0) for m in sorted_months]
    trend_expense = [expense_map.get(m, 0) for m in sorted_months]

    # Expense breakdown for doughnut chart
    expense_vals = [float(c['total']) for c in data['expense_breakdown']]
    total_exp = sum(expense_vals)
    expense_cats = [
        f"{c['category']} {round(float(c['total']) / total_exp * 100, 1)}%" if total_exp > 0 else c['category']
        for c in data['expense_breakdown']
    ]

    context = {
        **data,
        'insights': insights,
        'trend_labels_json': json.dumps(trend_labels),
        'trend_income_json': json.dumps(trend_income),
        'trend_expense_json': json.dumps(trend_expense),
        'expense_cats_json': json.dumps(expense_cats),
        'expense_vals_json': json.dumps(expense_vals),
    }
    return render(request, 'reports/dashboard.html', context)


@login_required
def monthly_report_view(request):
    """Monthly report with selectable year/month."""
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Clamp values
    if month < 1 or month > 12:
        month = today.month
    if year < 2000 or year > 2100:
        year = today.year

    report = get_monthly_report(request.user, year, month)

    # Expense breakdown for pie chart
    expense_vals = [float(c['total']) for c in report['expense_breakdown']]
    total_exp = sum(expense_vals)
    expense_cats = [
        f"{c['category']} {round(float(c['total']) / total_exp * 100, 1)}%" if total_exp > 0 else c['category']
        for c in report['expense_breakdown']
    ]

    # Income breakdown for pie chart
    income_cats = [c['category'] for c in report['income_breakdown']]
    income_vals = [float(c['total']) for c in report['income_breakdown']]

    # Investment breakdown for pie chart
    invest_cats = [c['category'] for c in report.get('investment_breakdown', [])]
    invest_vals = [float(c['total']) for c in report.get('investment_breakdown', [])]

    # Year/month options for the selector — pre-mark selected for template
    year_choices = [
        {'value': y, 'label': y, 'selected': 'selected' if y == year else ''}
        for y in range(today.year - 3, today.year + 1)
    ]
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
    ]
    month_choices = [
        {'value': i + 1, 'label': name, 'selected': 'selected' if i + 1 == month else ''}
        for i, name in enumerate(month_names)
    ]

    context = {
        'report': report,
        'selected_year': year,
        'selected_month': month,
        'year_choices': year_choices,
        'month_choices': month_choices,
        'expense_cats_json': json.dumps(expense_cats),
        'expense_vals_json': json.dumps(expense_vals),
        'income_cats_json': json.dumps(income_cats),
        'income_vals_json': json.dumps(income_vals),
        'invest_cats_json': json.dumps(invest_cats),
        'invest_vals_json': json.dumps(invest_vals),
    }
    return render(request, 'reports/monthly_report.html', context)


@login_required
def anomaly_view(request):
    """Spending anomaly detection page."""
    from .anomaly import get_anomalies
    data = get_anomalies(request.user)
    return render(request, 'reports/anomaly.html', data)


@login_required
def ai_insights_view(request):
    """AI-powered financial insights page."""
    from .ai_insights import get_ai_insights
    data = get_ai_insights(request.user)
    return render(request, 'reports/ai_insights.html', data)
