from django.db import models
# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    parts = models.CharField(max_length=50, null=True, blank=True)
    parts_relation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class ExchangePrice(models.Model):
    first_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='first_currency')
    second_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='second_currency')
    price = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.first_currency.name}-{self.second_currency.name}-{self.price}'


class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class AccountMovement(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_account')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_account')
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.from_account.name}-{self.to_account.name}-{self.amount}-{self.date}'




def get_employee_model():
    from hr_tool.models import Employee
    return Employee


class SalaryBlock(models.Model):
    employee = models.ForeignKey(
        'hr_tool.Employee',  # Use string reference to avoid circular import
        on_delete=models.CASCADE
    )
    amount = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Import Employee only when needed to avoid circular import
        return f'{self.employee.name}-{self.amount}-{self.date}'


class SalaryBlockEntry(models.Model):
    salary_block = models.ForeignKey(SalaryBlock, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.salary_block.employee.name}-{self.name}-{self.amount}'
