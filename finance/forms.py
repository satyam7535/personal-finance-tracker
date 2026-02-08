from django import forms
from .models import Transaction, Category, Currency


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
