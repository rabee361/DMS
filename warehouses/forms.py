from django import forms
from .models import (
    Warehouse, Unit, UnitConversion, Category, Material, MaterialStock,
    Invoice, Customer, Supplier, SalesInvoice, PurchaseInvoice,
    SalesReturnInvoice, PurchaseReturnInvoice, InvoiceItem, MaterialMove
)
from django.forms import inlineformset_factory


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'code', 'location', 'region', 'warehouse_type', 'description',
                  'capacity', 'status', 'manager', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'سيتم إنشاؤه تلقائياً إذا تُرك فارغاً'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'warehouse_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'symbol', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class UnitConversionForm(forms.ModelForm):
    class Meta:
        model = UnitConversion
        fields = ['from_unit', 'to_unit', 'conversion_factor']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'name', 'code', 'barcode', 'description', 'category',
            'unit', 'cost_price', 'selling_price', 'min_stock_level', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class MaterialStockForm(forms.ModelForm):
    class Meta:
        model = MaterialStock
        fields = ['material', 'warehouse', 'quantity']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'date', 'notes', 'payment_status']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
        }


class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ['customer', 'warehouse']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = PurchaseInvoice
        fields = ['supplier', 'warehouse']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class SalesReturnInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesReturnInvoice
        fields = ['customer', 'original_invoice', 'warehouse']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'original_invoice': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class PurchaseReturnInvoiceForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturnInvoice
        fields = ['supplier', 'original_invoice', 'warehouse']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'original_invoice': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['material', 'quantity', 'unit_price']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


class MaterialMoveForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        required=False,
        label='المستودع',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = MaterialMove
        fields = [
            'material', 'source_warehouse', 'destination_warehouse',
            'quantity', 'reference_invoice', 'notes'
        ]
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'source_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'destination_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'reference_invoice': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Create formsets for invoice items
InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)
