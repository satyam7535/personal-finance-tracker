from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    """Dashboard — will be fully built in Phase 8."""
    return render(request, 'reports/dashboard.html')


@login_required
def monthly_report_view(request):
    """Monthly report — will be fully built in Phase 8."""
    return render(request, 'reports/monthly_report.html')
