from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListForms.as_view(), name='form_builder'),
    path('forms/add', views.CreateFormView.as_view(), name='add_form'),
    path('forms/fields/add', views.CreateFormFieldsView.as_view(), name='add_form_fields'),
    path('forms/<int:pk>/add', views.CreateRecordView.as_view(), name='add_record'),
    path('forms/<int:pk>/delete/<int:record_id>', views.DeleteRecordView.as_view(), name='delete_record'),
    path('forms/<int:pk>/update/<int:record_id>', views.UpdateRecordView.as_view(), name='update_record'),
    path('forms/<int:pk>/delete', views.DeleteFormView.as_view(), name='delete_form'),
    path('forms/view/<int:pk>/', views.FormView.as_view(), name='view_form'),
    path('forms/<int:pk>/', views.FormDetailView.as_view(), name='form_detail'),
    path('forms/action', views.FormsActionView.as_view(), name='forms_action'),
    path('forms/export/pdf/<int:pk>/', views.ExportFormPdfView.as_view(), name='export_form_pdf'),
    path('forms/export/excel/<int:pk>/', views.ExportFormExcelView.as_view(), name='export_form_excel'),
]