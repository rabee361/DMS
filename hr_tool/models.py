from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator
from utility.types import *
from django.core.validators import RegexValidator
User = get_user_model()




class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=50, null=True, blank=True)
    parts = models.CharField(max_length=50, null=True, blank=True)
    parts_relation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class ExchangePrice(models.Model):
    first_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='first_currency')
    second_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='second_currency')
    price = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_currency.name}-{self.second_currency.name}-{self.price}'


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
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='position_currency',null=True,blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name






class   Employee(User):
    position = models.ForeignKey(Position , on_delete=models.CASCADE , blank=True , null=True)
    department = models.ForeignKey(Department , on_delete=models.CASCADE , blank=True , null=True)
    address = models.CharField(max_length=100)
    base_salary = models.FloatField(validators=[MinValueValidator(0)])
    social_status = models.CharField(max_length=50,choices=SocialStatus)
    start_date = models.DateField(null=True , blank=True)
    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'

    def __str__(self) -> str:
        return self.username
    



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

    def __str__(self) -> str:
        return f'{self.employee.username}'



class Absence(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, choices=Absence,default='_')
    start = models.DateField()
    end = models.DateField()

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