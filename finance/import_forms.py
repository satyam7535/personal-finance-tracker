import csv
from django import forms
from .models import Currency


class BankStatementForm(forms.Form):
    """Form for uploading bank statement CSV or PDF files."""
    file = forms.FileField(
        label='Bank Statement File',
        help_text='Upload a CSV or PDF bank statement',
        widget=forms.ClearableFileInput(attrs={'accept': '.csv,.pdf'}),
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        label='Currency',
        help_text='Currency of the transactions in the file',
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
        help_text='Select the date format used in your file',
    )

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            name_lower = f.name.lower()
            if not (name_lower.endswith('.csv') or name_lower.endswith('.pdf')):
                raise forms.ValidationError('Only CSV and PDF files are allowed.')
            if f.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError('File size must be under 10 MB.')
        return f
