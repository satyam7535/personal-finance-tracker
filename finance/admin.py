from django.contrib import admin
from .models import Currency, Category, Transaction, Budget


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'exchange_rate_to_usd', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'user__username')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'category', 'amount', 'currency', 'date', 'created_at')
    list_filter = ('type', 'currency', 'date')
    search_fields = ('description', 'user__username', 'category__name')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'limit_amount', 'month', 'created_at')
    list_filter = ('month',)
    search_fields = ('user__username', 'category__name')
