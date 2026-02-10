import csv
from django import forms
from .models import Currency


class BankStatementForm(forms.Form):
    """Form for uploading bank statement CSV files."""
    file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: date, description, amount (or debit/credit)',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'}),
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        label='Currency',
        help_text='Currency of the transactions in the CSV',
    )
    date_format = forms.ChoiceField(
        choices=[
            ('%Y-%m-%d', 'YYYY-MM-DD (2026-01-15)'),
            ('%d/%m/%Y', 'DD/MM/YYYY (15/01/2026)'),
            ('%m/%d/%Y', 'MM/DD/YYYY (01/15/2026)'),
            ('%d-%m-%Y', 'DD-MM-YYYY (15-01-2026)'),
            ('%d %b %Y', 'DD Mon YYYY (15 Jan 2026)'),
        ],
        initial='%Y-%m-%d',
        label='Date Format',
        help_text='Select the date format used in your CSV',
    )

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            if not f.name.endswith('.csv'):
                raise forms.ValidationError('Only CSV files are allowed.')
            if f.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('File size must be under 10 MB.')
        return f
