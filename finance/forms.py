from django import forms
from .models import *


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'

class ExchangePriceForm(forms.ModelForm):
    class Meta:
        model = ExchangePrice
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit)
        # Call create_movement after saving the expense
        create_movement(instance.account, instance.opposite_account, instance.amount, instance.currency, 'قرض', instance.id)
        return instance


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

from utility.account import create_movement

class ExpenseForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit)
        # Call create_movement after saving the expense
        create_movement(instance.account, instance.opposite_account, instance.amount, instance.currency, 'مصروف', instance.id)
        return instance


class AccountMovementForm(forms.ModelForm):
    class Meta:
        model = AccountMovement
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

