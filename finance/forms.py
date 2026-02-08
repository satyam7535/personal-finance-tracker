from django import forms
from .models import Transaction, Category, Currency, Budget


class TransactionForm(forms.ModelForm):
    """
    Form for creating/editing transactions.
    - `type` is excluded (auto-set from category)
    - Category choices filtered to current user in __init__
    """
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'currency', 'date', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional description...'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['currency'].queryset = Currency.objects.filter(is_active=True)

        # Better labels
        self.fields['category'].empty_label = '— Select Category —'
        self.fields['currency'].empty_label = '— Select Currency —'


class TransactionFilterForm(forms.Form):
    """Filter form for transaction list view."""
    TYPE_CHOICES = [('', 'All Types')] + Transaction.TYPE_CHOICES

    type = forms.ChoiceField(choices=TYPE_CHOICES, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label='All Categories'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)


class CategoryForm(forms.ModelForm):
    """Form to create/edit categories."""
    class Meta:
        model = Category
        fields = ['name', 'type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description...'}),
        }


class BudgetForm(forms.ModelForm):
    """Form to create/edit monthly budgets for expense categories."""
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'month']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
            'limit_amount': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Only expense categories can have budgets
            self.fields['category'].queryset = Category.objects.filter(
                user=user, type='EXPENSE'
            )
        self.fields['category'].empty_label = '— Select Expense Category —'

    def clean_month(self):
        """Normalize month to first day."""
        month = self.cleaned_data.get('month')
        if month:
            return month.replace(day=1)
        return month
