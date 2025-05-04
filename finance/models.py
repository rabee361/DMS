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
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_currency.name}-{self.second_currency.name}-{self.price}'



class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
