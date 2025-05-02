from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from hr_tool.models import Employee
# Create your views here.

class EmployeeHoursView(APIView):
    def get(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            work_hours = employee.department.work_hours
            return Response({"work_hours": work_hours}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
