from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator
from utility.types import *
from django.core.validators import RegexValidator
from finance.models import Currency
User = get_user_model()





class Payroll(models.Model):
    employee = models.ForeignKey('Employee' , on_delete=models.CASCADE)
    leaves = models.FloatField()
    base_salary = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.employee.username}-{self.amount}'




class Department(models.Model):
    name = models.CharField(max_length=100)
    work_hours = models.FloatField()
    work_day_friday = models.BooleanField(default=False)
    work_day_tuesday = models.BooleanField(default=False)
    work_day_thursday = models.BooleanField(default=False)
    work_day_wednesday = models.BooleanField(default=False)
    work_day_monday = models.BooleanField(default=False)
    work_day_sunday = models.BooleanField(default=False)
    work_day_saturday = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)
    default_salary = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='position_currency',null=True,blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name




class Employee(User):
    position = models.ForeignKey(Position , on_delete=models.CASCADE , blank=True , null=True)
    department = models.ForeignKey(Department , on_delete=models.CASCADE , blank=True , null=True)
    address = models.CharField(max_length=100)
    base_salary = models.FloatField(validators=[MinValueValidator(0)])
    salary_currency = models.ForeignKey(Currency , on_delete=models.CASCADE , blank=True , null=True)
    social_status = models.CharField(max_length=50,choices=SocialStatus)
    start_date = models.DateField(null=True , blank=True)
    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self) -> str:
        return self.username



class AdditionDiscount(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    value = models.FloatField()
    type = models.CharField(max_length=100,choices=AdditionDiscountType)
    currency = models.ForeignKey(Currency , on_delete=models.CASCADE , blank=True , null=True)
    start = models.DateField()
    end = models.DateField()
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.employee.username} - {self.value}'




class EmployeeCertificate(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    grade = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.employee.username} - {self.university}'




class Holiday(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    days = models.FloatField(validators=[MinValueValidator(0)])
    start = models.DateField()
    paid = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    @property
    def hours(self):
        return self.days * self.employee.department.work_hours
    
    @property
    def holiday_discount(self):
        return (self.employee.base_salary / 30) * self.days

    def __str__(self) -> str:
        return f'{self.employee.username}'



class ExtraWork(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    days = models.FloatField(validators=[MinValueValidator(0)])
    start = models.DateField()
    notes = models.TextField(blank=True,null=True)
    value_per_hour = models.FloatField(validators=[MinValueValidator(0)])
    currency = models.ForeignKey(Currency , on_delete=models.CASCADE , blank=True , null=True)

    @property
    def total_extra_work_value(self):
        return self.value_per_hour * self.days

    def __str__(self) -> str:
        return f'{self.employee.username} - {self.days}'




class Recruitment(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    state = models.CharField(max_length=30 , choices=State)
    image = models.ImageField(upload_to='recruiters/images', default='placeholder.jpg')
    position = models.ForeignKey(Position , on_delete=models.CASCADE , blank=True , null=True)
    department = models.ForeignKey(Department , on_delete=models.CASCADE , blank=True , null=True)
    resume = models.FileField(upload_to='recruitment/resumes',blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Skill(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name



class WorkGoal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill , on_delete=models.CASCADE) # modify the on_delete
    created = models.DateField(auto_now_add=True)
    progress = models.CharField(max_length=20 , choices=Progress ,default="0%")

    def __str__(self) -> str:
        return f"{self.employee.username} - {self.skill}"




class HRSettings(models.Model):
    date_format = models.CharField(max_length=20 , choices=DateFormat , default=DateFormat.DMY)
    time_format = models.CharField(max_length=100 , choices=TimeFormat , default=TimeFormat.TWELVE_HOUR)
    language = models.CharField(max_length=100 , choices=Language , default=Language.ENGLISH)
    days_in_month = models.IntegerField(validators=[MinValueValidator(1) , MaxValueValidator(31)] , default=28)

    def __str__(self) -> str:
        return self.name