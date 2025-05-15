# from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model() 

# # Create your models here.


# class INVOICE_TYPES(models.TextChoices):
#     SELL = 'مبيع'
#     BUY = 'شراء'
#     SELL_RETURN = 'مرتجع مبيع'
#     BUY_RETURN = 'مرتجع شراء'
#     INPUT = 'ادخال'
#     OUTPUT = 'اخراج'


# class Material(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     current_stock = models.DecimalField(max_digits=10, decimal_places=2)
#     unit = models.ForeignKey('Unit', on_delete=models.CASCADE)


# class MaterialMove(models.Model):
#     source_warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='source_warehouse')
#     source_warehouse_entry = models.IntegerField(default=0)
#     destination_warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='destination_warehouse')
#     destination_warehouse_entry = models.IntegerField(default=0)
#     material = models.ForeignKey('Material', on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)
#     move_date = models.DateTimeField(auto_now_add=True)


# class Warehouse(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     location = models.CharField(max_length=255)
#     capacity = models.DecimalField(max_digits=10, decimal_places=2)
#     capacity_unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
#     manager = models.ForeignKey('User', on_delete=models.CASCADE)
#     current_stock = models.DecimalField(max_digits=10, decimal_places=2)




# class Unit(models.Model):
#     name = models.CharField(max_length=255)


# class UnitConversion(models.Model):
#     unit1 = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='unit1')
#     unit2 = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='unit2')
#     conversion_factor = models.DecimalField(max_digits=10, decimal_places=2)


# class Client(models.Model):
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=20, choices=(('CLIENT', 'cleint'), ('SUPPLIER', 'supplier')))
#     phone = models.IntegerField(max_length=255)
#     phone2 = models.IntegerField(max_length=255)
#     email = models.EmailField()
#     address = models.CharField(max_length=255)


# class InvoiceMaterials(models.Model):
#     material = models.ForeignKey('Material', on_delete=models.CASCADE)
#     invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)



# class Invoice(models.Model):
#     client = models.ForeignKey('Client', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
#     date = models.DateField(auto_now_add=True)


