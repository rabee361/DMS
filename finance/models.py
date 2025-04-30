from django.db import models
from hr_tool.models import Employee

# Create your models here.



class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    parts = models.CharField(max_length=50, null=True, blank=True)
    parts_relation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Salary(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.employee.username}-{self.amount}'
    



# class UpfrontPayment(models.Model):
#     pass


