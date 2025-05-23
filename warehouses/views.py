from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, F, Q, ExpressionWrapper, DecimalField, Count, Case, When, Value
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils import timezone
import json
from datetime import datetime, timedelta
import csv
from collections import defaultdict

from .models import (
    Material, Category, Unit, UnitConversion, Warehouse, MaterialStock,
    Customer, Supplier, Invoice, SalesInvoice, PurchaseInvoice,
    SalesReturnInvoice, PurchaseReturnInvoice, InvoiceItem, MaterialMove
)
from .forms import (
    MaterialForm, CategoryForm, UnitForm, WarehouseForm, CustomerForm,
    SupplierForm, InvoiceForm, SalesInvoiceForm, PurchaseInvoiceForm,
    SalesReturnInvoiceForm, PurchaseReturnInvoiceForm, InvoiceItemForm,
    MaterialMoveForm, InvoiceItemFormSet
)

# Dashboard View
@method_decorator(login_required, name='dispatch')
class WarehouseDashboardView(TemplateView):
    template_name = 'warehouses/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Real data counts
        context.update({
            'total_materials': Material.objects.count(),
            'total_warehouses': Warehouse.objects.count(),
            'total_customers': Customer.objects.count(),
            'total_suppliers': Supplier.objects.count(),
            'total_invoices': Invoice.objects.count(),
            'total_sales': SalesInvoice.objects.count(),
            'total_purchases': PurchaseInvoice.objects.count(),
            'total_movements': MaterialMove.objects.count(),
            'low_stock_materials': Material.objects.filter(
                materialstock__quantity__lt=F('min_stock_level')
            ).distinct()[:5],
            'recent_invoices': Invoice.objects.order_by('-created_at')[:5],
            'recent_movements': MaterialMove.objects.order_by('-created_at')[:5],
        })

        return context

# Material Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListMaterialsView(ListView):
    model = Material
    template_name = 'warehouses/materials/materials.html'
    context_object_name = 'materials'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(code__icontains=q) | Q(barcode__icontains=q)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class CreateMaterialView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'warehouses/materials/material_form.html'
    success_url = reverse_lazy('materials')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'تم إضافة المادة بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MaterialDetailView(DetailView):
    model = Material
    template_name = 'warehouses/materials/material_detail.html'
    context_object_name = 'material'

    def get(self, request, *args, **kwargs):
        # If edit parameter is present, redirect to the update view
        if 'edit' in request.GET:
            return redirect('update_material', pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object

        # Get stock information for this material across all warehouses
        stocks = MaterialStock.objects.filter(material=material).select_related('warehouse')

        # Calculate total stock and value
        total_stock = sum(stock.quantity for stock in stocks)
        total_value = total_stock * material.cost_price

        context['stocks'] = stocks
        context['total_stock'] = total_stock
        context['total_value'] = total_value

        # Get recent movements for this material
        context['recent_movements'] = MaterialMove.objects.filter(
            material=material
        ).select_related('source_warehouse', 'destination_warehouse').order_by('-created_at')[:10]

        return context

@method_decorator(login_required, name='dispatch')
class UpdateMaterialView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'warehouses/materials/material_form.html'
    success_url = reverse_lazy('materials')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث المادة بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteMaterialView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف المادة بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MaterialActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي مواد')
            return redirect('materials')

        if action == 'delete':
            Material.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'تم حذف {len(selected_ids)} مواد بنجاح')
        elif action == 'activate':
            Material.objects.filter(id__in=selected_ids).update(is_active=True)
            messages.success(request, f'تم تنشيط {len(selected_ids)} مواد بنجاح')
        elif action == 'deactivate':
            Material.objects.filter(id__in=selected_ids).update(is_active=False)
            messages.success(request, f'تم إلغاء تنشيط {len(selected_ids)} مواد بنجاح')

        return redirect('materials')

# Category Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListCategoriesView(ListView):
    model = Category
    template_name = 'warehouses/categories/categories.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'warehouses/categories/category_form.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة الفئة بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateCategoryView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'warehouses/categories/category_form.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث الفئة بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف الفئة بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CategoryActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي فئات')
            return redirect('categories')

        if action == 'delete':
            Category.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'تم حذف {len(selected_ids)} فئات بنجاح')

        return redirect('categories')

# Unit Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListUnitsView(ListView):
    model = Unit
    template_name = 'warehouses/units/units.html'
    context_object_name = 'units'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(symbol__icontains=q)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateUnitView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'warehouses/units/unit_form.html'
    success_url = reverse_lazy('units')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة وحدة القياس بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateUnitView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'warehouses/units/unit_form.html'
    success_url = reverse_lazy('units')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث وحدة القياس بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteUnitView(DeleteView):
    model = Unit
    success_url = reverse_lazy('units')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف وحدة القياس بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class UnitActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي وحدات قياس')
            return redirect('units')

        if action == 'delete':
            Unit.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'تم حذف {len(selected_ids)} وحدات قياس بنجاح')

        return redirect('units')

@method_decorator(login_required, name='dispatch')
class UnitConversionsView(TemplateView):
    template_name = 'warehouses/units/unit_conversions.html'

# Warehouse Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListWarehousesView(ListView):
    model = Warehouse
    template_name = 'warehouses/warehouses/warehouses.html'
    context_object_name = 'warehouses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Basic search
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(location__icontains=q) |
                Q(code__icontains=q) | Q(manager__icontains=q)
            )

        # Status filter
        status = self.request.GET.get('status', None)
        if status:
            if status == 'active':
                queryset = queryset.filter(is_active=True)
            elif status == 'inactive':
                queryset = queryset.filter(is_active=False)
            elif status == 'maintenance':
                queryset = queryset.filter(status='maintenance')

        # Capacity filter
        capacity = self.request.GET.get('capacity', None)
        if capacity:
            if capacity == 'low':
                # Less than 30% capacity usage
                queryset = queryset.filter(capacity_usage__lt=30)
            elif capacity == 'medium':
                # Between 30% and 70% capacity usage
                queryset = queryset.filter(capacity_usage__gte=30, capacity_usage__lt=70)
            elif capacity == 'high':
                # More than 70% capacity usage
                queryset = queryset.filter(capacity_usage__gte=70, capacity_usage__lt=90)
            elif capacity == 'full':
                # More than 90% capacity usage
                queryset = queryset.filter(capacity_usage__gte=90)

        # Warehouse type filter
        warehouse_type = self.request.GET.get('warehouse_type', None)
        if warehouse_type:
            queryset = queryset.filter(warehouse_type=warehouse_type)

        # Region filter
        region = self.request.GET.get('region', None)
        if region:
            queryset = queryset.filter(region=region)

        # Sort
        sort = self.request.GET.get('sort', 'name')
        if sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'location':
            queryset = queryset.order_by('location')
        elif sort == 'updated':
            queryset = queryset.order_by('-updated_at')
        elif sort == 'capacity':
            # This is a bit tricky since capacity_usage is a property
            # For now, we'll just sort by capacity
            queryset = queryset.order_by('-capacity')
        elif sort == 'items':
            # This is also tricky since total_items is a property
            # We could use annotate to add a count, but for simplicity we'll use ID for now
            queryset = queryset.order_by('-id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate warehouse statistics
        warehouses = context['warehouses']
        total_materials = Material.objects.count()
        total_stock_items = MaterialStock.objects.count()

        # Calculate low stock items across all warehouses
        from django.db.models import F
        low_stock_count = MaterialStock.objects.filter(
            quantity__lt=F('material__min_stock_level'),
            quantity__gt=0
        ).count()

        # Calculate out of stock items
        out_of_stock_count = MaterialStock.objects.filter(quantity__lte=0).count()

        # Calculate today's movements
        from django.utils import timezone
        import datetime
        today = timezone.now().date()
        today_movements = MaterialMove.objects.filter(
            created_at__date=today
        ).count()

        # Calculate total warehouse capacity and usage
        from django.db.models import F, Sum, ExpressionWrapper, DecimalField
        total_capacity = Warehouse.objects.aggregate(Sum('capacity'))['capacity__sum'] or 0

        # Calculate total value of inventory
        total_value = MaterialStock.objects.annotate(
            item_value=ExpressionWrapper(
                F('quantity') * F('material__cost_price'),
                output_field=DecimalField()
            )
        ).aggregate(Sum('item_value'))['item_value__sum'] or 0

        # Add properties to each warehouse
        for warehouse in warehouses:
            # We're now using the model properties instead of calculating here
            # This makes the code cleaner and more maintainable
            pass

        context.update({
            'total_materials': total_materials,
            'total_stock_items': total_stock_items,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'low_stock_percentage': round((low_stock_count / total_stock_items * 100) if total_stock_items > 0 else 0, 1),
            'today_movements': today_movements,
            'total_capacity': total_capacity,
            'total_value': total_value,
            'warehouse_types': Warehouse.WAREHOUSE_TYPES,
            'regions': Warehouse.REGIONS,
            'status_choices': Warehouse.STATUS_CHOICES
        })

        return context

@method_decorator(login_required, name='dispatch')
class CreateWarehouseView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouses/warehouses/warehouse_form.html'
    success_url = reverse_lazy('warehouses_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة المستودع بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class WarehouseDetailView(DetailView):
    model = Warehouse
    template_name = 'warehouses/warehouses/warehouse_detail.html'
    context_object_name = 'warehouse'

    def get(self, request, *args, **kwargs):
        # If edit parameter is present, redirect to the update view
        if 'edit' in request.GET:
            return redirect('update_warehouse', pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse = self.object

        # Get all stocks in this warehouse with calculated values
        stocks = MaterialStock.objects.filter(warehouse=warehouse).select_related('material', 'material__unit', 'material__category')

        # Calculate total value and add it to each stock item
        total_value = 0
        for stock in stocks:
            stock.total_value = stock.quantity * stock.material.cost_price
            total_value += stock.total_value

            # Add stock status for each item
            if stock.quantity <= 0:
                stock.status = 'out_of_stock'
                stock.status_text = 'نفاذ المخزون'
                stock.status_class = 'danger'
            elif stock.quantity < stock.material.min_stock_level:
                stock.status = 'low_stock'
                stock.status_text = 'منخفض'
                stock.status_class = 'warning'
            else:
                stock.status = 'in_stock'
                stock.status_text = 'متوفر'
                stock.status_class = 'success'

        context['stocks'] = stocks

        # Calculate statistics - using model properties where possible
        context['total_value'] = total_value

        # Calculate stock status distribution
        normal_stock = stocks.filter(quantity__gte=F('material__min_stock_level')).count()
        low_stock = stocks.filter(quantity__lt=F('material__min_stock_level'), quantity__gt=0).count()
        out_of_stock = stocks.filter(quantity__lte=0).count()

        total_stock_count = normal_stock + low_stock + out_of_stock

        if total_stock_count > 0:
            context['normal_stock_percentage'] = round((normal_stock / total_stock_count) * 100)
            context['low_stock_percentage'] = round((low_stock / total_stock_count) * 100)
            context['out_of_stock_percentage'] = round((out_of_stock / total_stock_count) * 100)
        else:
            context['normal_stock_percentage'] = 0
            context['low_stock_percentage'] = 0
            context['out_of_stock_percentage'] = 0

        # Get recent movements for this warehouse
        context['recent_movements'] = MaterialMove.objects.filter(
            Q(source_warehouse=warehouse) | Q(destination_warehouse=warehouse)
        ).select_related('material', 'source_warehouse', 'destination_warehouse').order_by('-created_at')[:10]

        # Calculate movement statistics
        from django.utils import timezone
        import datetime
        today = timezone.now().date()
        this_month = timezone.now().replace(day=1)

        # Get movements by type
        today_movements = MaterialMove.objects.filter(
            Q(source_warehouse=warehouse) | Q(destination_warehouse=warehouse),
            created_at__date=today
        )

        context['today_movements_count'] = today_movements.count()

        # Count by movement type
        context['today_incoming'] = today_movements.filter(
            Q(destination_warehouse=warehouse),
            ~Q(source_warehouse=warehouse)  # Exclude transfers within the same warehouse
        ).count()

        context['today_outgoing'] = today_movements.filter(
            Q(source_warehouse=warehouse),
            ~Q(destination_warehouse=warehouse)  # Exclude transfers within the same warehouse
        ).count()

        context['today_transfers'] = today_movements.filter(
            Q(source_warehouse=warehouse),
            Q(destination_warehouse=warehouse)  # Only count transfers within the same warehouse
        ).count()

        context['month_movements_count'] = MaterialMove.objects.filter(
            Q(source_warehouse=warehouse) | Q(destination_warehouse=warehouse),
            created_at__gte=this_month
        ).count()

        # Get top materials by quantity
        top_materials = stocks.order_by('-quantity')[:5]
        context['top_materials'] = top_materials

        # Get warehouse type and region display names
        context['warehouse_type_display'] = warehouse.get_warehouse_type_display()
        context['region_display'] = warehouse.get_region_display()
        context['status_display'] = warehouse.get_status_display()

        return context

@method_decorator(login_required, name='dispatch')
class UpdateWarehouseView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouses/warehouses/warehouse_form.html'
    success_url = reverse_lazy('warehouses_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث المستودع بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteWarehouseView(DeleteView):
    model = Warehouse
    template_name = 'warehouses/warehouses/delete_warehouse.html'
    context_object_name = 'warehouse'
    success_url = reverse_lazy('warehouses_list')

    def delete(self, request, *args, **kwargs):
        warehouse = self.get_object()

        # Check if warehouse has materials
        if warehouse.materialstock_set.exists():
            messages.error(request, f'لا يمكن حذف المستودع "{warehouse.name}" لأنه يحتوي على مواد')
            return redirect('warehouses_list')

        messages.success(request, 'تم حذف المستودع بنجاح')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class WarehouseActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي مستودعات')
            return redirect('warehouses_list')

        if action == 'delete':
            # Check if warehouses have materials
            warehouses_with_materials = Warehouse.objects.filter(
                id__in=selected_ids,
                materialstock__quantity__gt=0
            ).distinct()

            if warehouses_with_materials.exists():
                warehouse_names = ", ".join([w.name for w in warehouses_with_materials])
                messages.error(
                    request,
                    f'لا يمكن حذف المستودعات التي تحتوي على مواد: {warehouse_names}'
                )
            else:
                # Safe to delete
                Warehouse.objects.filter(id__in=selected_ids).delete()
                messages.success(request, f'تم حذف {len(selected_ids)} مستودعات بنجاح')

        elif action == 'activate':
            Warehouse.objects.filter(id__in=selected_ids).update(is_active=True)
            messages.success(request, f'تم تنشيط {len(selected_ids)} مستودعات بنجاح')

        elif action == 'deactivate':
            Warehouse.objects.filter(id__in=selected_ids).update(is_active=False)
            messages.success(request, f'تم إلغاء تنشيط {len(selected_ids)} مستودعات بنجاح')

        return redirect('warehouses_list')

# Customer Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListCustomersView(ListView):
    model = Customer
    template_name = 'warehouses/customers/customers.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(contact_person__icontains=q) |
                Q(email__icontains=q) |
                Q(phone__icontains=q)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateCustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'warehouses/customers/customer_form.html'
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة العميل بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateCustomerView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'warehouses/customers/customer_form.html'
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث العميل بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteCustomerView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف العميل بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CustomerActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي عملاء')
            return redirect('customers')

        if action == 'delete':
            Customer.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'تم حذف {len(selected_ids)} عملاء بنجاح')
        elif action == 'activate':
            Customer.objects.filter(id__in=selected_ids).update(is_active=True)
            messages.success(request, f'تم تنشيط {len(selected_ids)} عملاء بنجاح')
        elif action == 'deactivate':
            Customer.objects.filter(id__in=selected_ids).update(is_active=False)
            messages.success(request, f'تم إلغاء تنشيط {len(selected_ids)} عملاء بنجاح')

        return redirect('customers')

# Supplier Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListSuppliersView(ListView):
    model = Supplier
    template_name = 'warehouses/suppliers/suppliers.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(contact_person__icontains=q) |
                Q(email__icontains=q) |
                Q(phone__icontains=q)
            )
        return queryset

@method_decorator(login_required, name='dispatch')
class CreateSupplierView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'warehouses/suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers')

    def form_valid(self, form):
        messages.success(self.request, 'تم إضافة المورد بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UpdateSupplierView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'warehouses/suppliers/supplier_form.html'
    success_url = reverse_lazy('suppliers')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث المورد بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteSupplierView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'تم حذف المورد بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class SupplierActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي موردين')
            return redirect('suppliers')

        if action == 'delete':
            Supplier.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'تم حذف {len(selected_ids)} موردين بنجاح')
        elif action == 'activate':
            Supplier.objects.filter(id__in=selected_ids).update(is_active=True)
            messages.success(request, f'تم تنشيط {len(selected_ids)} موردين بنجاح')
        elif action == 'deactivate':
            Supplier.objects.filter(id__in=selected_ids).update(is_active=False)
            messages.success(request, f'تم إلغاء تنشيط {len(selected_ids)} موردين بنجاح')

        return redirect('suppliers')

# Invoice Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListInvoicesView(ListView):
    model = Invoice
    template_name = 'warehouses/invoices/invoices.html'
    context_object_name = 'invoices'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        invoice_type = self.request.GET.get('type', None)
        status = self.request.GET.get('status', None)

        if q:
            queryset = queryset.filter(
                Q(invoice_number__icontains=q) |
                Q(salesinvoice__customer__name__icontains=q) |
                Q(purchaseinvoice__supplier__name__icontains=q)
            )

        if invoice_type:
            queryset = queryset.filter(invoice_type=invoice_type)

        if status:
            queryset = queryset.filter(payment_status=status)

        return queryset.order_by('-date')

@method_decorator(login_required, name='dispatch')
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'warehouses/invoices/invoice_detail.html'
    context_object_name = 'invoice'

@method_decorator(login_required, name='dispatch')
class CreateSalesInvoiceView(CreateView):
    model = SalesInvoice
    form_class = SalesInvoiceForm
    template_name = 'warehouses/invoices/invoice_form.html'
    success_url = reverse_lazy('invoices')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_type'] = 'sales'
        context['invoice_type_display'] = 'فاتورة مبيعات جديدة'

        if self.request.POST:
            context['invoice_form'] = InvoiceForm(self.request.POST, prefix='invoice')
            context['formset'] = InvoiceItemFormSet(self.request.POST, prefix='items')
        else:
            context['invoice_form'] = InvoiceForm(prefix='invoice', initial={'invoice_type': 'sales'})
            context['formset'] = InvoiceItemFormSet(prefix='items')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_form = context['invoice_form']
        formset = context['formset']

        if invoice_form.is_valid() and formset.is_valid():
            # Save invoice
            invoice = invoice_form.save(commit=False)
            invoice.created_by = self.request.user
            invoice.save()

            # Save sales invoice
            sales_invoice = form.save(commit=False)
            sales_invoice.invoice = invoice
            sales_invoice.save()

            # Save invoice items
            total_amount = 0
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = item_form.save(commit=False)
                    item.invoice = invoice
                    item.total_price = item.quantity * item.unit_price
                    item.save()
                    total_amount += item.total_price

                    # Update stock
                    MaterialStock.objects.update_or_create(
                        material=item.material,
                        warehouse=sales_invoice.warehouse,
                        defaults={'quantity': F('quantity') - item.quantity}
                    )

                    # Create movement
                    MaterialMove.objects.create(
                        material=item.material,
                        quantity=item.quantity,
                        move_type='out',
                        source_warehouse=sales_invoice.warehouse,
                        reference_invoice=invoice,
                        created_by=self.request.user
                    )

            # Update invoice total
            invoice.total_amount = total_amount
            invoice.save()

            messages.success(self.request, 'تم إنشاء فاتورة المبيعات بنجاح')
            return redirect('invoices')
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CreatePurchaseInvoiceView(CreateView):
    model = PurchaseInvoice
    form_class = PurchaseInvoiceForm
    template_name = 'warehouses/invoices/invoice_form.html'
    success_url = reverse_lazy('invoices')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_type'] = 'purchase'
        context['invoice_type_display'] = 'فاتورة مشتريات جديدة'

        if self.request.POST:
            context['invoice_form'] = InvoiceForm(self.request.POST, prefix='invoice')
            context['formset'] = InvoiceItemFormSet(self.request.POST, prefix='items')
        else:
            context['invoice_form'] = InvoiceForm(prefix='invoice', initial={'invoice_type': 'purchase'})
            context['formset'] = InvoiceItemFormSet(prefix='items')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_form = context['invoice_form']
        formset = context['formset']

        if invoice_form.is_valid() and formset.is_valid():
            # Save invoice
            invoice = invoice_form.save(commit=False)
            invoice.created_by = self.request.user
            invoice.save()

            # Save purchase invoice
            purchase_invoice = form.save(commit=False)
            purchase_invoice.invoice = invoice
            purchase_invoice.save()

            # Save invoice items
            total_amount = 0
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = item_form.save(commit=False)
                    item.invoice = invoice
                    item.total_price = item.quantity * item.unit_price
                    item.save()
                    total_amount += item.total_price

                    # Update stock
                    MaterialStock.objects.update_or_create(
                        material=item.material,
                        warehouse=purchase_invoice.warehouse,
                        defaults={'quantity': F('quantity') + item.quantity}
                    )

                    # Create movement
                    MaterialMove.objects.create(
                        material=item.material,
                        quantity=item.quantity,
                        move_type='in',
                        destination_warehouse=purchase_invoice.warehouse,
                        reference_invoice=invoice,
                        created_by=self.request.user
                    )

            # Update invoice total
            invoice.total_amount = total_amount
            invoice.save()

            messages.success(self.request, 'تم إنشاء فاتورة المشتريات بنجاح')
            return redirect('invoices')
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class DeleteInvoiceView(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices')

    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()

        # Reverse stock changes
        if invoice.invoice_type == 'sales':
            sales_invoice = invoice.salesinvoice
            for item in invoice.items.all():
                # Add back to stock
                MaterialStock.objects.update_or_create(
                    material=item.material,
                    warehouse=sales_invoice.warehouse,
                    defaults={'quantity': F('quantity') + item.quantity}
                )
        elif invoice.invoice_type == 'purchase':
            purchase_invoice = invoice.purchaseinvoice
            for item in invoice.items.all():
                # Remove from stock
                MaterialStock.objects.update_or_create(
                    material=item.material,
                    warehouse=purchase_invoice.warehouse,
                    defaults={'quantity': F('quantity') - item.quantity}
                )

        # Delete related movements
        MaterialMove.objects.filter(reference_invoice=invoice).delete()

        messages.success(request, 'تم حذف الفاتورة بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PrintInvoiceView(DetailView):
    model = Invoice
    template_name = 'warehouses/invoices/invoice_print.html'
    context_object_name = 'invoice'

@method_decorator(login_required, name='dispatch')
class UpdateInvoiceStatusView(UpdateView):
    model = Invoice
    fields = ['payment_status']
    template_name = 'warehouses/invoices/update_status.html'
    success_url = reverse_lazy('invoices')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث حالة الدفع بنجاح')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class InvoiceActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي فواتير')
            return redirect('invoices')

        if action == 'delete':
            # Get invoices
            invoices = Invoice.objects.filter(id__in=selected_ids)

            # Reverse stock changes for each invoice
            for invoice in invoices:
                if invoice.invoice_type == 'sales':
                    sales_invoice = invoice.salesinvoice
                    for item in invoice.items.all():
                        # Add back to stock
                        MaterialStock.objects.update_or_create(
                            material=item.material,
                            warehouse=sales_invoice.warehouse,
                            defaults={'quantity': F('quantity') + item.quantity}
                        )
                elif invoice.invoice_type == 'purchase':
                    purchase_invoice = invoice.purchaseinvoice
                    for item in invoice.items.all():
                        # Remove from stock
                        MaterialStock.objects.update_or_create(
                            material=item.material,
                            warehouse=purchase_invoice.warehouse,
                            defaults={'quantity': F('quantity') - item.quantity}
                        )

                # Delete related movements
                MaterialMove.objects.filter(reference_invoice=invoice).delete()

            # Delete invoices
            invoices.delete()
            messages.success(request, f'تم حذف {len(selected_ids)} فواتير بنجاح')
        elif action in ['mark_paid', 'mark_partial', 'mark_pending']:
            status_map = {
                'mark_paid': 'paid',
                'mark_partial': 'partial',
                'mark_pending': 'pending'
            }
            Invoice.objects.filter(id__in=selected_ids).update(payment_status=status_map[action])
            messages.success(request, f'تم تحديث حالة {len(selected_ids)} فواتير بنجاح')

        return redirect('invoices')

# Material Movement Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ListMovementsView(ListView):
    model = MaterialMove
    template_name = 'warehouses/movements/movements.html'
    context_object_name = 'movements'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        material = self.request.GET.get('material', None)
        warehouse = self.request.GET.get('warehouse', None)
        move_type = self.request.GET.get('move_type', None)

        if q:
            queryset = queryset.filter(
                Q(material__name__icontains=q) |
                Q(source_warehouse__name__icontains=q) |
                Q(destination_warehouse__name__icontains=q)
            )

        if material:
            queryset = queryset.filter(material_id=material)

        if warehouse:
            queryset = queryset.filter(
                Q(source_warehouse_id=warehouse) |
                Q(destination_warehouse_id=warehouse)
            )

        if move_type:
            queryset = queryset.filter(move_type=move_type)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materials'] = Material.objects.all()
        context['warehouses'] = Warehouse.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class MovementDetailView(DetailView):
    model = MaterialMove
    template_name = 'warehouses/movements/movement_detail.html'
    context_object_name = 'movement'

@method_decorator(login_required, name='dispatch')
class CreateMovementView(CreateView):
    model = MaterialMove
    form_class = MaterialMoveForm
    template_name = 'warehouses/movements/movement_form.html'
    success_url = reverse_lazy('movements')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movement_type = self.request.GET.get('type', 'transfer')
        context['movement_type'] = movement_type

        type_display_map = {
            'in': 'إدخال مواد',
            'out': 'إخراج مواد',
            'transfer': 'نقل مواد',
            'adjustment': 'تعديل مخزون'
        }
        context['movement_type_display'] = type_display_map.get(movement_type, 'حركة جديدة')

        return context

    def form_valid(self, form):
        try:
            movement = form.save(commit=False)
            movement_type = self.request.GET.get('type', 'transfer')
            movement.move_type = movement_type
            movement.created_by = self.request.user

            # Handle different movement types
            if movement_type == 'in':
                # Validate destination warehouse
                if not movement.destination_warehouse:
                    form.add_error('destination_warehouse', 'يجب تحديد المستودع الهدف')
                    return self.form_invalid(form)

                # Add to destination warehouse
                MaterialStock.objects.update_or_create(
                    material=movement.material,
                    warehouse=movement.destination_warehouse,
                    defaults={'quantity': F('quantity') + movement.quantity}
                )

            elif movement_type == 'out':
                # Validate source warehouse
                if not movement.source_warehouse:
                    form.add_error('source_warehouse', 'يجب تحديد المستودع المصدر')
                    return self.form_invalid(form)

                # Check if enough stock
                stock = MaterialStock.objects.filter(
                    material=movement.material,
                    warehouse=movement.source_warehouse
                ).first()

                if not stock:
                    form.add_error(None, f'لا يوجد مخزون للمادة {movement.material.name} في المستودع {movement.source_warehouse.name}')
                    return self.form_invalid(form)

                if stock.quantity < movement.quantity:
                    form.add_error(None, f'لا يوجد مخزون كافي في المستودع المصدر. المتوفر: {stock.quantity} {movement.material.unit.symbol}')
                    return self.form_invalid(form)

                # Remove from source warehouse
                stock.quantity -= movement.quantity
                stock.save()

            elif movement_type == 'transfer':
                # Validate source and destination warehouses
                if not movement.source_warehouse:
                    form.add_error('source_warehouse', 'يجب تحديد المستودع المصدر')
                    return self.form_invalid(form)

                if not movement.destination_warehouse:
                    form.add_error('destination_warehouse', 'يجب تحديد المستودع الهدف')
                    return self.form_invalid(form)

                if movement.source_warehouse == movement.destination_warehouse:
                    form.add_error(None, 'لا يمكن نقل المواد إلى نفس المستودع')
                    return self.form_invalid(form)

                # Check if enough stock
                stock = MaterialStock.objects.filter(
                    material=movement.material,
                    warehouse=movement.source_warehouse
                ).first()

                if not stock:
                    form.add_error(None, f'لا يوجد مخزون للمادة {movement.material.name} في المستودع {movement.source_warehouse.name}')
                    return self.form_invalid(form)

                if stock.quantity < movement.quantity:
                    form.add_error(None, f'لا يوجد مخزون كافي في المستودع المصدر. المتوفر: {stock.quantity} {movement.material.unit.symbol}')
                    return self.form_invalid(form)

                # Remove from source warehouse
                stock.quantity -= movement.quantity
                stock.save()

                # Add to destination warehouse
                MaterialStock.objects.update_or_create(
                    material=movement.material,
                    warehouse=movement.destination_warehouse,
                    defaults={'quantity': F('quantity') + movement.quantity}
                )

            elif movement_type == 'adjustment':
                # For adjustment, we use source_warehouse as the warehouse to adjust
                warehouse = movement.source_warehouse
                if not warehouse:
                    form.add_error('source_warehouse', 'يجب تحديد المستودع للتعديل')
                    return self.form_invalid(form)

                # Store previous quantity
                stock = MaterialStock.objects.filter(
                    material=movement.material,
                    warehouse=warehouse
                ).first()

                # Store previous quantity in notes if not already set
                previous_qty = stock.quantity if stock else 0
                if not movement.notes:
                    movement.notes = f"تعديل المخزون من {previous_qty} إلى {movement.quantity}"

                # Update stock
                MaterialStock.objects.update_or_create(
                    material=movement.material,
                    warehouse=warehouse,
                    defaults={'quantity': movement.quantity}
                )

            # Save the movement
            movement.save()
            messages.success(self.request, 'تم إنشاء الحركة بنجاح')
            return redirect('movements')

        except Exception as e:
            form.add_error(None, f'حدث خطأ أثناء معالجة الحركة: {str(e)}')
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class DeleteMovementView(DeleteView):
    model = MaterialMove
    success_url = reverse_lazy('movements')

    def delete(self, request, *args, **kwargs):
        movement = self.get_object()

        # Reverse stock changes
        if movement.move_type == 'in':
            # Remove from destination warehouse
            MaterialStock.objects.update_or_create(
                material=movement.material,
                warehouse=movement.destination_warehouse,
                defaults={'quantity': F('quantity') - movement.quantity}
            )
        elif movement.move_type == 'out':
            # Add back to source warehouse
            MaterialStock.objects.update_or_create(
                material=movement.material,
                warehouse=movement.source_warehouse,
                defaults={'quantity': F('quantity') + movement.quantity}
            )
        elif movement.move_type == 'transfer':
            # Add back to source warehouse
            MaterialStock.objects.update_or_create(
                material=movement.material,
                warehouse=movement.source_warehouse,
                defaults={'quantity': F('quantity') + movement.quantity}
            )

            # Remove from destination warehouse
            MaterialStock.objects.update_or_create(
                material=movement.material,
                warehouse=movement.destination_warehouse,
                defaults={'quantity': F('quantity') - movement.quantity}
            )
        elif movement.move_type == 'adjustment':
            # For adjustment, we use source_warehouse as the warehouse
            warehouse = movement.source_warehouse

            # Extract previous quantity from notes if available
            previous_qty = 0
            if movement.notes and 'تعديل المخزون من' in movement.notes:
                try:
                    # Try to extract the previous quantity from the notes
                    parts = movement.notes.split('تعديل المخزون من')[1].split('إلى')
                    if len(parts) > 0:
                        previous_qty = float(parts[0].strip())
                except:
                    pass

            # Restore previous quantity
            MaterialStock.objects.update_or_create(
                material=movement.material,
                warehouse=warehouse,
                defaults={'quantity': previous_qty}
            )

        messages.success(request, 'تم حذف الحركة بنجاح')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class MovementActionView(View):
    def post(self, request):
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.error(request, 'لم يتم تحديد أي حركات')
            return redirect('movements')

        if action == 'delete':
            # Get movements
            movements = MaterialMove.objects.filter(id__in=selected_ids)

            # Reverse stock changes for each movement
            for movement in movements:
                if movement.move_type == 'in':
                    # Remove from destination warehouse
                    MaterialStock.objects.update_or_create(
                        material=movement.material,
                        warehouse=movement.destination_warehouse,
                        defaults={'quantity': F('quantity') - movement.quantity}
                    )
                elif movement.move_type == 'out':
                    # Add back to source warehouse
                    MaterialStock.objects.update_or_create(
                        material=movement.material,
                        warehouse=movement.source_warehouse,
                        defaults={'quantity': F('quantity') + movement.quantity}
                    )
                elif movement.move_type == 'transfer':
                    # Add back to source warehouse
                    MaterialStock.objects.update_or_create(
                        material=movement.material,
                        warehouse=movement.source_warehouse,
                        defaults={'quantity': F('quantity') + movement.quantity}
                    )

                    # Remove from destination warehouse
                    MaterialStock.objects.update_or_create(
                        material=movement.material,
                        warehouse=movement.destination_warehouse,
                        defaults={'quantity': F('quantity') - movement.quantity}
                    )
                elif movement.move_type == 'adjustment':
                    # For adjustment, we use source_warehouse as the warehouse
                    warehouse = movement.source_warehouse

                    # Extract previous quantity from notes if available
                    previous_qty = 0
                    if movement.notes and 'تعديل المخزون من' in movement.notes:
                        try:
                            # Try to extract the previous quantity from the notes
                            parts = movement.notes.split('تعديل المخزون من')[1].split('إلى')
                            if len(parts) > 0:
                                previous_qty = float(parts[0].strip())
                        except:
                            pass

                    # Restore previous quantity
                    MaterialStock.objects.update_or_create(
                        material=movement.material,
                        warehouse=warehouse,
                        defaults={'quantity': previous_qty}
                    )

            # Delete movements
            movements.delete()
            messages.success(request, f'تم حذف {len(selected_ids)} حركات بنجاح')

        return redirect('movements')

# API Views
@method_decorator(login_required, name='dispatch')
class MaterialStockAPIView(View):
    def get(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        stocks = MaterialStock.objects.filter(material=material).select_related('warehouse')

        data = {
            'material_id': material.id,
            'material_name': material.name,
            'unit_symbol': material.unit.symbol,
            'min_stock_level': float(material.min_stock_level),
            'stocks': [
                {
                    'warehouse_id': stock.warehouse.id,
                    'warehouse_name': stock.warehouse.name,
                    'quantity': float(stock.quantity),
                    'status': 'out' if stock.quantity <= 0 else ('low' if stock.quantity < material.min_stock_level else 'ok')
                }
                for stock in stocks
            ]
        }

        return JsonResponse(data)

# Placeholder Views for each section
@method_decorator(login_required, name='dispatch')
class MaterialsPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'المواد',
            'description': 'إدارة المواد والمنتجات في المستودعات',
            'features': [
                'إضافة وتعديل وحذف المواد',
                'تصنيف المواد حسب الفئات',
                'تتبع المخزون لكل مادة',
                'تحديد وحدات القياس',
                'إضافة صور للمواد',
                'تحديد أسعار البيع والشراء',
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class WarehousesPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'المستودعات',
            'description': 'إدارة المستودعات ومواقع التخزين',
            'features': [
                'إضافة وتعديل وحذف المستودعات',
                'تحديد موقع كل مستودع',
                'تعيين مسؤولين للمستودعات',
                'تتبع المخزون في كل مستودع',
                'نقل المواد بين المستودعات',
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class InvoicesPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'الفواتير',
            'description': 'إدارة فواتير المبيعات والمشتريات',
            'features': [
                'إنشاء فواتير المبيعات',
                'إنشاء فواتير المشتريات',
                'إدارة فواتير المرتجعات',
                'طباعة الفواتير',
                'تتبع حالة الدفع',
                'ربط الفواتير بحركة المخزون',
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class CustomersPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'العملاء',
            'description': 'إدارة بيانات العملاء',
            'features': [
                'إضافة وتعديل وحذف العملاء',
                'تتبع مشتريات العملاء',
                'إدارة الحسابات والديون',
                'تقارير مبيعات لكل عميل',
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class SuppliersPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'الموردين',
            'description': 'إدارة بيانات الموردين',
            'features': [
                'إضافة وتعديل وحذف الموردين',
                'تتبع المشتريات من كل مورد',
                'إدارة الحسابات والديون',
                'تقارير المشتريات لكل مورد',
            ]
        })
        return context

@method_decorator(login_required, name='dispatch')
class MovementsPlaceholderView(TemplateView):
    template_name = 'warehouses/placeholder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'حركة المواد',
            'description': 'تتبع حركة المواد بين المستودعات',
            'features': [
                'تسجيل نقل المواد بين المستودعات',
                'تعديل المخزون يدوياً',
                'تتبع تاريخ كل حركة',
                'ربط الحركات بالفواتير',
                'تقارير الحركة لكل مادة ومستودع',
            ]
        })
        return context

# Report Views - Real implementation
@method_decorator(login_required, name='dispatch')
class ReportsView(TemplateView):
    template_name = 'warehouses/reports/reports.html'

@method_decorator(login_required, name='dispatch')
class InventoryReportView(ListView):
    model = MaterialStock
    template_name = 'warehouses/reports/inventory_report.html'
    context_object_name = 'inventory_items'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('material', 'material__category', 'material__unit', 'warehouse')
        q = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)
        warehouse = self.request.GET.get('warehouse', None)
        stock_status = self.request.GET.get('stock_status', None)

        if q:
            queryset = queryset.filter(
                Q(material__name__icontains=q) |
                Q(material__code__icontains=q) |
                Q(warehouse__name__icontains=q)
            )

        if category:
            queryset = queryset.filter(material__category_id=category)

        if warehouse:
            queryset = queryset.filter(warehouse_id=warehouse)

        if stock_status == 'low':
            queryset = queryset.filter(quantity__lt=F('material__min_stock_level'), quantity__gt=0)
        elif stock_status == 'out':
            queryset = queryset.filter(quantity__lte=0)

        # Annotate with total value
        queryset = queryset.annotate(
            total_value=ExpressionWrapper(
                F('quantity') * F('material__cost_price'),
                output_field=DecimalField()
            )
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = 'inventory'
        context['categories'] = Category.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        # Get selected filters
        if 'category' in self.request.GET and self.request.GET['category']:
            context['selected_category'] = Category.objects.get(id=self.request.GET['category'])

        if 'warehouse' in self.request.GET and self.request.GET['warehouse']:
            context['selected_warehouse'] = Warehouse.objects.get(id=self.request.GET['warehouse'])

        # Calculate total value
        total_value = sum(item.total_value for item in context['inventory_items'])
        context['total_value'] = total_value

        return context

@method_decorator(login_required, name='dispatch')
class MovementReportView(ListView):
    model = MaterialMove
    template_name = 'warehouses/reports/movement_report.html'
    context_object_name = 'movements'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'material', 'material__unit', 'source_warehouse',
            'destination_warehouse', 'reference_invoice', 'created_by'
        )

        q = self.request.GET.get('q', None)
        material = self.request.GET.get('material', None)
        warehouse = self.request.GET.get('warehouse', None)
        move_type = self.request.GET.get('move_type', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if q:
            queryset = queryset.filter(
                Q(material__name__icontains=q) |
                Q(source_warehouse__name__icontains=q) |
                Q(destination_warehouse__name__icontains=q)
            )

        if material:
            queryset = queryset.filter(material_id=material)

        if warehouse:
            queryset = queryset.filter(
                Q(source_warehouse_id=warehouse) |
                Q(destination_warehouse_id=warehouse)
            )

        if move_type:
            queryset = queryset.filter(move_type=move_type)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = 'movement'
        context['materials'] = Material.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        return context

@method_decorator(login_required, name='dispatch')
class SalesReportView(ListView):
    model = Invoice
    template_name = 'warehouses/reports/sales_report.html'
    context_object_name = 'invoices'
    paginate_by = 20

    def get_queryset(self):
        queryset = Invoice.objects.filter(invoice_type='sales').select_related(
            'salesinvoice', 'salesinvoice__customer', 'salesinvoice__warehouse'
        ).prefetch_related('items')

        q = self.request.GET.get('q', None)
        customer = self.request.GET.get('customer', None)
        warehouse = self.request.GET.get('warehouse', None)
        payment_status = self.request.GET.get('payment_status', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if q:
            queryset = queryset.filter(
                Q(invoice_number__icontains=q) |
                Q(salesinvoice__customer__name__icontains=q)
            )

        if customer:
            queryset = queryset.filter(salesinvoice__customer_id=customer)

        if warehouse:
            queryset = queryset.filter(salesinvoice__warehouse_id=warehouse)

        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__lte=end_date)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = 'sales'
        context['customers'] = Customer.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        # Calculate total sales
        total_sales = context['invoices'].aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['total_sales'] = total_sales

        # Prepare chart data if there are invoices
        if context['invoices']:
            context['show_chart'] = True

            # Customer chart data
            customer_data = {}
            for invoice in context['invoices']:
                customer_name = invoice.salesinvoice.customer.name
                if customer_name in customer_data:
                    customer_data[customer_name] += float(invoice.total_amount)
                else:
                    customer_data[customer_name] = float(invoice.total_amount)

            # Sort by amount and limit to top 10
            sorted_customer_data = dict(sorted(customer_data.items(), key=lambda x: x[1], reverse=True)[:10])

            context['customer_labels'] = json.dumps(list(sorted_customer_data.keys()))
            context['customer_data'] = json.dumps(list(sorted_customer_data.values()))

            # Monthly chart data
            monthly_data = {}
            for invoice in context['invoices']:
                month_key = invoice.date.strftime('%Y-%m')
                month_name = invoice.date.strftime('%b %Y')
                if month_key in monthly_data:
                    monthly_data[month_key]['amount'] += float(invoice.total_amount)
                else:
                    monthly_data[month_key] = {'name': month_name, 'amount': float(invoice.total_amount)}

            # Sort by month
            sorted_monthly_data = dict(sorted(monthly_data.items()))

            context['monthly_labels'] = json.dumps([data['name'] for data in sorted_monthly_data.values()])
            context['monthly_data'] = json.dumps([data['amount'] for data in sorted_monthly_data.values()])

        return context

@method_decorator(login_required, name='dispatch')
class PurchaseReportView(ListView):
    model = Invoice
    template_name = 'warehouses/reports/purchase_report.html'
    context_object_name = 'invoices'
    paginate_by = 20

    def get_queryset(self):
        queryset = Invoice.objects.filter(invoice_type='purchase').select_related(
            'purchaseinvoice', 'purchaseinvoice__supplier', 'purchaseinvoice__warehouse'
        ).prefetch_related('items')

        q = self.request.GET.get('q', None)
        supplier = self.request.GET.get('supplier', None)
        warehouse = self.request.GET.get('warehouse', None)
        payment_status = self.request.GET.get('payment_status', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if q:
            queryset = queryset.filter(
                Q(invoice_number__icontains=q) |
                Q(purchaseinvoice__supplier__name__icontains=q)
            )

        if supplier:
            queryset = queryset.filter(purchaseinvoice__supplier_id=supplier)

        if warehouse:
            queryset = queryset.filter(purchaseinvoice__warehouse_id=warehouse)

        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(date__date__lte=end_date)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = 'purchase'
        context['suppliers'] = Supplier.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        # Calculate total purchases
        total_purchases = context['invoices'].aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['total_purchases'] = total_purchases

        # Prepare chart data if there are invoices
        if context['invoices']:
            context['show_chart'] = True

            # Supplier chart data
            supplier_data = {}
            for invoice in context['invoices']:
                supplier_name = invoice.purchaseinvoice.supplier.name
                if supplier_name in supplier_data:
                    supplier_data[supplier_name] += float(invoice.total_amount)
                else:
                    supplier_data[supplier_name] = float(invoice.total_amount)

            # Sort by amount and limit to top 10
            sorted_supplier_data = dict(sorted(supplier_data.items(), key=lambda x: x[1], reverse=True)[:10])

            context['supplier_labels'] = json.dumps(list(sorted_supplier_data.keys()))
            context['supplier_data'] = json.dumps(list(sorted_supplier_data.values()))

            # Monthly chart data
            monthly_data = {}
            for invoice in context['invoices']:
                month_key = invoice.date.strftime('%Y-%m')
                month_name = invoice.date.strftime('%b %Y')
                if month_key in monthly_data:
                    monthly_data[month_key]['amount'] += float(invoice.total_amount)
                else:
                    monthly_data[month_key] = {'name': month_name, 'amount': float(invoice.total_amount)}

            # Sort by month
            sorted_monthly_data = dict(sorted(monthly_data.items()))

            context['monthly_labels'] = json.dumps([data['name'] for data in sorted_monthly_data.values()])
            context['monthly_data'] = json.dumps([data['amount'] for data in sorted_monthly_data.values()])

        return context

@method_decorator(login_required, name='dispatch')
class PrintInventoryReportView(InventoryReportView):
    template_name = 'warehouses/reports/print_inventory_report.html'
    paginate_by = None  # Show all items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class ExportInventoryReportView(InventoryReportView):
    paginate_by = None  # Show all items

# Advanced Visualization Views
@method_decorator(login_required, name='dispatch')
class VisualizationDashboardView(TemplateView):
    template_name = 'warehouses/visualizations/dashboard.html'

@method_decorator(login_required, name='dispatch')
class WarehouseHeatmapView(TemplateView):
    template_name = 'warehouses/visualizations/heatmap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all warehouses with their utilization data
        warehouses = Warehouse.objects.all()
        context['warehouses'] = warehouses

        # Get warehouse types data
        warehouse_types = dict(Warehouse.WAREHOUSE_TYPES)
        type_counts = Warehouse.objects.values('warehouse_type').annotate(count=Count('id'))

        type_names = []
        type_counts_list = []

        for type_data in type_counts:
            type_code = type_data['warehouse_type']
            type_names.append(warehouse_types.get(type_code, type_code))
            type_counts_list.append(type_data['count'])

        context['warehouse_types'] = json.dumps(type_names)
        context['warehouse_type_counts'] = json.dumps(type_counts_list)

        # Get warehouse names and stock data for charts
        warehouse_names = []
        warehouse_stock = []

        for warehouse in warehouses:
            warehouse_names.append(warehouse.name)
            warehouse_stock.append(float(warehouse.total_quantity))

        context['warehouse_names'] = json.dumps(warehouse_names)
        context['warehouse_stock'] = json.dumps(warehouse_stock)

        return context

@method_decorator(login_required, name='dispatch')
class MaterialTimelineView(TemplateView):
    template_name = 'warehouses/visualizations/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get movement data for the last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        movements = MaterialMove.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).order_by('created_at')

        # Prepare data for timeline
        dates_dict = defaultdict(lambda: {'incoming': 0, 'outgoing': 0, 'transfers': 0})

        for movement in movements:
            date_str = movement.created_at.date().strftime('%Y-%m-%d')

            if movement.move_type in ['purchase', 'return_in']:
                dates_dict[date_str]['incoming'] += 1
            elif movement.move_type in ['sale', 'return_out']:
                dates_dict[date_str]['outgoing'] += 1
            elif movement.move_type in ['transfer', 'adjustment']:
                dates_dict[date_str]['transfers'] += 1

        # Fill in missing dates
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str not in dates_dict:
                dates_dict[date_str] = {'incoming': 0, 'outgoing': 0, 'transfers': 0}
            current_date += timedelta(days=1)

        # Sort dates
        sorted_dates = sorted(dates_dict.items())
        movement_dates = [date for date, _ in sorted_dates]
        movement_incoming = [data['incoming'] for _, data in sorted_dates]
        movement_outgoing = [data['outgoing'] for _, data in sorted_dates]
        movement_transfers = [data['transfers'] for _, data in sorted_dates]

        context['movement_dates'] = json.dumps(movement_dates)
        context['movement_incoming'] = json.dumps(movement_incoming)
        context['movement_outgoing'] = json.dumps(movement_outgoing)
        context['movement_transfers'] = json.dumps(movement_transfers)

        # Get movement types data
        movement_types_data = MaterialMove.objects.values('move_type').annotate(count=Count('id'))
        movement_types = []
        movement_type_counts = []

        move_type_display = dict(MaterialMove.MOVE_TYPES)

        for type_data in movement_types_data:
            type_code = type_data['move_type']
            movement_types.append(move_type_display.get(type_code, type_code))
            movement_type_counts.append(type_data['count'])

        context['movement_types'] = json.dumps(movement_types)
        context['movement_type_counts'] = json.dumps(movement_type_counts)

        # Get top moved materials
        top_moved_data = MaterialMove.objects.values('material__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        top_moved_materials = []
        top_moved_counts = []

        for item in top_moved_data:
            top_moved_materials.append(item['material__name'])
            top_moved_counts.append(item['count'])

        context['top_moved_materials'] = json.dumps(top_moved_materials)
        context['top_moved_counts'] = json.dumps(top_moved_counts)

        # Get recent movements for timeline display
        context['recent_movements'] = MaterialMove.objects.select_related(
            'material', 'source_warehouse', 'destination_warehouse', 'material__unit'
        ).order_by('-created_at')[:20]

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all categories and warehouses for filters
        context['categories'] = Category.objects.all()
        context['warehouses'] = Warehouse.objects.all()

        # 1. Inventory Analysis Data
        # Get category data for inventory analysis
        categories = Category.objects.all()
        category_data = []
        category_names = []
        category_quantities = []
        category_values = []

        for category in categories:
            # Get total quantity and value for each category
            materials = Material.objects.filter(category=category)
            total_quantity = 0
            total_value = 0

            for material in materials:
                quantity = material.total_stock
                total_quantity += quantity
                total_value += quantity * material.cost_price

            if total_quantity > 0:  # Only include categories with stock
                category_names.append(category.name)
                category_quantities.append(float(total_quantity))
                category_values.append(float(total_value))

        context['category_names'] = json.dumps(category_names)
        context['category_quantities'] = json.dumps(category_quantities)
        context['category_values'] = json.dumps(category_values)

        # Get warehouse distribution data
        warehouses = Warehouse.objects.all()
        warehouse_names = []
        warehouse_stock = []
        warehouse_utilization = []
        warehouse_material_counts = []

        for warehouse in warehouses:
            warehouse_names.append(warehouse.name)
            warehouse_stock.append(float(warehouse.total_quantity))
            warehouse_utilization.append(float(warehouse.capacity_usage))
            warehouse_material_counts.append(warehouse.materialstock_set.count())

        context['warehouse_names'] = json.dumps(warehouse_names)
        context['warehouse_stock'] = json.dumps(warehouse_stock)
        context['warehouse_utilization'] = json.dumps(warehouse_utilization)
        context['warehouse_material_counts'] = json.dumps(warehouse_material_counts)

        # Get warehouse types data
        warehouse_types = dict(Warehouse.WAREHOUSE_TYPES)
        type_counts = Warehouse.objects.values('warehouse_type').annotate(count=Count('id'))
        type_names = []
        type_utilization = []

        for type_data in type_counts:
            type_code = type_data['warehouse_type']
            type_names.append(warehouse_types.get(type_code, type_code))

            # Calculate average utilization for this warehouse type
            warehouses_of_type = Warehouse.objects.filter(warehouse_type=type_code)
            avg_utilization = sum(w.capacity_usage for w in warehouses_of_type) / warehouses_of_type.count() if warehouses_of_type.exists() else 0
            type_utilization.append(float(avg_utilization))

        context['warehouse_types'] = json.dumps(type_names)
        context['warehouse_type_utilization'] = json.dumps(type_utilization)

        # Get low stock materials data
        low_stock_materials = Material.objects.filter(
            materialstock__quantity__lt=F('min_stock_level'),
            materialstock__quantity__gt=0
        ).distinct()[:10]

        low_stock_names = []
        low_stock_current = []
        low_stock_minimum = []

        for material in low_stock_materials:
            low_stock_names.append(material.name)
            low_stock_current.append(float(material.total_stock))
            low_stock_minimum.append(float(material.min_stock_level))

        context['low_stock_names'] = json.dumps(low_stock_names)
        context['low_stock_current'] = json.dumps(low_stock_current)
        context['low_stock_minimum'] = json.dumps(low_stock_minimum)

        # 2. Material Movement Timeline Data
        # Get movement data for the last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        movements = MaterialMove.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).order_by('created_at')

        # Prepare data for timeline
        dates_dict = defaultdict(lambda: {'incoming': 0, 'outgoing': 0, 'transfers': 0})

        for movement in movements:
            date_str = movement.created_at.date().strftime('%Y-%m-%d')

            if movement.move_type in ['purchase', 'return_in']:
                dates_dict[date_str]['incoming'] += 1
            elif movement.move_type in ['sale', 'return_out']:
                dates_dict[date_str]['outgoing'] += 1
            elif movement.move_type in ['transfer', 'adjustment']:
                dates_dict[date_str]['transfers'] += 1

        # Fill in missing dates
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str not in dates_dict:
                dates_dict[date_str] = {'incoming': 0, 'outgoing': 0, 'transfers': 0}
            current_date += timedelta(days=1)

        # Sort dates
        sorted_dates = sorted(dates_dict.items())
        movement_dates = [date for date, _ in sorted_dates]
        movement_incoming = [data['incoming'] for _, data in sorted_dates]
        movement_outgoing = [data['outgoing'] for _, data in sorted_dates]
        movement_transfers = [data['transfers'] for _, data in sorted_dates]

        context['movement_dates'] = json.dumps(movement_dates)
        context['movement_incoming'] = json.dumps(movement_incoming)
        context['movement_outgoing'] = json.dumps(movement_outgoing)
        context['movement_transfers'] = json.dumps(movement_transfers)

        # Get movement types data
        movement_types_data = MaterialMove.objects.values('move_type').annotate(count=Count('id'))
        movement_types = []
        movement_type_counts = []

        move_type_display = dict(MaterialMove.MOVE_TYPES)

        for type_data in movement_types_data:
            type_code = type_data['move_type']
            movement_types.append(move_type_display.get(type_code, type_code))
            movement_type_counts.append(type_data['count'])

        context['movement_types'] = json.dumps(movement_types)
        context['movement_type_counts'] = json.dumps(movement_type_counts)

        # Get top moved materials
        top_moved_data = MaterialMove.objects.values('material__name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        top_moved_materials = []
        top_moved_counts = []

        for item in top_moved_data:
            top_moved_materials.append(item['material__name'])
            top_moved_counts.append(item['count'])

        context['top_moved_materials'] = json.dumps(top_moved_materials)
        context['top_moved_counts'] = json.dumps(top_moved_counts)

        return context

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['الكود', 'المادة', 'الفئة', 'المستودع', 'الكمية', 'الوحدة', 'الحد الأدنى', 'حالة المخزون', 'سعر التكلفة', 'القيمة الإجمالية'])

        for item in context['inventory_items']:
            if item.quantity <= 0:
                stock_status = 'نفاذ المخزون'
            elif item.quantity < item.material.min_stock_level:
                stock_status = 'منخفض'
            else:
                stock_status = 'متوفر'

            writer.writerow([
                item.material.code,
                item.material.name,
                item.material.category.name if item.material.category else '-',
                item.warehouse.name,
                item.quantity,
                item.material.unit.symbol,
                item.material.min_stock_level,
                stock_status,
                item.material.cost_price,
                item.total_value
            ])

        return response

@method_decorator(login_required, name='dispatch')
class ExportMovementReportView(MovementReportView):
    paginate_by = None  # Show all items

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="movement_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['رقم الحركة', 'المادة', 'نوع الحركة', 'الكمية', 'المستودع المصدر', 'المستودع الهدف', 'الفاتورة المرتبطة', 'التاريخ', 'المستخدم'])

        for movement in context['movements']:
            if movement.move_type == 'in':
                move_type = 'إدخال'
            elif movement.move_type == 'out':
                move_type = 'إخراج'
            elif movement.move_type == 'transfer':
                move_type = 'نقل'
            elif movement.move_type == 'adjustment':
                move_type = 'تعديل'
            else:
                move_type = movement.move_type

            writer.writerow([
                movement.id,
                movement.material.name,
                move_type,
                f"{movement.quantity} {movement.material.unit.symbol}",
                movement.source_warehouse.name if movement.source_warehouse else '-',
                movement.destination_warehouse.name if movement.destination_warehouse else '-',
                movement.reference_invoice.invoice_number if movement.reference_invoice else '-',
                movement.created_at.strftime('%Y-%m-%d %H:%M'),
                movement.created_by.username if movement.created_by else '-'
            ])

        return response

@method_decorator(login_required, name='dispatch')
class PrintMovementReportView(MovementReportView):
    template_name = 'warehouses/reports/print_movement_report.html'
    paginate_by = None  # Show all items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class ExportSalesReportView(SalesReportView):
    paginate_by = None  # Show all items

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['رقم الفاتورة', 'التاريخ', 'العميل', 'المستودع', 'المبلغ', 'حالة الدفع', 'عدد المواد'])

        for invoice in context['invoices']:
            if invoice.payment_status == 'paid':
                payment_status = 'مدفوعة'
            elif invoice.payment_status == 'partial':
                payment_status = 'مدفوعة جزئياً'
            elif invoice.payment_status == 'overdue':
                payment_status = 'متأخرة'
            else:
                payment_status = 'قيد الانتظار'

            writer.writerow([
                invoice.invoice_number,
                invoice.date.strftime('%Y-%m-%d %H:%M'),
                invoice.salesinvoice.customer.name,
                invoice.salesinvoice.warehouse.name,
                invoice.total_amount,
                payment_status,
                invoice.items.count()
            ])

        return response

@method_decorator(login_required, name='dispatch')
class PrintSalesReportView(SalesReportView):
    template_name = 'warehouses/reports/print_sales_report.html'
    paginate_by = None  # Show all items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class ExportPurchaseReportView(PurchaseReportView):
    paginate_by = None  # Show all items

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="purchase_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['رقم الفاتورة', 'التاريخ', 'المورد', 'المستودع', 'المبلغ', 'حالة الدفع', 'عدد المواد'])

        for invoice in context['invoices']:
            if invoice.payment_status == 'paid':
                payment_status = 'مدفوعة'
            elif invoice.payment_status == 'partial':
                payment_status = 'مدفوعة جزئياً'
            elif invoice.payment_status == 'overdue':
                payment_status = 'متأخرة'
            else:
                payment_status = 'قيد الانتظار'

            writer.writerow([
                invoice.invoice_number,
                invoice.date.strftime('%Y-%m-%d %H:%M'),
                invoice.purchaseinvoice.supplier.name,
                invoice.purchaseinvoice.warehouse.name,
                invoice.total_amount,
                payment_status,
                invoice.items.count()
            ])

        return response

@method_decorator(login_required, name='dispatch')
class PrintPurchaseReportView(PurchaseReportView):
    template_name = 'warehouses/reports/print_purchase_report.html'
    paginate_by = None  # Show all items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context
