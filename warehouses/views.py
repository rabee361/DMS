from django.shortcuts import render
from django.views import View


class MainWarehouseView(View):
    def get(self, request):
        return render(request, 'warehouses/warehouses.html')