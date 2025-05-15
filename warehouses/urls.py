from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainWarehouseView.as_view(), name='warehouses'),
]

