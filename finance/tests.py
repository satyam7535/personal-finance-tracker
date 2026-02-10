"""
Comprehensive tests for the finance app.

Covers: Models, Services, Views, Currency Utils, Import Service.
"""
import io
from decimal import Decimal
from datetime import date

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.urls import reverse
from django.db.models import ProtectedError

from finance.models import Currency, Category, Transaction, Budget, Notification
from finance.services import (
    create_transaction, update_transaction, delete_transaction, get_user_transactions,
)
from finance.currency_utils import (
    convert_amount, convert_to_usd, get_user_preferred_currency, get_currency,
)


# ═══════════════════════════════════════════════════════════════════
#  FIXTURES MIXIN
# ═══════════════════════════════════════════════════════════════════

class FinanceTestMixin:
    """Common setup for finance tests."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'pass1234')
        self.other_user = User.objects.create_user('otheruser', 'other@example.com', 'pass1234')

        # Currencies
        self.usd = Currency.objects.create(code='USD', name='US Dollar', symbol='$',
                                           exchange_rate_to_usd=Decimal('1.000000'))
        self.inr = Currency.objects.create(code='INR', name='Indian Rupee', symbol='₹',
                                           exchange_rate_to_usd=Decimal('0.012000'))
        self.eur = Currency.objects.create(code='EUR', name='Euro', symbol='€',
                                           exchange_rate_to_usd=Decimal('1.080000'))

        # Categories
        self.expense_cat = Category.objects.create(
            user=self.user, name='Food', type='EXPENSE')
        self.income_cat = Category.objects.create(
            user=self.user, name='Salary', type='INCOME')
        self.invest_cat = Category.objects.create(
            user=self.user, name='Stocks', type='INVESTMENT')
        self.other_user_cat = Category.objects.create(
            user=self.other_user, name='Other Food', type='EXPENSE')


# ═══════════════════════════════════════════════════════════════════
#  MODEL TESTS
# ═══════════════════════════════════════════════════════════════════

class CurrencyModelTest(TestCase):

    def test_currency_str(self):
        c = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        self.assertEqual(str(c), 'USD - US Dollar')

    def test_default_exchange_rate(self):
        c = Currency.objects.create(code='GBP', name='Pound', symbol='£')
        self.assertEqual(c.exchange_rate_to_usd, Decimal('1.000000'))


class CategoryModelTest(FinanceTestMixin, TestCase):

    def test_category_str(self):
        self.assertEqual(str(self.expense_cat), 'Food (Expense)')

    def test_unique_together_user_name_type(self):
        with self.assertRaises(Exception):
            Category.objects.create(user=self.user, name='Food', type='EXPENSE')

    def test_blank_name_rejected(self):
        cat = Category(user=self.user, name='   ', type='EXPENSE')
        with self.assertRaises(ValidationError):
            cat.full_clean()

    def test_two_users_same_category_name_allowed(self):
        cat = Category.objects.create(user=self.other_user, name='Food', type='EXPENSE')
        self.assertIsNotNone(cat.pk)


class TransactionModelTest(FinanceTestMixin, TestCase):

    def test_create_expense(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('50.00'), currency=self.usd, date=date.today())
        tx.save()
        self.assertEqual(tx.type, 'EXPENSE')
        self.assertEqual(tx.amount, Decimal('50.00'))

    def test_type_auto_set_from_category(self):
        tx = Transaction(user=self.user, category=self.income_cat,
                         amount=Decimal('1000.00'), currency=self.usd, date=date.today())
        tx.save()
        self.assertEqual(tx.type, 'INCOME')

    def test_decimal_precision_rounded(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('50.999'), currency=self.usd, date=date.today())
        tx.save()
        self.assertEqual(tx.amount, Decimal('51.00'))

    def test_zero_amount_rejected(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('0'), currency=self.usd, date=date.today())
        with self.assertRaises(ValidationError) as ctx:
            tx.save()
        self.assertIn('amount', ctx.exception.message_dict)

    def test_negative_amount_allowed_for_expense_refund(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('-25.00'), currency=self.usd, date=date.today())
        tx.save()
        self.assertEqual(tx.amount, Decimal('-25.00'))
        self.assertEqual(tx.type, 'EXPENSE')

    def test_negative_amount_rejected_for_income(self):
        tx = Transaction(user=self.user, category=self.income_cat,
                         amount=Decimal('-100.00'), currency=self.usd, date=date.today())
        with self.assertRaises(ValidationError) as ctx:
            tx.save()
        self.assertIn('amount', ctx.exception.message_dict)

    def test_negative_amount_rejected_for_investment(self):
        tx = Transaction(user=self.user, category=self.invest_cat,
                         amount=Decimal('-50.00'), currency=self.usd, date=date.today())
        with self.assertRaises(ValidationError):
            tx.save()

    def test_other_users_category_rejected(self):
        tx = Transaction(user=self.user, category=self.other_user_cat,
                         amount=Decimal('50.00'), currency=self.usd, date=date.today())
        with self.assertRaises(ValidationError) as ctx:
            tx.save()
        self.assertIn('category', ctx.exception.message_dict)

    def test_category_with_transactions_cannot_be_deleted(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('50.00'), currency=self.usd, date=date.today())
        tx.save()
        with self.assertRaises(ProtectedError):
            self.expense_cat.delete()

    def test_amount_in_usd_property(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('1000.00'), currency=self.inr, date=date.today())
        tx.save()
        # 1000 INR * 0.012 = 12.00 USD
        self.assertEqual(tx.amount_in_usd, Decimal('12.00'))

    def test_transaction_str(self):
        tx = Transaction(user=self.user, category=self.expense_cat,
                         amount=Decimal('50.00'), currency=self.usd, date=date(2026, 1, 15))
        tx.save()
        self.assertIn('Expense', str(tx))
        self.assertIn('50.00', str(tx))


class BudgetModelTest(FinanceTestMixin, TestCase):

    def test_create_budget(self):
        b = Budget(user=self.user, category=self.expense_cat,
                   limit_amount=Decimal('500.00'), month=date(2026, 2, 1))
        b.full_clean()
        b.save()
        self.assertEqual(b.limit_amount, Decimal('500.00'))

    def test_budget_only_for_expense_categories(self):
        b = Budget(user=self.user, category=self.income_cat,
                   limit_amount=Decimal('500.00'), month=date(2026, 2, 1))
        with self.assertRaises(ValidationError) as ctx:
            b.full_clean()
        self.assertIn('category', ctx.exception.message_dict)

    def test_negative_limit_rejected(self):
        b = Budget(user=self.user, category=self.expense_cat,
                   limit_amount=Decimal('-100.00'), month=date(2026, 2, 1))
        with self.assertRaises(ValidationError) as ctx:
            b.full_clean()
        self.assertIn('limit_amount', ctx.exception.message_dict)

    def test_zero_limit_rejected(self):
        b = Budget(user=self.user, category=self.expense_cat,
                   limit_amount=Decimal('0.00'), month=date(2026, 2, 1))
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_month_normalised_to_first(self):
        b = Budget(user=self.user, category=self.expense_cat,
                   limit_amount=Decimal('500.00'), month=date(2026, 2, 15))
        b.full_clean()
        self.assertEqual(b.month, date(2026, 2, 1))

    def test_spent_property(self):
        b = Budget.objects.create(user=self.user, category=self.expense_cat,
                                  limit_amount=Decimal('500.00'), month=date(2026, 2, 1))
        Transaction.objects.create(user=self.user, category=self.expense_cat,
                                   amount=Decimal('100.00'), currency=self.usd,
                                   date=date(2026, 2, 10))
        Transaction.objects.create(user=self.user, category=self.expense_cat,
                                   amount=Decimal('200.00'), currency=self.usd,
                                   date=date(2026, 2, 15))
        # spent should be 300
        self.assertGreaterEqual(b.spent, Decimal('200.00'))

    def test_percentage_used(self):
        b = Budget.objects.create(user=self.user, category=self.expense_cat,
                                  limit_amount=Decimal('100.00'), month=date(2026, 2, 1))
        Transaction.objects.create(user=self.user, category=self.expense_cat,
                                   amount=Decimal('80.00'), currency=self.usd,
                                   date=date(2026, 2, 5))
        self.assertGreaterEqual(b.percentage_used, Decimal('50'))

    def test_is_overrun(self):
        b = Budget.objects.create(user=self.user, category=self.expense_cat,
                                  limit_amount=Decimal('100.00'), month=date(2026, 2, 1))
        Transaction.objects.create(user=self.user, category=self.expense_cat,
                                   amount=Decimal('150.00'), currency=self.usd,
                                   date=date(2026, 2, 5))
        self.assertTrue(b.is_overrun)

    def test_budget_other_users_category_rejected(self):
        b = Budget(user=self.user, category=self.other_user_cat,
                   limit_amount=Decimal('500.00'), month=date(2026, 2, 1))
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_unique_together_user_category_month(self):
        Budget.objects.create(user=self.user, category=self.expense_cat,
                              limit_amount=Decimal('500.00'), month=date(2026, 2, 1))
        with self.assertRaises(Exception):
            Budget.objects.create(user=self.user, category=self.expense_cat,
                                  limit_amount=Decimal('600.00'), month=date(2026, 2, 1))


class NotificationModelTest(FinanceTestMixin, TestCase):

    def test_notification_str(self):
        b = Budget.objects.create(user=self.user, category=self.expense_cat,
                                  limit_amount=Decimal('100.00'), month=date(2026, 2, 1))
        n = Notification.objects.create(
            user=self.user, budget=b, message='Budget overrun!',
            notification_type='BUDGET_OVERRUN')
        self.assertIn('Overrun', str(n))

    def test_notification_default_unread(self):
        n = Notification.objects.create(
            user=self.user, message='Test', notification_type='BUDGET_WARNING')
        self.assertFalse(n.is_read)


# ═══════════════════════════════════════════════════════════════════
#  SERVICE LAYER TESTS
# ═══════════════════════════════════════════════════════════════════

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TransactionServiceTest(FinanceTestMixin, TestCase):

    def _make_data(self, **overrides):
        defaults = {
            'category': self.expense_cat,
            'amount': Decimal('50.00'),
            'currency': self.usd,
            'date': date(2026, 2, 10),
            'description': 'Test transaction',
        }
        defaults.update(overrides)
        return defaults

    def test_create_transaction(self):
        tx = create_transaction(self.user, self._make_data())
        self.assertIsNotNone(tx.pk)
        self.assertEqual(tx.type, 'EXPENSE')
        self.assertEqual(tx.user, self.user)

    def test_create_income_transaction(self):
        tx = create_transaction(self.user, self._make_data(
            category=self.income_cat, amount=Decimal('5000.00')))
        self.assertEqual(tx.type, 'INCOME')

    def test_create_triggers_budget_check(self):
        Budget.objects.create(user=self.user, category=self.expense_cat,
                              limit_amount=Decimal('100.00'), month=date(2026, 2, 1))
        create_transaction(self.user, self._make_data(amount=Decimal('90.00')))
        # Should create a budget warning notification (90% > 80%)
        self.assertTrue(Notification.objects.filter(
            user=self.user, notification_type='BUDGET_WARNING').exists())

    def test_create_overrun_notification(self):
        Budget.objects.create(user=self.user, category=self.expense_cat,
                              limit_amount=Decimal('100.00'), month=date(2026, 2, 1))
        create_transaction(self.user, self._make_data(amount=Decimal('150.00')))
        self.assertTrue(Notification.objects.filter(
            user=self.user, notification_type='BUDGET_OVERRUN').exists())

    def test_update_transaction(self):
        tx = create_transaction(self.user, self._make_data())
        updated = update_transaction(self.user, tx.pk, self._make_data(
            amount=Decimal('75.00'), description='Updated'))
        self.assertEqual(updated.amount, Decimal('75.00'))
        self.assertEqual(updated.description, 'Updated')

    def test_update_other_users_transaction_denied(self):
        tx = create_transaction(self.user, self._make_data())
        with self.assertRaises(PermissionDenied):
            update_transaction(self.other_user, tx.pk, self._make_data())

    def test_delete_transaction(self):
        tx = create_transaction(self.user, self._make_data())
        pk = tx.pk
        delete_transaction(self.user, pk)
        self.assertFalse(Transaction.objects.filter(pk=pk).exists())

    def test_delete_other_users_transaction_denied(self):
        tx = create_transaction(self.user, self._make_data())
        with self.assertRaises(PermissionDenied):
            delete_transaction(self.other_user, tx.pk)

    def test_get_user_transactions_filtered_by_type(self):
        create_transaction(self.user, self._make_data())
        create_transaction(self.user, self._make_data(
            category=self.income_cat, amount=Decimal('5000.00')))
        qs = get_user_transactions(self.user, {'type': 'EXPENSE'})
        self.assertEqual(qs.count(), 1)

    def test_get_user_transactions_filtered_by_date(self):
        create_transaction(self.user, self._make_data(date=date(2026, 1, 1)))
        create_transaction(self.user, self._make_data(date=date(2026, 3, 1)))
        qs = get_user_transactions(self.user, {
            'date_from': date(2026, 2, 1),
            'date_to': date(2026, 2, 28),
        })
        self.assertEqual(qs.count(), 0)


# ═══════════════════════════════════════════════════════════════════
#  CURRENCY UTILS TESTS
# ═══════════════════════════════════════════════════════════════════

class CurrencyUtilsTest(FinanceTestMixin, TestCase):

    def test_same_currency_no_conversion(self):
        result = convert_amount(Decimal('100.00'), self.usd, self.usd)
        self.assertEqual(result, Decimal('100.00'))

    def test_convert_inr_to_usd(self):
        # 1000 INR * 0.012 = 12.00 USD
        result = convert_amount(Decimal('1000.00'), self.inr, self.usd)
        self.assertEqual(result, Decimal('12.00'))

    def test_convert_usd_to_inr(self):
        # 12 USD / 0.012 = 1000 INR
        result = convert_amount(Decimal('12.00'), self.usd, self.inr)
        self.assertEqual(result, Decimal('1000.00'))

    def test_convert_eur_to_inr(self):
        # 100 EUR * 1.08 = 108 USD; 108 / 0.012 = 9000 INR
        result = convert_amount(Decimal('100.00'), self.eur, self.inr)
        self.assertEqual(result, Decimal('9000.00'))

    def test_convert_none_returns_zero(self):
        result = convert_amount(None, self.usd, self.inr)
        self.assertEqual(result, Decimal('0.00'))

    def test_convert_to_usd_function(self):
        result = convert_to_usd(Decimal('1000.00'), self.inr)
        self.assertEqual(result, Decimal('12.00'))

    def test_get_currency_active(self):
        c = get_currency('USD')
        self.assertIsNotNone(c)
        self.assertEqual(c.code, 'USD')

    def test_get_currency_nonexistent(self):
        c = get_currency('XYZ')
        self.assertIsNone(c)

    def test_get_user_preferred_currency(self):
        pref = get_user_preferred_currency(self.user)
        self.assertEqual(pref.code, 'USD')

    def test_get_user_preferred_currency_inr(self):
        self.user.profile.preferred_currency = 'INR'
        self.user.profile.save()
        pref = get_user_preferred_currency(self.user)
        self.assertEqual(pref.code, 'INR')


# ═══════════════════════════════════════════════════════════════════
#  VIEW / INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════

class TransactionViewTest(FinanceTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_transaction_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('finance:transaction_list'))
        self.assertEqual(response.status_code, 302)

    def test_transaction_list_loads(self):
        response = self.client.get(reverse('finance:transaction_list'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_create_form_loads(self):
        response = self.client.get(reverse('finance:transaction_create'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_create_post(self):
        response = self.client.post(reverse('finance:transaction_create'), {
            'category': self.expense_cat.pk,
            'amount': '50.00',
            'currency': self.usd.pk,
            'date': '2026-02-10',
            'description': 'Test expense',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 1)

    def test_transaction_edit(self):
        tx = Transaction.objects.create(
            user=self.user, category=self.expense_cat,
            amount=Decimal('50.00'), currency=self.usd, date=date(2026, 2, 10))
        response = self.client.post(reverse('finance:transaction_edit', args=[tx.pk]), {
            'category': self.expense_cat.pk,
            'amount': '75.00',
            'currency': self.usd.pk,
            'date': '2026-02-10',
            'description': 'Updated',
        })
        self.assertEqual(response.status_code, 302)
        tx.refresh_from_db()
        self.assertEqual(tx.amount, Decimal('75.00'))

    def test_transaction_delete(self):
        tx = Transaction.objects.create(
            user=self.user, category=self.expense_cat,
            amount=Decimal('50.00'), currency=self.usd, date=date(2026, 2, 10))
        response = self.client.post(reverse('finance:transaction_delete', args=[tx.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=tx.pk).exists())

    def test_transaction_detail(self):
        tx = Transaction.objects.create(
            user=self.user, category=self.expense_cat,
            amount=Decimal('50.00'), currency=self.usd, date=date(2026, 2, 10))
        response = self.client.get(reverse('finance:transaction_detail', args=[tx.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '50.00')

    def test_other_users_transaction_not_accessible(self):
        tx = Transaction.objects.create(
            user=self.other_user, category=self.other_user_cat,
            amount=Decimal('50.00'), currency=self.usd, date=date(2026, 2, 10))
        response = self.client.get(reverse('finance:transaction_detail', args=[tx.pk]))
        self.assertEqual(response.status_code, 403)


class CategoryViewTest(FinanceTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_category_list_loads(self):
        response = self.client.get(reverse('finance:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Food')

    def test_category_create(self):
        response = self.client.post(reverse('finance:category_create'), {
            'name': 'Transport',
            'type': 'EXPENSE',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(user=self.user, name='Transport').exists())

    def test_category_delete_protected(self):
        Transaction.objects.create(
            user=self.user, category=self.expense_cat,
            amount=Decimal('50.00'), currency=self.usd, date=date(2026, 2, 10))
        response = self.client.post(reverse('finance:category_delete', args=[self.expense_cat.pk]))
        self.assertEqual(response.status_code, 302)
        # Category should still exist (protected)
        self.assertTrue(Category.objects.filter(pk=self.expense_cat.pk).exists())


class BudgetViewTest(FinanceTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_budget_list_loads(self):
        response = self.client.get(reverse('finance:budget_list'))
        self.assertEqual(response.status_code, 200)

    def test_budget_create(self):
        response = self.client.post(reverse('finance:budget_create'), {
            'category': self.expense_cat.pk,
            'limit_amount': '500.00',
            'month': '2026-02-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Budget.objects.filter(user=self.user, category=self.expense_cat).exists())


class NotificationViewTest(FinanceTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)
        self.notification = Notification.objects.create(
            user=self.user, message='Test notification',
            notification_type='BUDGET_WARNING')

    def test_notification_list_loads(self):
        response = self.client.get(reverse('finance:notification_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test notification')

    def test_mark_notification_read(self):
        response = self.client.post(reverse('finance:notification_mark_read',
                                            args=[self.notification.pk]))
        self.assertEqual(response.status_code, 302)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_clear_all_notifications(self):
        # Mark the notification as read first — clear_all deletes read notifications
        self.notification.is_read = True
        self.notification.save()
        response = self.client.post(reverse('finance:notification_clear_all'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notification.objects.filter(pk=self.notification.pk).exists())


class ImportViewTest(FinanceTestMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_import_page_loads(self):
        response = self.client.get(reverse('finance:import_statement'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload CSV or PDF')

    def test_sample_csv_download(self):
        response = self.client.get(reverse('finance:download_sample_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response['Content-Type'])
        self.assertIn('date,description,amount', response.content.decode())

    def test_csv_upload_preview(self):
        csv_content = (
            'date,description,amount\n'
            '2026-01-15,Grocery Store,45.99\n'
            '2026-01-16,Salary Deposit,5000.00\n'
        )
        from django.core.files.uploadedfile import SimpleUploadedFile
        csv_file = SimpleUploadedFile('test.csv', csv_content.encode(), content_type='text/csv')
        response = self.client.post(reverse('finance:import_statement'), {
            'file': csv_file,
            'currency': self.usd.pk,
            'date_format': '%Y-%m-%d',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Preview')
        self.assertContains(response, 'Total Rows')


# ═══════════════════════════════════════════════════════════════════
#  IMPORT SERVICE UNIT TESTS
# ═══════════════════════════════════════════════════════════════════

class ImportServiceTest(FinanceTestMixin, TestCase):

    def test_parse_csv_basic(self):
        from finance.import_service import parse_csv_statement
        csv_content = (
            'date,description,amount\n'
            '2026-01-15,Grocery Store,45.99\n'
            '2026-01-16,Salary Deposit,5000.00\n'
        )
        f = io.BytesIO(csv_content.encode('utf-8'))
        result = parse_csv_statement(f, self.user, currency_code='USD')
        self.assertEqual(result['total_rows'], 2)
        self.assertEqual(len(result['errors']), 0)

    def test_parse_csv_debit_credit_columns(self):
        from finance.import_service import parse_csv_statement
        csv_content = (
            'date,description,debit,credit\n'
            '2026-01-15,Grocery Store,45.99,\n'
            '2026-01-16,Salary,,5000.00\n'
        )
        f = io.BytesIO(csv_content.encode('utf-8'))
        result = parse_csv_statement(f, self.user, currency_code='USD')
        self.assertEqual(result['total_rows'], 2)

    def test_parse_csv_bad_date(self):
        from finance.import_service import parse_csv_statement
        csv_content = (
            'date,description,amount\n'
            'invalid-date,Test,45.99\n'
        )
        f = io.BytesIO(csv_content.encode('utf-8'))
        result = parse_csv_statement(f, self.user)
        self.assertEqual(result['total_rows'], 0)
        self.assertEqual(len(result['errors']), 1)

    def test_duplicate_detection(self):
        from finance.import_service import parse_csv_statement
        # Create an existing transaction
        Transaction.objects.create(
            user=self.user, category=self.expense_cat,
            amount=Decimal('45.99'), currency=self.usd,
            date=date(2026, 1, 15), description='Grocery Store')
        csv_content = (
            'date,description,amount\n'
            '2026-01-15,Grocery Store,45.99\n'
        )
        f = io.BytesIO(csv_content.encode('utf-8'))
        result = parse_csv_statement(f, self.user, currency_code='USD')
        self.assertEqual(result['duplicates'], 1)
        self.assertEqual(result['new_count'], 0)

    def test_import_transactions(self):
        from finance.import_service import import_transactions
        rows = [{
            'date': date(2026, 1, 15),
            'description': 'Test',
            'amount': Decimal('50.00'),
            'type': 'EXPENSE',
            'category': self.expense_cat,
            'is_duplicate': False,
            'is_uncategorized': False,
        }]
        result = import_transactions(self.user, rows, self.usd)
        self.assertEqual(result['imported'], 1)
        self.assertEqual(result['skipped'], 0)
        # Verify type was set
        tx = Transaction.objects.get(user=self.user, description='Test')
        self.assertEqual(tx.type, 'EXPENSE')

    def test_import_skips_duplicates(self):
        from finance.import_service import import_transactions
        rows = [{
            'date': date(2026, 1, 15),
            'description': 'Test',
            'amount': Decimal('50.00'),
            'type': 'EXPENSE',
            'category': self.expense_cat,
            'is_duplicate': True,
        }]
        result = import_transactions(self.user, rows, self.usd)
        self.assertEqual(result['imported'], 0)
        self.assertEqual(result['skipped'], 1)

    def test_fallback_category_created(self):
        from finance.import_service import _get_or_create_fallback_category
        cat = _get_or_create_fallback_category(self.user, 'EXPENSE')
        self.assertEqual(cat.name, 'Uncategorized')
        self.assertEqual(cat.type, 'EXPENSE')
        self.assertEqual(cat.user, self.user)
        # Should return existing on second call
        cat2 = _get_or_create_fallback_category(self.user, 'EXPENSE')
        self.assertEqual(cat.pk, cat2.pk)
