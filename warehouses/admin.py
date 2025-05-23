from django.contrib import admin
from .models import (
    Warehouse, Unit, UnitConversion, Category, Material, MaterialStock,
    Invoice, Customer, Supplier, SalesInvoice, PurchaseInvoice,
    SalesReturnInvoice, PurchaseReturnInvoice, InvoiceItem, MaterialMove
)

# Register your models here.

class MaterialStockInline(admin.TabularInline):
    model = MaterialStock
    extra = 1

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'unit', 'cost_price', 'selling_price', 'total_stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'barcode')
    inlines = [MaterialStockInline]

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

@admin.register(UnitConversion)
class UnitConversionAdmin(admin.ModelAdmin):
    list_display = ('from_unit', 'to_unit', 'conversion_factor')
    list_filter = ('from_unit', 'to_unit')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(MaterialStock)
class MaterialStockAdmin(admin.ModelAdmin):
    list_display = ('material', 'warehouse', 'quantity')
    list_filter = ('warehouse',)
    search_fields = ('material__name', 'material__code', 'warehouse__name')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_type', 'date', 'total_amount', 'payment_status')
    list_filter = ('invoice_type', 'payment_status', 'date')
    search_fields = ('invoice_number',)
    inlines = [InvoiceItemInline]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'email', 'phone')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_person', 'email', 'phone')

@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'customer', 'warehouse')
    list_filter = ('warehouse',)
    search_fields = ('invoice__invoice_number', 'customer__name')

@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'supplier', 'warehouse')
    list_filter = ('warehouse',)
    search_fields = ('invoice__invoice_number', 'supplier__name')

@admin.register(SalesReturnInvoice)
class SalesReturnInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'customer', 'original_invoice', 'warehouse')
    list_filter = ('warehouse',)
    search_fields = ('invoice__invoice_number', 'customer__name')

@admin.register(PurchaseReturnInvoice)
class PurchaseReturnInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'supplier', 'original_invoice', 'warehouse')
    list_filter = ('warehouse',)
    search_fields = ('invoice__invoice_number', 'supplier__name')

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'material', 'quantity', 'unit_price', 'total_price')
    list_filter = ('invoice__invoice_type',)
    search_fields = ('invoice__invoice_number', 'material__name', 'material__code')

@admin.register(MaterialMove)
class MaterialMoveAdmin(admin.ModelAdmin):
    list_display = ('material', 'source_warehouse', 'destination_warehouse', 'quantity', 'move_type', 'created_at')
    list_filter = ('move_type', 'source_warehouse', 'destination_warehouse')
    search_fields = ('material__name', 'material__code', 'reference_invoice__invoice_number')
