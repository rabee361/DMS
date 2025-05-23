from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Warehouse(models.Model):
    """Model for warehouses/storage locations"""
    WAREHOUSE_TYPES = (
        ('main', 'رئيسي'),
        ('branch', 'فرعي'),
        ('factory', 'مصنع'),
        ('distribution', 'توزيع'),
        ('temporary', 'مؤقت'),
    )

    REGIONS = (
        ('central', 'المنطقة الوسطى'),
        ('eastern', 'المنطقة الشرقية'),
        ('western', 'المنطقة الغربية'),
        ('northern', 'المنطقة الشمالية'),
        ('southern', 'المنطقة الجنوبية'),
    )

    STATUS_CHOICES = (
        ('active', 'نشط'),
        ('inactive', 'غير نشط'),
        ('maintenance', 'قيد الصيانة'),
        ('full', 'ممتلئ'),
    )

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True, help_text="Warehouse code (auto-generated if empty)")
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=20, choices=REGIONS, default='central')
    description = models.TextField(blank=True, null=True)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES, default='main')
    capacity = models.DecimalField(max_digits=10, decimal_places=2, default=1000,help_text="Maximum storage capacity in cubic meters")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    manager = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_warehouse_type_display()})"

    def save(self, *args, **kwargs):
        # Auto-generate warehouse code if not provided
        if not self.code:
            # Get the last warehouse ID and increment by 1
            last_id = Warehouse.objects.order_by('-id').first()
            next_id = 1 if not last_id else last_id.id + 1
            self.code = f"WH-{next_id:03d}"
        super().save(*args, **kwargs)

    @property
    def total_items(self):
        """Get the total number of different items in this warehouse"""
        return self.materialstock_set.count()

    @property
    def total_quantity(self):
        """Get the total quantity of all items in this warehouse"""
        from django.db.models import Sum
        result = self.materialstock_set.aggregate(Sum('quantity'))
        return result['quantity__sum'] or 0

    @property
    def capacity_usage(self):
        """Calculate the capacity usage as a percentage"""
        # For realistic calculation, we use the total quantity relative to capacity
        # This is a simplified calculation - in a real system you might calculate based on volume
        if self.capacity > 0:
            usage = (self.total_quantity / self.capacity) * 100
            return min(100, round(usage, 1))  # Cap at 100%
        return 0

    @property
    def low_stock_count(self):
        """Count materials with quantity less than min_stock_level"""
        from django.db.models import F
        return self.materialstock_set.filter(
            quantity__lt=F('material__min_stock_level'),
            quantity__gt=0  # Only count items that are not completely out of stock
        ).count()

    @property
    def out_of_stock_count(self):
        """Count materials that are out of stock"""
        return self.materialstock_set.filter(quantity__lte=0).count()

    @property
    def total_value(self):
        """Calculate the total value of all items in this warehouse"""
        from django.db.models import F, Sum, ExpressionWrapper, DecimalField
        result = self.materialstock_set.annotate(
            item_value=ExpressionWrapper(
                F('quantity') * F('material__cost_price'),
                output_field=DecimalField()
            )
        ).aggregate(Sum('item_value'))
        return result['item_value__sum'] or 0


class Unit(models.Model):
    """Model for units of measurement"""
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class UnitConversion(models.Model):
    """Model for converting between different units"""
    from_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='from_conversions')
    to_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='to_conversions')
    conversion_factor = models.FloatField(validators=[MinValueValidator(0.0001)])

    class Meta:
        unique_together = ('from_unit', 'to_unit')

    def __str__(self):
        return f"1 {self.from_unit.symbol} = {self.conversion_factor} {self.to_unit.symbol}"


class Category(models.Model):
    """Model for material categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Material(models.Model):
    """Model for materials/products"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    min_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def total_stock(self):
        """Calculate total stock across all warehouses"""
        from django.db.models import Sum
        stock = MaterialStock.objects.filter(material=self).aggregate(Sum('quantity'))
        return stock['quantity__sum'] or 0


class MaterialStock(models.Model):
    """Model for tracking material stock in each warehouse"""
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('material', 'warehouse')

    def __str__(self):
        return f"{self.material.name} in {self.warehouse.name}: {self.quantity} {self.material.unit.symbol}"


class Invoice(models.Model):
    """Base model for all invoice types"""
    INVOICE_TYPES = (
        ('sales', 'Sales Invoice'),
        ('purchase', 'Purchase Invoice'),
        ('sales_return', 'Sales Return Invoice'),
        ('purchase_return', 'Purchase Return Invoice'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_invoice_type_display()} #{self.invoice_number}"


class Customer(models.Model):
    """Model for customers"""
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Model for suppliers"""
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SalesInvoice(models.Model):
    """Model for sales invoices (outgoing goods)"""
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)

    def __str__(self):
        return f"Sales Invoice #{self.invoice.invoice_number}"


class PurchaseInvoice(models.Model):
    """Model for purchase invoices (incoming goods)"""
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)

    def __str__(self):
        return f"Purchase Invoice #{self.invoice.invoice_number}"


class SalesReturnInvoice(models.Model):
    """Model for sales return invoices (goods returned by customers)"""
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    original_invoice = models.ForeignKey(SalesInvoice, on_delete=models.PROTECT, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)

    def __str__(self):
        return f"Sales Return Invoice #{self.invoice.invoice_number}"


class PurchaseReturnInvoice(models.Model):
    """Model for purchase return invoices (goods returned to suppliers)"""
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    original_invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.PROTECT, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)

    def __str__(self):
        return f"Purchase Return Invoice #{self.invoice.invoice_number}"


class InvoiceItem(models.Model):
    """Model for invoice line items"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.material.name} - {self.quantity} {self.material.unit.symbol}"

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class MaterialMove(models.Model):
    """Model for tracking material movements"""
    MOVE_TYPES = (
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('return_in', 'Return In'),
        ('return_out', 'Return Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    )

    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='source_moves', null=True, blank=True)
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='destination_moves', null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    move_type = models.CharField(max_length=20, choices=MOVE_TYPES)
    reference_invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.move_type == 'transfer':
            return f"{self.material.name}: {self.source_warehouse.name} → {self.destination_warehouse.name} ({self.quantity} {self.material.unit.symbol})"
        elif self.move_type in ['sale', 'return_out']:
            return f"{self.material.name}: {self.source_warehouse.name} → Customer ({self.quantity} {self.material.unit.symbol})"
        elif self.move_type in ['purchase', 'return_in']:
            return f"{self.material.name}: Supplier → {self.destination_warehouse.name} ({self.quantity} {self.material.unit.symbol})"
        else:
            return f"{self.material.name}: Adjustment in {self.source_warehouse or self.destination_warehouse} ({self.quantity} {self.material.unit.symbol})"

