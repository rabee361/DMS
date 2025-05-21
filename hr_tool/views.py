# hr_tool/views.py
from typing import Any
import json
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from .forms import *
# from users.models import User
from .forms import EmployeeRegistrationForm , EmployeeUpdateForm , HolidayForm , WorkGoalForm , HRSettingsForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
import datetime
from django.http import HttpResponse
from django.urls import reverse_lazy
from .resources import EmployeeResource, HolidayResource, RecruitmentResource
from utility.permissioms import hr_criteria_add_perm, hr_criteria_delete_perm, hr_criteria_edit_perm
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from utility.helper import change_format, reverse_format
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

User = get_user_model()


@method_decorator(user_passes_test(hr_criteria_add_perm, login_url='401'), name='dispatch')
class MainHR(View):
    def get(self, request):
        total_holidays = Holiday.objects.count()
        total_additions_discounts = AdditionDiscount.objects.count()
        total_employees = Employee.objects.count()
        total_hr_loans = HRLoan.objects.count()
        total_extras = ExtraWork.objects.count()
        active_employees = Employee.objects.filter(is_active=True).count()
        approved_holidays = Holiday.objects.filter(accepted=True).count()
        total_recruiters = Recruitment.objects.count()
        total_goals = WorkGoal.objects.count()
        total_skills = Skill.objects.count()
        total_courses = Skill.objects.count()
        total_departments = Department.objects.count()
        total_positions = Position.objects.count()
        return render(request, 'hr_tool/HR.html', {
            'total_holidays': total_holidays,
            'total_additions_discounts': total_additions_discounts,
            'total_extras': total_extras,
            'total_employees': total_employees,
            'active_employees': active_employees,
            'approved_holidays': approved_holidays,
            'total_recruiters': total_recruiters,
            'total_goals': total_goals,
            'total_skills': total_skills, 
            'total_courses': total_courses, 
            'total_departments': total_departments,
            'total_positions': total_positions,
            'total_hr_loans': total_hr_loans
        })


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListEmployeesView(ListView):
    model = Employee
    template_name = 'hr_tool/employee/employees.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'partials/employees_partial.html'
            if q:
                return super().get_queryset().filter(username__icontains=q)
        else:
            return super().get_queryset()


@method_decorator(user_passes_test(hr_criteria_add_perm, login_url='401'), name='dispatch')
class CreateEmployeeView(CreateView):
    model = Employee
    form_class = EmployeeRegistrationForm
    template_name = 'hr_tool/employee/create_employee.html'
    success_url = '/dms/hr/employees/'

    def form_invalid(self, form):
        # Print form errors for debugging
        print(form.errors)
        return super().form_invalid(form)


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteEmployeeView(DeleteView):
    model = Employee
    template_name = 'hr_tool/employee/delete_employee.html'
    context_object_name = 'employee'
    success_url = reverse_lazy('employee_list')


@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class UpdateEmployeeView(UpdateView):
    model = Employee
    template_name = 'hr_tool/employee/employee_profile.html'
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('employee_list')

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
        print("VVVVVVVVVVVVVVVVVVVV")
        return super().form_invalid(form)

    # add extra data for each employee in the context
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        holidays = Holiday.objects.filter(employee=self.object).count()  # get number of holidays for the employee
        context['holidays'] = holidays
        return context


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class EmployeesActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        employees = Employee.objects.filter(id__in=selected_items)

        if request.POST.get('action') == 'delete':
            employees.delete()

        if request.POST.get('action') == 'activate':
            employees.update(is_active=True)

        if request.POST.get('action') == 'deactivate':
            employees.update(is_active=False)

        elif request.POST.get('action') == 'export_excel':
            employee_resource = EmployeeResource()
            dataset = employee_resource.export(employees)
            dataset = dataset.export(format='xlsx')
            response = HttpResponse(
                dataset,
                content_type='application/vnd.ms-excel'
            )
            response['Content-Disposition'] = f'attachment; filename="employees_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
            return response

        return redirect('employee_list')


@method_decorator([login_required, user_passes_test(hr_criteria_add_perm)], name='dispatch')
class CreateHolidayView(View):
    def get(self, request):
        form = HolidayForm()
        return render(request, 'hr_tool/holiday/holiday_form.html', {'form': form})

    def post(self, request):
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save(commit=False)
            holiday.save()
            return redirect('holidays_list')
        return redirect('create_holiday')


@method_decorator([login_required, user_passes_test(hr_criteria_add_perm)], name='dispatch')
class ListHolidaysView(ListView):
    model = Holiday
    template_name = 'hr_tool/holiday/holidays.html'
    context_object_name = 'holidays'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'partials/holidays_partial.html'
            if q:
                return super().get_queryset().filter(username__icontains=q)
        else:
            return super().get_queryset()




@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class HolidaysActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        holidays = Holiday.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            holidays.delete()

        if request.POST.get('action') == 'accept':
            holidays.update(accepted=True)

        if request.POST.get('action') == 'reject':
            holidays.update(accepted=False)

        elif request.POST.get('action') == 'export_excel':
            holiday_resource = HolidayResource()
            dataset = holiday_resource.export(holidays)
            dataset = dataset.export(format='xlsx')
            response = HttpResponse(
                dataset,
                content_type='application/vnd.ms-excel'
            )
            response['Content-Disposition'] = f'attachment; filename="holidays_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
            return response

        return redirect('holidays_list')


@method_decorator([login_required, user_passes_test(hr_criteria_edit_perm)], name='dispatch')
class UpdateHolidayView(View):
    def get(self, request, pk):
        holiday = Holiday.objects.get(id=pk)
        form = HolidayForm(instance=holiday)
        context = {
            'form': form,
            'hours': holiday.hours
        }
        return render(request, 'hr_tool/holiday/holiday_form.html', context)

    def post(self, request, pk):
        form = HolidayForm(request.POST, instance=Holiday.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('holidays_list')
        return redirect('holiday_info')


@method_decorator([login_required, user_passes_test(hr_criteria_delete_perm)], name='dispatch')
class DeleteHolidayView(DeleteView):
    model = Holiday
    template_name = 'hr_tool/holiday/delete_holiday.html'
    context_object_name = 'holiday'
    success_url = reverse_lazy('holidays_list')




@method_decorator([login_required, user_passes_test(hr_criteria_add_perm)], name='dispatch')
class ListExtraWorkView(ListView):
    model = ExtraWork
    template_name = 'hr_tool/extra/extras.html'
    context_object_name = 'extras'
    paginate_by = 10

@method_decorator([login_required, user_passes_test(hr_criteria_add_perm)], name='dispatch')
class CreateExtraWorkView(CreateView):
    model = ExtraWork
    form_class = ExtraWorkForm
    template_name = 'hr_tool/extra/extra_form.html'
    success_url = reverse_lazy('extras')

@method_decorator([login_required, user_passes_test(hr_criteria_edit_perm)], name='dispatch')
class UpdateExtraWorkView(UpdateView):
    model = ExtraWork
    form_class = ExtraWorkForm
    template_name = 'hr_tool/extra/extra_form.html'
    success_url = reverse_lazy('extras')

@method_decorator([login_required, user_passes_test(hr_criteria_delete_perm)], name='dispatch')
class DeleteExtraWorkView(DeleteView):
    model = ExtraWork
    template_name = 'hr_tool/extra/delete_extra.html'
    success_url = reverse_lazy('extras')

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class ExtraWorkActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids', '[]'))
        extra_works = ExtraWork.objects.filter(id__in=selected_items)

        if request.POST.get('action') == 'delete':
            extra_works.delete()

        return redirect('extras')


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListRecruitersView(ListView):
    model = Recruitment
    template_name = 'hr_tool/recruitment/list_recruiters.html'
    context_object_name = 'recruiters'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                first_name__startswith=q
            )
        return queryset


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class RecruitersActionView(View):
    def post(self, request):
        selected_ids = json.loads(request.POST.get('selected_ids'))
        recruiters = Recruitment.objects.filter(id__in=selected_ids)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            recruiters.delete()

        elif request.POST.get('action') == 'export_excel':
            recruiter_resource = RecruitmentResource()
            dataset = recruiter_resource.export(recruiters)
            dataset = dataset.export(format='xlsx')

            response = HttpResponse(
                dataset,
                content_type='application/vnd.ms-excel'
            )
            response['Content-Disposition'] = f'attachment; filename="recruiters_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
            return response

        return redirect('recruiters_list')


@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class RecruiterProfileView(UpdateView):
    model = Recruitment
    template_name = 'hr_tool/recruitment/recruiter_profile.html'
    success_url = reverse_lazy('recruiters_list')
    context_object_name = 'recruiter'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteRecruiterView(DeleteView):
    model = Recruitment
    template_name = 'hr_tool/recruitment/delete_recruite.html'
    success_url = reverse_lazy('recruiters_list')
    context_object_name = 'recruiter'


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListGoalsView(ListView):
    model = WorkGoal
    template_name = 'hr_tool/goals/goals.html'
    context_object_name = 'goals'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                employee__username__startswith=q
            )
        return queryset


class GoalsSkillsView(View):
    def get(self, request):
        return render(request, 'hr_tool/goals/goals_skills.html')


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateGoalView(CreateView):
    model = WorkGoal
    template_name = 'hr_tool/goals/create_goal.html'
    success_url = reverse_lazy('goals_skills')
    form_class = WorkGoalForm


@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class GoalDetailView(UpdateView):
    model = WorkGoal
    template_name = 'hr_tool/goals/goal_detail.html'
    context_object_name = 'goal'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteGoalView(DeleteView):
    model = WorkGoal
    template_name = 'hr_tool/goals/delete_goal.html'
    success_url = reverse_lazy('goals_list')
    context_object_name = 'goal'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class GoalsActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        goals = WorkGoal.objects.filter(id__in=selected_items)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            goals.delete()
        return redirect('goals_list')



class ListAdditionsDiscountsView(ListView):
    model = AdditionDiscount
    template_name = 'hr_tool/addition_discount/additions_discounts.html'
    context_object_name = 'additions_discounts'
    paginate_by = 10


class CreateAdditionDiscountView(CreateView):
    model = AdditionDiscount
    form_class = AdditionDiscountForm
    template_name = 'hr_tool/addition_discount/addition_discount_form.html'
    success_url = reverse_lazy('additions_discounts')


class AdditionDiscountDetailView(UpdateView):
    model = AdditionDiscount
    form_class = AdditionDiscountForm
    template_name = 'hr_tool/addition_discount/addition_discount_form.html'
    success_url = reverse_lazy('additions_discounts')


class DeleteAdditionDiscountView(DeleteView):
    model = AdditionDiscount
    template_name = 'hr_tool/addition_discount/delete_addition_discount.html'
    success_url = reverse_lazy('additions_discounts')


class AdditionsDiscountsActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        additions = AdditionDiscount.objects.filter(id__in=selected_items)
        if request.POST.get('action') == 'delete':
            additions.delete()
        return redirect('additions_discounts')



@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListSkillsView(ListView):
    model = Skill
    template_name = 'hr_tool/goals/skills.html'
    context_object_name = 'skills'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                name__startswith=q
            )
        return queryset


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateSkillView(CreateView):
    model = Skill
    fields = ['name']
    template_name = 'hr_tool/goals/create_skill.html'
    success_url = reverse_lazy('skills_list')


@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class SkillDetailView(UpdateView):
    model = Skill
    template_name = 'hr_tool/goals/skill_detail.html'
    context_object_name = 'skill'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteSkillView(DeleteView):
    model = Skill
    template_name = 'hr_tool/goals/delete_skill.html'
    success_url = reverse_lazy('skills_list')
    context_object_name = 'skill'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class SkillsActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        skills = Skill.objects.filter(id__in=selected_items)
        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            skills.delete()
        return redirect('skills_list')


class SettingsView(View):
    def get(self, request):
        settings_instance = HRSettings.objects.first()
        form = HRSettingsForm(instance=settings_instance)
        return render(request, 'hr_tool/hr_settings.html', {'form': form})

    def post(self, request):
        form = HRSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_settings')
        return redirect('hr_settings')


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListDepartmentsView(ListView):
    model = Department
    template_name = 'hr_tool/departments/departments.html'
    context_object_name = 'departments'
    paginate_by = 10

@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateDepartmentView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'hr_tool/departments/department_form.html'
    success_url = reverse_lazy('departments')

@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class DepartmentDetailView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'hr_tool/departments/department_form.html'
    context_object_name = 'department'
    success_url = reverse_lazy('departments')

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteDepartmentView(DeleteView):
    model = Department
    template_name = 'hr_tool/departments/delete_department.html'
    success_url = reverse_lazy('departments')
    context_object_name = 'department'

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DepartmentsActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        departments = Department.objects.filter(id__in=selected_items)
        if request.POST.get('action') == 'delete':
            departments.delete()
        return redirect('departments_list')


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListPositionsView(ListView):
    model = Position
    template_name = 'hr_tool/positions/positions.html'
    context_object_name = 'positions'
    paginate_by = 10

@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreatePositionView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'hr_tool/positions/position_form.html'
    success_url = reverse_lazy('positions')

@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class PositionDetailView(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'hr_tool/positions/position_form.html'
    context_object_name = 'position'
    success_url = reverse_lazy('positions')

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeletePositionView(DeleteView):
    model = Position
    template_name = 'hr_tool/positions/delete_position.html'
    success_url = reverse_lazy('positions')
    context_object_name = 'position'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class PositionsActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        positions = Position.objects.filter(id__in=selected_items)
        if request.POST.get('action') == 'delete':
            positions.delete()
        return redirect('positions_list')





@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListCoursesView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'hr_tool/courses/courses.html'
    paginate_by = 10

@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateCourseView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'hr_tool/courses/course_form.html'
    success_url = reverse_lazy('courses')



@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateCourseEmployeeView(View):
    def get(self, request):
        return render(request , 'hr_tool/courses/course_form.html')

    def post(self, request):
        return redirect('courses')


class ListCourseEmployeeView(ListView):
    model = CourseEmployee
    context_object_name = 'course_employees'
    pk_url_kwarg = 'id'
    template_name = 'hr_tool/courses/course_employees.html'
    paginate_by = 10



@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class DeleteCourseEmployeeView(DeleteView):
    model = CourseEmployee
    success_url = reverse_lazy('courses')
    pk_url_kwarg =  'id'
    context_object_name = 'course_employee'


@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class AddCourseEmployeeView(View):
    def post(self, request):
        course_id = request.POST.get('course')
        employee_id = request.POST.get('employee')
        course = Course.objects.get_or_404(id=course_id)
        employee = Employee.objects.get_or_404(id=employee_id)
        course.employees.add(employee)
        return redirect('courses')



@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class CourseDetailView(View):
    def get(self, request, id):
        course = get_object_or_404(Course, pk=id)
        employees = CourseEmployee.objects.filter(course=course)
        form = CourseForm(instance=course)
        return render(request, 'hr_tool/courses/course_form.html', {'form': form , 'employees':employees})

    def post(self, request, id):
        employee_id = request.POST.get('employee')
        course = get_object_or_404(Course, pk=id)
        employee = get_object_or_404(Employee, pk=employee_id)
        course.employees.remove(employee)
        return redirect('courses')



@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteCourseView(DeleteView):
    model = Course
    pk_url_kwarg = 'id'
    template_name = 'hr_tool/courses/delete_course.html'
    success_url = reverse_lazy('courses')
    context_object_name = 'course'


@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class CoursesActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        courses = Course.objects.filter(id__in=selected_items)
        if request.POST.get('action') == 'delete':
            courses.delete()
        return redirect('courses')





@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class ListHRLoansView(ListView):
    model = HRLoan
    template_name = 'hr_tool/hr_loans/hr_loans.html'
    context_object_name = 'hr_loans'
    paginate_by = 10

@method_decorator(user_passes_test(hr_criteria_add_perm), name='dispatch')
class CreateHRLoanView(CreateView):
    model = HRLoan
    form_class = HRLoanForm
    template_name = 'hr_tool/hr_loans/hr_loan_form.html'
    success_url = reverse_lazy('hr_loans')

@method_decorator(user_passes_test(hr_criteria_edit_perm), name='dispatch')
class HRLoanDetailView(UpdateView):
    model = HRLoan
    form_class = HRLoanForm
    template_name = 'hr_tool/hr_loans/hr_loan_form.html'
    context_object_name = 'loan'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('hr_loans')

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class DeleteHRLoanView(DeleteView):
    def get(self, request, id):
        loan = get_object_or_404(HRLoan, pk=id)
        form = HRLoanForm(instance=loan)
        return render(request, 'hr_tool/hr_loans/hr_loan_form.html', {'form': form , 'payments':loan.payments})

    def post(self, request, id):
        loan = get_object_or_404(HRLoan, pk=id)
        loan.delete()
        return redirect('hr_loans')

@method_decorator(user_passes_test(hr_criteria_delete_perm), name='dispatch')
class HRLoansActionView(View):
    def post(self, request):
        selected_items = json.loads(request.POST.get('selected_ids'))
        loans = HRLoan.objects.filter(id__in=selected_items)
        if request.POST.get('action') == 'delete':
            loans.delete()
        return redirect('courses')


