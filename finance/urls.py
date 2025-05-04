# pr_tool/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.FinanceView.as_view(), name="finance"),

    path('currencies/', views.ListCurrenciesView.as_view(), name="currencies"),
    path('currencies/add', views.CreateCurrencyView.as_view(), name="create_currency"),
    path('currencies/<int:id>/', views.UpdateCurrencyView.as_view(), name="currency_info"),
    path('currencies/delete/<int:id>/', views.DeleteCurrencyView.as_view(), name="delete_currency"),
    path('currencies/action', views.CurrencyActionView.as_view(), name="currencies_action"),

    path('exchanges/', views.ListExchangesView.as_view(), name="exchanges"),
    path('exchanges/add', views.CreateExchangeView.as_view(), name="create_exchange"),
    path('exchanges/<int:id>/', views.UpdateExchangeView.as_view(), name="exchange_info"),
    path('exchanges/delete/<int:id>/', views.DeleteExchangeView.as_view(), name="delete_exchange"),
    path('exchanges/action/', views.ExchangeActionView.as_view(), name="exchange_action"),

    path('accounts/', views.ListAccountsView.as_view(), name="accounts"),
    path('accounts/add', views.CreateAccountView.as_view(), name="create_account"),
    path('accounts/<int:id>/', views.UpdateAccountView.as_view(), name="account_info"),
    path('accounts/delete/<int:id>/', views.DeleteAccountView.as_view(), name="delete_account"),
    path('accounts/action/', views.AccountActionView.as_view(), name="accounts_action"),
]
