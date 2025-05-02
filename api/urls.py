from django.contrib import admin
from django.urls import path, include
from .views import EmployeeHoursView

urlpatterns = [
    path('emp-hours/<int:id>/', EmployeeHoursView.as_view(), name='emp-hours'),
]
