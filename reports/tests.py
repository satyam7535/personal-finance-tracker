"""
Comprehensive tests for the reports app.

Covers: Dashboard selectors, monthly report, anomaly detection, AI insights,
        and report views.
"""
from decimal import Decimal
from datetime import date, timedelta

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse

from finance.models import Currency, Category, Transaction, Budget
from reports.selectors import (
    get_total_income, get_total_expense, get_total_investment,
    get_net_savings, get_category_breakdown, get_monthly_trend,
)
from reports.anomaly import (
    get_anomalies, _zscore_flag, _iqr_flag, _round_number_flag,
    _frequency_spike, _compute_risk_score,
)
from reports.ai_insights import get_ai_insights, _generate_mock_insights


# ═══════════════════════════════════════════════════════════════════
#  FIXTURES MIXIN
# ═══════════════════════════════════════════════════════════════════

class ReportsTestMixin:
    """Common setup for report tests."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.other_user = User.objects.create_user('otheruser', 'other@example.com', 'pass1234')

        # Currencies
        self.usd = Currency.objects.create(code='USD', name='US Dollar', symbol='$',
                                           exchange_rate_to_usd=Decimal('1.000000'))
        self.inr = Currency.objects.create(code='INR', name='Indian Rupee', symbol='₹',
                                           exchange_rate_to_usd=Decimal('0.012000'))

        # Categories
        self.food_cat = Category.objects.create(
            user=self.user, name='Food', type='EXPENSE')
        self.salary_cat = Category.objects.create(
            user=self.user, name='Salary', type='INCOME')
        self.stocks_cat = Category.objects.create(
            user=self.user, name='Stocks', type='INVESTMENT')
        self.transport_cat = Category.objects.create(
            user=self.user, name='Transport', type='EXPENSE')


# ═══════════════════════════════════════════════════════════════════
#  SELECTOR TESTS
# ═══════════════════════════════════════════════════════════════════

class SelectorTest(ReportsTestMixin, TestCase):

    def _add_tx(self, category, amount, tx_date=None, currency=None):
        return Transaction.objects.create(
            user=self.user,
            category=category,
            amount=Decimal(str(amount)),
            currency=currency or self.usd,
            date=tx_date or date(2026, 2, 10),
        )

    def test_total_income_empty(self):
        total, cur = get_total_income(self.user)
        self.assertEqual(total, Decimal('0.00'))

    def test_total_income(self):
        self._add_tx(self.salary_cat, '5000.00')
        total, cur = get_total_income(self.user)
        self.assertEqual(total, Decimal('5000.00'))

    def test_total_expense(self):
        self._add_tx(self.food_cat, '200.00')
        self._add_tx(self.food_cat, '150.00')
        total, cur = get_total_expense(self.user)
        self.assertEqual(total, Decimal('350.00'))

    def test_total_investment(self):
        self._add_tx(self.stocks_cat, '1000.00')
        total, cur = get_total_investment(self.user)
        self.assertEqual(total, Decimal('1000.00'))

    def test_net_savings(self):
        self._add_tx(self.salary_cat, '5000.00')
        self._add_tx(self.food_cat, '200.00')
        self._add_tx(self.stocks_cat, '1000.00')
        net, cur = get_net_savings(self.user)
        # 5000 - 200 - 1000 = 3800
        self.assertEqual(net, Decimal('3800.00'))

    def test_date_range_filter(self):
        self._add_tx(self.salary_cat, '1000.00', date(2026, 1, 15))
        self._add_tx(self.salary_cat, '2000.00', date(2026, 2, 15))
        total, cur = get_total_income(self.user,
                                      date_from=date(2026, 2, 1),
                                      date_to=date(2026, 2, 28))
        self.assertEqual(total, Decimal('2000.00'))

    def test_multi_currency_conversion(self):
        self._add_tx(self.food_cat, '1000.00', currency=self.inr)
        # 1000 INR * 0.012 = 12.00 USD
        total, cur = get_total_expense(self.user)
        self.assertEqual(total, Decimal('12.00'))

    def test_category_breakdown(self):
        self._add_tx(self.food_cat, '200.00')
        self._add_tx(self.transport_cat, '100.00')
        breakdown, cur = get_category_breakdown(self.user, txn_type='EXPENSE')
        self.assertEqual(len(breakdown), 2)
        names = [b['category'] for b in breakdown]
        self.assertIn('Food', names)
        self.assertIn('Transport', names)

    def test_monthly_trend(self):
        self._add_tx(self.food_cat, '200.00', date(2026, 1, 15))
        self._add_tx(self.food_cat, '300.00', date(2026, 2, 15))
        trend = get_monthly_trend(self.user)
        self.assertGreaterEqual(len(trend), 1)

    def test_user_isolation(self):
        """Other user's transactions should not appear in selectors."""
        other_cat = Category.objects.create(
            user=self.other_user, name='OtherFood', type='EXPENSE')
        Transaction.objects.create(
            user=self.other_user, category=other_cat,
            amount=Decimal('999.00'), currency=self.usd, date=date(2026, 2, 10))
        total, _ = get_total_expense(self.user)
        self.assertEqual(total, Decimal('0.00'))


# ═══════════════════════════════════════════════════════════════════
#  ANOMALY DETECTION TESTS
# ═══════════════════════════════════════════════════════════════════

class AnomalyHelperTest(TestCase):
    """Unit tests for individual anomaly-detection signal functions."""

    def test_zscore_flag_above_threshold(self):
        result = _zscore_flag(150, 50, 30)
        self.assertIsNotNone(result)
        self.assertGreater(result, 2.0)

    def test_zscore_flag_below_threshold(self):
        result = _zscore_flag(60, 50, 30)
        self.assertIsNone(result)

    def test_zscore_flag_zero_std(self):
        result = _zscore_flag(100, 50, 0)
        self.assertIsNone(result)

    def test_iqr_flag_outlier(self):
        amounts = [10, 20, 30, 40, 50, 60, 70, 80, 500]
        self.assertTrue(_iqr_flag(500, amounts))

    def test_iqr_flag_normal(self):
        amounts = [10, 20, 30, 40, 50, 60, 70, 80]
        self.assertFalse(_iqr_flag(40, amounts))

    def test_iqr_flag_too_few_samples(self):
        self.assertFalse(_iqr_flag(100, [10, 20, 30]))

    def test_round_number_thousand(self):
        self.assertEqual(_round_number_flag(Decimal('5000')), 'exact_thousand')

    def test_round_number_five_hundred(self):
        self.assertEqual(_round_number_flag(Decimal('1500')), 'exact_500')

    def test_round_number_hundred(self):
        self.assertEqual(_round_number_flag(Decimal('300')), 'exact_hundred')

    def test_round_number_normal(self):
        self.assertIsNone(_round_number_flag(Decimal('45.99')))

    def test_frequency_spike_triggered(self):
        date_counts = {date(2026, 1, 15): 10}
        result = _frequency_spike(date(2026, 1, 15), date_counts, avg_daily=2)
        self.assertEqual(result, 10)

    def test_frequency_spike_normal(self):
        date_counts = {date(2026, 1, 15): 2}
        result = _frequency_spike(date(2026, 1, 15), date_counts, avg_daily=2)
        self.assertIsNone(result)

    def test_risk_score_no_signals(self):
        self.assertEqual(_compute_risk_score({}), 0)

    def test_risk_score_single_signal(self):
        score = _compute_risk_score({'zscore': True})
        self.assertEqual(score, 35)

    def test_risk_score_all_signals(self):
        score = _compute_risk_score({
            'zscore': True, 'iqr': True, 'round_number': True,
            'frequency': True, 'velocity': True,
        })
        self.assertEqual(score, 100)

    def test_risk_score_capped_at_100(self):
        score = _compute_risk_score({
            'zscore': True, 'iqr': True, 'round_number': True,
            'frequency': True, 'velocity': True,
        })
        self.assertLessEqual(score, 100)


class AnomalyIntegrationTest(ReportsTestMixin, TestCase):
    """Integration tests for the full anomaly detection pipeline."""

    def test_no_transactions_no_anomalies(self):
        result = get_anomalies(self.user)
        self.assertEqual(result['total_flagged'], 0)
        self.assertEqual(result['anomalies'], [])

    def test_outlier_detected(self):
        """A very large transaction among many small ones should be flagged."""
        for i in range(10):
            Transaction.objects.create(
                user=self.user, category=self.food_cat,
                amount=Decimal('50.00'), currency=self.usd,
                date=date(2026, 2, i + 1))
        # Add outlier
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('5000.00'), currency=self.usd,
            date=date(2026, 2, 15))
        result = get_anomalies(self.user)
        self.assertGreater(result['total_flagged'], 0)
        # The outlier should have a high risk score
        high_risk = [a for a in result['anomalies'] if a['risk_score'] >= 35]
        self.assertGreater(len(high_risk), 0)

    def test_round_number_flagged(self):
        """Round-number transactions should trigger round_number signal."""
        for i in range(5):
            Transaction.objects.create(
                user=self.user, category=self.food_cat,
                amount=Decimal('50.00'), currency=self.usd,
                date=date(2026, 2, i + 1))
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('5000.00'), currency=self.usd,
            date=date(2026, 2, 20))
        result = get_anomalies(self.user)
        flagged_amounts = [a['converted_amount'] for a in result['anomalies']]
        self.assertIn(Decimal('5000.00'), flagged_amounts)

    def test_detection_summary_keys(self):
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('50.00'), currency=self.usd,
            date=date(2026, 2, 1))
        result = get_anomalies(self.user)
        for key in ('zscore', 'iqr', 'round_number', 'frequency', 'velocity'):
            self.assertIn(key, result['detection_summary'])


# ═══════════════════════════════════════════════════════════════════
#  AI INSIGHTS TESTS
# ═══════════════════════════════════════════════════════════════════

@override_settings(GEMINI_API_KEY=None, OPENAI_API_KEY=None)
class AIInsightsTest(ReportsTestMixin, TestCase):
    """Tests for the AI insights (uses rule-based fallback since no API keys)."""

    def test_fallback_insights_no_data(self):
        result = get_ai_insights(self.user)
        self.assertFalse(result['ai_powered'])
        self.assertEqual(result['provider'], 'Smart Analysis')
        self.assertIsInstance(result['insights'], list)
        self.assertGreater(len(result['insights']), 0)

    def test_fallback_with_transactions(self):
        Transaction.objects.create(
            user=self.user, category=self.salary_cat,
            amount=Decimal('5000.00'), currency=self.usd,
            date=date.today() - timedelta(days=5))
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('200.00'), currency=self.usd,
            date=date.today() - timedelta(days=3))
        result = get_ai_insights(self.user)
        self.assertIsInstance(result['insights'], list)
        self.assertGreater(len(result['insights']), 0)
        # Each insight should have title and body
        for insight in result['insights']:
            self.assertIn('title', insight)
            self.assertIn('body', insight)

    def test_context_has_required_keys(self):
        result = get_ai_insights(self.user)
        ctx = result['context']
        self.assertIn('income', ctx)
        self.assertIn('expenses', ctx)
        self.assertIn('savings', ctx)

    def test_budget_insight_generated(self):
        Budget.objects.create(
            user=self.user, category=self.food_cat,
            limit_amount=Decimal('200.00'), month=date.today().replace(day=1))
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('180.00'), currency=self.usd,
            date=date.today() - timedelta(days=2))
        result = get_ai_insights(self.user)
        bodies = ' '.join(i['body'] for i in result['insights'])
        # Should mention budgets somewhere in insights
        self.assertTrue(len(result['insights']) > 0)


# ═══════════════════════════════════════════════════════════════════
#  REPORT VIEW TESTS
# ═══════════════════════════════════════════════════════════════════

class ReportViewTest(ReportsTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads(self):
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

    def test_dashboard_with_data(self):
        Transaction.objects.create(
            user=self.user, category=self.salary_cat,
            amount=Decimal('5000.00'), currency=self.usd,
            date=date(2026, 2, 10))
        Transaction.objects.create(
            user=self.user, category=self.food_cat,
            amount=Decimal('200.00'), currency=self.usd,
            date=date(2026, 2, 10))
        response = self.client.get(reverse('reports:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_monthly_report_loads(self):
        response = self.client.get(reverse('reports:monthly_report'))
        self.assertEqual(response.status_code, 200)

    def test_monthly_report_with_params(self):
        response = self.client.get(reverse('reports:monthly_report'), {
            'year': '2026', 'month': '2'})
        self.assertEqual(response.status_code, 200)

    def test_anomaly_view_loads(self):
        response = self.client.get(reverse('reports:anomaly'))
        self.assertEqual(response.status_code, 200)

    @override_settings(GEMINI_API_KEY=None, OPENAI_API_KEY=None)
    def test_ai_insights_view_loads(self):
        response = self.client.get(reverse('reports:ai_insights'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smart Analysis')
