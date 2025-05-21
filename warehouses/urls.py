from django.urls import path
from . import views

# Temporarily comment out other URLs until migrations are fixed
"""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.WarehouseDashboardView.as_view(), name='warehouses'),

    # Warehouses
    path('warehouses/', views.ListWarehousesView.as_view(), name='warehouse_list'),
    path('warehouses/add/', views.CreateWarehouseView.as_view(), name='create_warehouse'),
    path('warehouses/<int:pk>/', views.UpdateWarehouseView.as_view(), name='warehouse_detail'),
    path('warehouses/delete/<int:pk>/', views.DeleteWarehouseView.as_view(), name='delete_warehouse'),
    path('warehouses/action/', views.WarehouseActionView.as_view(), name='warehouse_action'),

    # Materials
    path('materials/', views.ListMaterialsView.as_view(), name='material_list'),
    path('materials/add/', views.CreateMaterialView.as_view(), name='create_material'),
    path('materials/<int:pk>/', views.UpdateMaterialView.as_view(), name='material_detail'),
    path('materials/delete/<int:pk>/', views.DeleteMaterialView.as_view(), name='delete_material'),
    path('materials/action/', views.MaterialActionView.as_view(), name='material_action'),

    # Categories
    path('categories/', views.ListCategoriesView.as_view(), name='category_list'),
    path('categories/add/', views.CreateCategoryView.as_view(), name='create_category'),
    path('categories/<int:pk>/', views.UpdateCategoryView.as_view(), name='category_detail'),
    path('categories/delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('categories/action/', views.CategoryActionView.as_view(), name='category_action'),

    # Units
    path('units/', views.ListUnitsView.as_view(), name='unit_list'),
    path('units/add/', views.CreateUnitView.as_view(), name='create_unit'),
    path('units/<int:pk>/', views.UpdateUnitView.as_view(), name='unit_detail'),
    path('units/delete/<int:pk>/', views.DeleteUnitView.as_view(), name='delete_unit'),
    path('units/action/', views.UnitActionView.as_view(), name='unit_action'),

    # Unit Conversions
    path('unit-conversions/', views.ListUnitConversionsView.as_view(), name='unit_conversion_list'),
    path('unit-conversions/add/', views.CreateUnitConversionView.as_view(), name='create_unit_conversion'),
    path('unit-conversions/<int:pk>/', views.UpdateUnitConversionView.as_view(), name='unit_conversion_detail'),
    path('unit-conversions/delete/<int:pk>/', views.DeleteUnitConversionView.as_view(), name='delete_unit_conversion'),
    path('unit-conversions/action/', views.UnitConversionActionView.as_view(), name='unit_conversion_action'),

    # Customers
    path('customers/', views.ListCustomersView.as_view(), name='customer_list'),
    path('customers/add/', views.CreateCustomerView.as_view(), name='create_customer'),
    path('customers/<int:pk>/', views.UpdateCustomerView.as_view(), name='customer_detail'),
    path('customers/delete/<int:pk>/', views.DeleteCustomerView.as_view(), name='delete_customer'),
    path('customers/action/', views.CustomerActionView.as_view(), name='customer_action'),

    # Suppliers
    path('suppliers/', views.ListSuppliersView.as_view(), name='supplier_list'),
    path('suppliers/add/', views.CreateSupplierView.as_view(), name='create_supplier'),
    path('suppliers/<int:pk>/', views.UpdateSupplierView.as_view(), name='supplier_detail'),
    path('suppliers/delete/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),
    path('suppliers/action/', views.SupplierActionView.as_view(), name='supplier_action'),

    # Invoices
    path('invoices/', views.ListInvoicesView.as_view(), name='invoice_list'),
    path('invoices/sales/add/', views.CreateSalesInvoiceView.as_view(), name='create_sales_invoice'),
    path('invoices/purchase/add/', views.CreatePurchaseInvoiceView.as_view(), name='create_purchase_invoice'),
    path('invoices/sales-return/add/', views.CreateSalesReturnInvoiceView.as_view(), name='create_sales_return_invoice'),
    path('invoices/purchase-return/add/', views.CreatePurchaseReturnInvoiceView.as_view(), name='create_purchase_return_invoice'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/delete/<int:pk>/', views.DeleteInvoiceView.as_view(), name='delete_invoice'),
    path('invoices/action/', views.InvoiceActionView.as_view(), name='invoice_action'),

    # Material Movements
    path('movements/', views.ListMaterialMovesView.as_view(), name='movement_list'),
    path('movements/add/', views.CreateMaterialMoveView.as_view(), name='create_movement'),
    path('movements/<int:pk>/', views.MaterialMoveDetailView.as_view(), name='movement_detail'),
    path('movements/delete/<int:pk>/', views.DeleteMaterialMoveView.as_view(), name='delete_movement'),
    path('movements/action/', views.MaterialMoveActionView.as_view(), name='movement_action'),

    # Reports
    path('reports/inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('reports/movements/', views.MovementReportView.as_view(), name='movement_report'),
    path('reports/sales/', views.SalesReportView.as_view(), name='sales_report'),
    path('reports/purchases/', views.PurchaseReportView.as_view(), name='purchase_report'),
]
"""

# Use dashboard view and real views for all sections
urlpatterns = [
    # # Dashboard
    # path('', views.WarehouseDashboardView.as_view(), name='warehouses'),

    # # Warehouses list - Direct access at /dms/warehouses/warehouses/
    # path('warehouses/', views.ListWarehousesView.as_view(), name='warehouses_list'),

    # # Materials - Real views
    # path('materials/', views.ListMaterialsView.as_view(), name='materials'),
    # path('materials/add/', views.CreateMaterialView.as_view(), name='create_material'),
    # path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    # path('materials/<int:pk>/edit/', views.UpdateMaterialView.as_view(), name='update_material'),
    # path('materials/delete/<int:pk>/', views.DeleteMaterialView.as_view(), name='delete_material'),
    # path('materials/action/', views.MaterialActionView.as_view(), name='material_action'),

    # # Categories - Real views
    # path('categories/', views.ListCategoriesView.as_view(), name='categories'),
    # path('categories/add/', views.CreateCategoryView.as_view(), name='create_category'),
    # path('categories/<int:pk>/', views.UpdateCategoryView.as_view(), name='category_detail'),
    # path('categories/delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete_category'),
    # path('categories/action/', views.CategoryActionView.as_view(), name='category_action'),

    # # Units - Real views
    # path('units/', views.ListUnitsView.as_view(), name='units'),
    # path('units/add/', views.CreateUnitView.as_view(), name='create_unit'),
    # path('units/<int:pk>/', views.UpdateUnitView.as_view(), name='unit_detail'),
    # path('units/delete/<int:pk>/', views.DeleteUnitView.as_view(), name='delete_unit'),
    # path('units/action/', views.UnitActionView.as_view(), name='unit_action'),
    # path('unit-conversions/', views.UnitConversionsView.as_view(), name='unit_conversions'),

    # # Warehouses - Real views (moved to /warehouses/ for direct access)
    # path('warehouses/add/', views.CreateWarehouseView.as_view(), name='create_warehouse'),
    # path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    # path('warehouses/<int:pk>/edit/', views.UpdateWarehouseView.as_view(), name='update_warehouse'),
    # path('warehouses/delete/<int:pk>/', views.DeleteWarehouseView.as_view(), name='delete_warehouse'),
    # path('warehouses/action/', views.WarehouseActionView.as_view(), name='warehouse_action'),

    # # Customers - Real views
    # path('customers/', views.ListCustomersView.as_view(), name='customers'),
    # path('customers/add/', views.CreateCustomerView.as_view(), name='create_customer'),
    # path('customers/<int:pk>/', views.UpdateCustomerView.as_view(), name='customer_detail'),
    # path('customers/delete/<int:pk>/', views.DeleteCustomerView.as_view(), name='delete_customer'),
    # path('customers/action/', views.CustomerActionView.as_view(), name='customer_action'),

    # # Suppliers - Real views
    # path('suppliers/', views.ListSuppliersView.as_view(), name='suppliers'),
    # path('suppliers/add/', views.CreateSupplierView.as_view(), name='create_supplier'),
    # path('suppliers/<int:pk>/', views.UpdateSupplierView.as_view(), name='supplier_detail'),
    # path('suppliers/delete/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),
    # path('suppliers/action/', views.SupplierActionView.as_view(), name='supplier_action'),

    # # Invoices - Real views
    # path('invoices/', views.ListInvoicesView.as_view(), name='invoices'),
    # path('invoices/sales/add/', views.CreateSalesInvoiceView.as_view(), name='create_sales_invoice'),
    # path('invoices/purchase/add/', views.CreatePurchaseInvoiceView.as_view(), name='create_purchase_invoice'),
    # path('invoices/sales-return/add/', views.InvoicesPlaceholderView.as_view(), name='create_sales_return_invoice'),
    # path('invoices/purchase-return/add/', views.InvoicesPlaceholderView.as_view(), name='create_purchase_return_invoice'),
    # path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    # path('invoices/delete/<int:pk>/', views.DeleteInvoiceView.as_view(), name='delete_invoice'),
    # path('invoices/print/<int:pk>/', views.PrintInvoiceView.as_view(), name='print_invoice'),
    # path('invoices/status/<int:pk>/', views.UpdateInvoiceStatusView.as_view(), name='update_invoice_status'),
    # path('invoices/action/', views.InvoiceActionView.as_view(), name='invoice_action'),

    # # Material Movements - Real views
    # path('movements/', views.ListMovementsView.as_view(), name='movements'),
    # path('movements/add/', views.CreateMovementView.as_view(), name='create_movement'),
    # path('movements/<int:pk>/', views.MovementDetailView.as_view(), name='movement_detail'),
    # path('movements/delete/<int:pk>/', views.DeleteMovementView.as_view(), name='delete_movement'),
    # path('movements/action/', views.MovementActionView.as_view(), name='movement_action'),

    # # Reports - Real views
    # path('reports/', views.ReportsView.as_view(), name='reports'),

    # # Advanced Visualizations
    # path('visualizations/', views.VisualizationDashboardView.as_view(), name='visualizations'),
    # path('visualizations/heatmap/', views.WarehouseHeatmapView.as_view(), name='warehouse_heatmap'),
    # path('visualizations/timeline/', views.MaterialTimelineView.as_view(), name='material_timeline'),

    # # Inventory reports
    # path('reports/inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    # path('reports/inventory/print/', views.PrintInventoryReportView.as_view(), name='print_inventory_report'),
    # path('reports/inventory/export/', views.ExportInventoryReportView.as_view(), name='export_inventory_report'),

    # # Movement reports
    # path('reports/movement/', views.MovementReportView.as_view(), name='movement_report'),
    # path('reports/movement/print/', views.PrintMovementReportView.as_view(), name='print_movement_report'),
    # path('reports/movement/export/', views.ExportMovementReportView.as_view(), name='export_movement_report'),

    # # Sales reports
    # path('reports/sales/', views.SalesReportView.as_view(), name='sales_report'),
    # path('reports/sales/print/', views.PrintSalesReportView.as_view(), name='print_sales_report'),
    # path('reports/sales/export/', views.ExportSalesReportView.as_view(), name='export_sales_report'),

    # # Purchase reports
    # path('reports/purchase/', views.PurchaseReportView.as_view(), name='purchase_report'),
    # path('reports/purchase/print/', views.PrintPurchaseReportView.as_view(), name='print_purchase_report'),
    # path('reports/purchase/export/', views.ExportPurchaseReportView.as_view(), name='export_purchase_report'),
]
