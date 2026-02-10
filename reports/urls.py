from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('reports/', views.monthly_report_view, name='monthly_report'),
    path('anomalies/', views.anomaly_view, name='anomaly'),
    path('ai-insights/', views.ai_insights_view, name='ai_insights'),
]
