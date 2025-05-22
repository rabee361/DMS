from typing import override
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from hr_tool.models import *
from django.views import View
import json

# Create your views here.

class FinanceView(View):
    def get(self, request):
        total_accounts = Account.objects.count()
        total_currencies = Currency.objects.count()
        total_exchanges = ExchangePrice.objects.count()
        total_expenses = Expense.objects.count()
        total_salaries = SalaryBlock.objects.count()
        total_loans = Loan.objects.count()
        total_account_movements = AccountMovement.objects.count()
        context = { 
            'total_accounts': total_accounts,
            'total_currencies': total_currencies,
            'total_exchanges': total_exchanges,
            'total_loans': total_loans,
            'total_expenses': total_expenses,
            'total_salaries': total_salaries,
            'total_account_movements': total_account_movements
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
    pk_url_kwarg = 'id'
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
    pk_url_kwarg = 'id'
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
    pk_url_kwarg = 'id'
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




# ------------------ Expense Views ------------------

@method_decorator(login_required, name='dispatch')
class ListExpensesView(ListView):
    model = Expense
    template_name = 'finance/expenses/expenses.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateExpenseView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expenses/expense_form.html'
    success_url = reverse_lazy('expenses')

@method_decorator(login_required, name='dispatch')
class UpdateExpenseView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expenses/expense_form.html'
    success_url = reverse_lazy('expenses')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class DeletEexpenseView(DeleteView):
    model = Expense
    template_name = 'finance/expenses/delete_expense.html'
    context_object_name = 'expense'
    success_url = reverse_lazy('expenses')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class ExpenseActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        expenses = Expense.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            expenses.delete()

        return redirect('expenses')



# ------------------ Loan Views ------------------

@method_decorator(login_required, name='dispatch')
class ListLoansView(ListView):
    model = Loan
    template_name = 'finance/loans/loans.html'
    context_object_name = 'loans'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateLoanView(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'finance/loans/loan_form.html'
    success_url = reverse_lazy('loans')

@method_decorator(login_required, name='dispatch')
class UpdateLoanView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'finance/loans/loan_form.html'
    success_url = reverse_lazy('loans')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class DeleteLoanView(DeleteView):
    model = Loan
    template_name = 'finance/loans/delete_loan.html'
    context_object_name = 'loan'
    success_url = reverse_lazy('loans')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class LoanActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        loans = Loan.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            loans.delete()

        return redirect('loans')






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
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        employees = Employee.objects.all().prefetch_related(
            'additiondiscount_set',
            'holiday_set',
            'extrawork_set',
            'hrloan_set'
        )
        employee_data = []
        
        for employee in employees:
            additions_discounts = employee.additiondiscount_set.all()
            holidays = employee.holiday_set.all()
            extras = employee.extrawork_set.all()
            hr_loans = employee.hrloan_set.all()
            
            # Calculate extras
            extra_work_value = sum((extra.total_extra_work_value or 0) for extra in extras)
            
            # Calculate additions and discounts
            additions = sum(ad.value for ad in additions_discounts if ad.type == 'إضافة')
            discounts = sum(ad.value for ad in additions_discounts if ad.type == 'خصم')
            
            # Calculate holiday discounts
            holiday_discounts = sum(holiday.holiday_discount for holiday in holidays if not holiday.paid)
            
            # Calculate loan discounts
            loan_discounts = sum(loan.discount_amount for loan in hr_loans)
            
            # Total calculations
            total_additions = extra_work_value + additions
            total_discounts = discounts + holiday_discounts + loan_discounts
            total_salary = employee.base_salary + total_additions - total_discounts
            
            employee_data.append({
                'employee': employee,
                'additions_discounts': additions_discounts,
                'holidays': holidays,
                'extras': extras,
                'hr_loans': hr_loans,
                'total_extra_work_value': extra_work_value,
                'total_additions': total_additions,
                'total_discounts': total_discounts,
                'total_salary': total_salary
            })

        return render(request, 'finance/salaries/salaries.html', {
            'employee_data': employee_data,
            'start_date': start_date,
            'end_date': end_date,
        })

    def post(self, request):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        submit_btn = request.POST.get('submit_btn', '')

        if 'صرف الرواتب' in submit_btn:
            # try:
            employees = Employee.objects.all().prefetch_related(
                'additiondiscount_set',
                'holiday_set',
                'extrawork_set',
                'hrloan_set'
            )
            
            for employee in employees:
                # Calculate net salary
                base_salary = employee.base_salary or 0
                
                # Get related data within date range
                additions_discounts = employee.additiondiscount_set.filter(
                    created__range=[start_date, end_date]
                )
                holidays = employee.holiday_set.filter(
                    start__range=[start_date, end_date]
                )
                extras = employee.extrawork_set.filter(
                    start__range=[start_date, end_date]
                )
                hr_loans = employee.hrloan_set.filter(
                    created__range=[start_date, end_date]
                )
                
                # Calculate additions
                total_additions = sum(extra.total_extra_work_value or 0 for extra in extras)
                total_additions += sum(ad.value for ad in additions_discounts if ad.type == "إضافة")
                
                # Calculate deductions
                total_deductions = sum(holiday.holiday_discount or 0 for holiday in holidays if not holiday.paid)
                total_deductions += sum(loan.discount_amount or 0 for loan in hr_loans)
                total_deductions += sum(ad.value for ad in additions_discounts if ad.type == "خصم")
                
                # Calculate final salary
                final_salary = base_salary + total_additions - total_deductions
                
                # Create salary block
                salary_block = SalaryBlock.objects.create(
                    employee=employee,
                    amount=final_salary,
                )
                
                # Create entries
                entry_id = SalaryBlockEntry.objects.create(
                    salary_block=salary_block,
                    name="الراتب الأساسي",
                    amount=base_salary
                )
                if entry_id:
                    AccountMovement.objects.create(
                        from_account=employee.account,
                        to_account=employee.opposite_account,
                        amount=base_salary,
                        origin_type="صرف راتب الموظف",
                        currency=employee.salary_currency,
                        origin_id=entry_id
                    )
                
                
                if total_additions > 0:
                    entry_id = SalaryBlockEntry.objects.create(
                        salary_block=salary_block,
                        name="إجمالي الإضافات",
                        amount=total_additions
                    )
                    if entry_id:
                        AccountMovement.objects.create(
                            from_account=employee.account,
                            to_account=employee.opposite_account,
                            amount=total_additions,
                            origin_type="صرف اضافات الموظف",
                            currency=employee.salary_currency,
                            origin_id=entry_id
                        )
                
                if total_deductions > 0:
                    entry_id = SalaryBlockEntry.objects.create(
                        salary_block=salary_block,
                        name="إجمالي الخصومات",
                        amount=-total_deductions
                    )
                    if entry_id:
                        AccountMovement.objects.create(
                            from_account=employee.account,
                            to_account=employee.opposite_account,
                            amount=total_deductions,
                            origin_type="صرف خصومات الموظف",
                            currency=employee.salary_currency,
                            origin_id=entry_id
                        )
            messages.success(request, 'تم صرف الرواتب بنجاح')
            # except Exception as e:
            #     messages.error(request, f'حدث خطأ أثناء صرف الرواتب: {str(e)}')
        
        # Always redirect back to salaries page with date parameters
        return redirect(f'{reverse_lazy("salaries")}?start_date={start_date}&end_date={end_date}')


@method_decorator(login_required, name='dispatch')
class CalculateSalariesHtmxView(View):
    """Handle HTMX request to calculate salaries based on date range"""
    
    def post(self, request):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Here you would implement the actual salary calculation logic
        # based on the date range parameters
        
        # For now we'll just fetch employees and return them
        # (replace with actual calculation logic in a real implementation)
        employees = Employee.objects.all()
        
        # This will return just the employee list part to replace the content
        # via HTMX's hx-target="#departmentsTree"
        return render(request, 'finance/salaries/partials/employee_list.html', {
            'employees': employees,
            'start_date': start_date,
            'end_date': end_date
        })



@method_decorator(login_required, name='dispatch')
class ListAccountMovementsView(ListView):
    model = AccountMovement
    template_name = 'finance/movement/account_moves.html'
    context_object_name = 'account_movements'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(description__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateAccountMovementView(CreateView):
    model = AccountMovement
    form_class = AccountMovementForm
    template_name = 'finance/movement/account_move_form.html'
    success_url = reverse_lazy('account_movements')

@method_decorator(login_required, name='dispatch')
class UpdateAccountMovementView(UpdateView):
    model = AccountMovement
    form_class = AccountMovementForm
    template_name = 'finance/movement/account_move_form.html'
    success_url = reverse_lazy('account_movements')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class DeleteAccountMovementView(DeleteView):
    model = AccountMovement
    template_name = 'finance/movement/delete_account_move.html'
    context_object_name = 'account_movement'
    success_url = reverse_lazy('account_movements')
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class AccountMovementActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        account_movements = AccountMovement.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            account_movements.delete()

        return redirect('account_movements')


