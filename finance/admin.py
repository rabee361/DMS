from django.contrib import admin
from .models import *


admin.site.register(Currency)
admin.site.register(ExchangePrice)
admin.site.register(Account)
admin.site.register(AccountMovement)
admin.site.register(SalaryBlock)
admin.site.register(SalaryBlockEntry)
admin.site.register(Loan)
admin.site.register(LoanPayment)
admin.site.register(Expense)

