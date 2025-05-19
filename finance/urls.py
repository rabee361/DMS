# pr_tool/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.FinanceView.as_view(), name="finance"),

    path('currencies/', views.ListCurrenciesView.as_view(), name="currencies"),
    path('currencies/add', views.CreateCurrencyView.as_view(), name="create_currency"),
    path('currencies/<int:pk>/', views.UpdateCurrencyView.as_view(), name="currency_info"),
    path('currencies/delete/<int:id>/', views.DeleteCurrencyView.as_view(), name="delete_currency"),
    path('currencies/action', views.CurrencyActionView.as_view(), name="currencies_action"),

    path('exchanges/', views.ListExchangesView.as_view(), name="exchanges"),
    path('exchanges/add', views.CreateExchangeView.as_view(), name="create_exchange"),
    path('exchanges/<int:id>/', views.UpdateExchangeView.as_view(), name="exchange_info"),
    path('exchanges/delete/<int:id>/', views.DeleteExchangeView.as_view(), name="delete_exchange"),
    path('exchanges/action/', views.ExchangeActionView.as_view(), name="exchanges_action"),

    path('accounts/', views.ListAccountsView.as_view(), name="accounts"),
    path('accounts/add', views.CreateAccountView.as_view(), name="create_account"),
    path('accounts/<int:id>/', views.UpdateAccountView.as_view(), name="account_info"),
    path('accounts/delete/<int:id>/', views.DeleteAccountView.as_view(), name="delete_account"),
    path('accounts/action/', views.AccountActionView.as_view(), name="accounts_action"),

    path('expenses/', views.ListExpensesView.as_view(), name="expenses"),
    path('expenses/add', views.CreateExpenseView.as_view(), name="create_expense"),
    path('expenses/<int:id>/', views.UpdateExpenseView.as_view(), name="expense_info"),
    path('expenses/delete/<int:id>/', views.DeletEexpenseView.as_view(), name="delete_expense"),
    path('expenses/action/', views.ExpenseActionView.as_view(), name="expenses_action"),

    path('loans/', views.ListLoansView.as_view(), name="loans"),
    path('loans/add', views.CreateLoanView.as_view(), name="create_loan"),
    path('loans/<int:id>/', views.UpdateLoanView.as_view(), name="loan_info"),
    path('loans/delete/<int:id>/', views.DeleteLoanView.as_view(), name="delete_loan"),
    path('loans/action/', views.LoanActionView.as_view(), name="loans_action"),

    path('account_movements/', views.ListAccountMovementsView.as_view(), name="account_movements"),
    path('account_movements/add', views.CreateAccountMovementView.as_view(), name="create_account_movement"),
    path('account_movements/<int:id>/', views.UpdateAccountMovementView.as_view(), name="account_movement_info"),
    path('account_movements/delete/<int:id>/', views.DeleteAccountMovementView.as_view(), name="delete_account_movement"),
    path('account_movements/action/', views.AccountMovementActionView.as_view(), name="account_movements_action"),

    path('salaries/', views.CalculateSalaryView.as_view(), name="salaries"),
    path('salaries/add', views.CreateSalaryView.as_view(), name="create_salary"),
    path('salaries/calculate/', views.CalculateSalariesHtmxView.as_view(), name="calculate_salaries"),
]
