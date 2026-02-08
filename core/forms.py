from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from finance.models import Currency


class UserRegistrationForm(UserCreationForm):
    """Registration form with email field."""
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class UserUpdateForm(forms.ModelForm):
    """Form to update user's basic info."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Exclude the current user from the uniqueness check
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class UserProfileForm(forms.ModelForm):
    """Form to update profile preferences."""
    preferred_currency = forms.ChoiceField(choices=[])

    class Meta:
        model = UserProfile
        fields = ['preferred_currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate from Currency table
        self.fields['preferred_currency'].choices = [
            (c.code, f"{c.code} - {c.name}")
            for c in Currency.objects.filter(is_active=True).order_by('code')
        ]
