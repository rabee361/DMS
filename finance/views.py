from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.views import View
import json

# Create your views here.

class FinanceView(View):
    def get(self, request):
        total_accounts = Account.objects.count()
        total_currencies = Currency.objects.count()
        total_exchanges = ExchangePrice.objects.count()
        context = { 
            'total_accounts': total_accounts,
            'total_currencies': total_currencies,
            'total_exchanges': total_exchanges
        }
        return render(request, 'finance/finance.html', context)

# ------------------ Currency Views ------------------

@method_decorator(login_required, name='dispatch')
class ListCurrenciesView(ListView):
    model = Currency
    template_name = 'finance/currencies/currencies.html'
    context_object_name = 'currencies'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateCurrencyView(CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'finance/currencies/currency_form.html'
    success_url = reverse_lazy('currencies')

@method_decorator(login_required, name='dispatch')
class UpdateCurrencyView(UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = 'finance/currencies/currency_form.html'
    success_url = reverse_lazy('currencies')

@method_decorator(login_required, name='dispatch')
class DeleteCurrencyView(DeleteView):
    model = Currency
    template_name = 'finance/salary/delete_currency.html'
    context_object_name = 'currency'
    success_url = reverse_lazy('currencies')

@method_decorator(login_required, name='dispatch')
class CurrencyActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        currencies = Currency.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            currencies.delete()

        return redirect('currencies')

# ------------------ ExchangePrice Views ------------------

@method_decorator(login_required, name='dispatch')
class ListExchangesView(ListView):
    model = ExchangePrice
    template_name = 'finance/exchanges/exchanges.html'
    context_object_name = 'exchanges'
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class CreateExchangeView(CreateView):
    model = ExchangePrice
    form_class = ExchangePriceForm
    template_name = 'finance/exchanges/exchange_form.html'
    success_url = reverse_lazy('exchanges')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['first_currency'].queryset = Currency.objects.all()
        form.fields['second_currency'].queryset = Currency.objects.all()
        return form

@method_decorator(login_required, name='dispatch')
class UpdateExchangeView(UpdateView):
    model = ExchangePrice
    form_class = ExchangePriceForm
    template_name = 'finance/exchanges/exchange_form.html'
    success_url = reverse_lazy('exchanges')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['first_currency'].queryset = Currency.objects.all()
        form.fields['second_currency'].queryset = Currency.objects.all()
        return form

@method_decorator(login_required, name='dispatch')
class DeleteExchangeView(DeleteView):
    model = ExchangePrice
    template_name = 'finance/exchanges/delete_exchange.html'
    context_object_name = 'exchange'
    success_url = reverse_lazy('exchanges')

@method_decorator(login_required, name='dispatch')
class ExchangeActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        exchanges = ExchangePrice.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            exchanges.delete()

        return redirect('exchanges')

# ------------------ Account Views ------------------

@method_decorator(login_required, name='dispatch')
class ListAccountsView(ListView):
    model = Account
    template_name = 'finance/accounts/accounts.html'
    context_object_name = 'accounts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateAccountView(CreateView):
    model = Account
    fields = '__all__'
    template_name = 'finance/accounts/account_form.html'
    success_url = reverse_lazy('accounts')

@method_decorator(login_required, name='dispatch')
class UpdateAccountView(UpdateView):
    model = Account
    fields = '__all__'
    template_name = 'finance/accounts/account_form.html'
    success_url = reverse_lazy('accounts')

@method_decorator(login_required, name='dispatch')
class DeleteAccountView(DeleteView):
    model = Account
    template_name = 'finance/accounts/delete_account.html'
    context_object_name = 'account'
    success_url = reverse_lazy('accounts')

@method_decorator(login_required, name='dispatch')
class AccountActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        accounts = Account.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            accounts.delete()

        return redirect('accounts')



# ------------------ Salary Views ------------------

@method_decorator(login_required, name='dispatch')
class ListSalariesView(ListView):
    model = SalaryBlock
    template_name = 'finance/salaries/salaries.html'
    context_object_name = 'salaries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateSalaryView(View):
    def post(self, request):
        pass


@method_decorator(login_required, name='dispatch')
class CalculateSalaryView(View):
    def get(self, request):
        return render(request, 'finance/salaries/salaries.html')

