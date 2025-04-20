from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django import forms


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self
        ]))

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})


class SignupForm(CustomUserCreationForm):
    income = forms.DecimalField(
        label="What’s your monthly income?",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 3000',
            'class': 'form-control',
            'step': '100'
        })
    )
    expenses = forms.DecimalField(
        label="What are your monthly expenses?",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 1200',
            'class': 'form-control',
            'step': '50'
        })
    )
    budget = forms.DecimalField(
        label="What’s your starting budget?",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 500',
            'class': 'form-control',
            'step': '20'
        })
    )
    goals = forms.CharField(
        label="What are your current financial goals?",
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'e.g. Pay off student loans, save for a trip, build emergency fund...',
            'class': 'form-control',
            'rows': 3
        })
    )
    categories = forms.CharField(
        label="What categories do you spend money on?",
        help_text="Separate with commas (e.g. Food, Rent, Fun)",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Rent, Groceries, Entertainment',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'income', 'expenses', 'budget', 'goals', 'categories']

