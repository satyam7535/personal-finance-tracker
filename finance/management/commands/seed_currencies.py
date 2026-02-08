from django.core.management.base import BaseCommand
from finance.models import Currency
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed the database with common currencies and exchange rates.'

    def handle(self, *args, **options):
        currencies = [
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$', 'exchange_rate_to_usd': Decimal('1.000000')},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'exchange_rate_to_usd': Decimal('1.080000')},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£', 'exchange_rate_to_usd': Decimal('1.260000')},
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹', 'exchange_rate_to_usd': Decimal('0.012000')},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥', 'exchange_rate_to_usd': Decimal('0.006700')},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': 'A$', 'exchange_rate_to_usd': Decimal('0.650000')},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': 'C$', 'exchange_rate_to_usd': Decimal('0.740000')},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF', 'exchange_rate_to_usd': Decimal('1.120000')},
            {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥', 'exchange_rate_to_usd': Decimal('0.140000')},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': 'S$', 'exchange_rate_to_usd': Decimal('0.750000')},
        ]

        created_count = 0
        for data in currencies:
            _, created = Currency.objects.update_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done: {created_count} currencies created, '
                f'{len(currencies) - created_count} updated.'
            )
        )
