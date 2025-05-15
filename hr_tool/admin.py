from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(Holiday)
admin.site.register(Skill)
admin.site.register(WorkGoal)
admin.site.register(Recruitment)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(EmployeeCertificate)
admin.site.register(Payroll)

