# pr_tool/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('' , views.MainHR.as_view() , name="hr"),

    path('employees/' , views.ListEmployeesView.as_view() , name="employee_list"),
    path('employees/add' , views.CreateEmployeeView.as_view() , name="create_employee"),
    path('employees/<str:pk>' , views.UpdateEmployeeView.as_view() , name="employee_profile"),
    path('employees/action/' , views.EmployeesActionView.as_view() , name="employees_action"),
    path('employees/<str:pk>/delete/' , views.DeleteEmployeeView.as_view() , name="delete_employee"),

    # holidays allocated by admin to employees
    path('holidays/' , views.ListHolidaysView.as_view() , name="holidays_list"),
    path('holidays/action' , views.HolidaysActionView.as_view() , name="holidays_action"),
    path('holidays/add' , views.CreateHolidayView.as_view() , name="create_holiday"),
    path('holidays/<str:pk>' , views.UpdateHolidayView.as_view() , name="holiday_info"),
    path('holidays/<str:pk>/delete' , views.DeleteHolidayView.as_view() , name="delete_holiday"),

    # extra work
    path('extras/' , views.ListExtraWorkView.as_view() , name="extras"),
    path('extras/action' , views.ExtraWorkActionView.as_view() , name="extras_action"),
    path('extras/add' , views.CreateExtraWorkView.as_view() , name="create_extra"),
    path('extras/<str:pk>' , views.UpdateExtraWorkView.as_view() , name="extra_info"),
    path('extras/<str:pk>/delete' , views.DeleteExtraWorkView.as_view() , name="delete_extra"),

    # Recruitment to store info about recruiters and thier interview process
    path('recruiters/' , views.ListRecruitersView.as_view() , name="recruiters_list"),
    path('recruiters/action' , views.RecruitersActionView.as_view() , name="recruiters_action"),
    path('recruiters/<str:pk>' , views.RecruiterProfileView.as_view() , name="recruiter_profile"),
    path('recruiters/<str:pk>/delete' , views.DeleteRecruiterView.as_view() , name="delete_recruiter"),

    # Development Tracking
    path('goals-skills/' , views.GoalsSkillsView.as_view() , name="goals_skills"),
    path('goals/' , views.ListGoalsView.as_view() , name="goals_list"),
    path('goals/action' , views.GoalsActionView.as_view() , name="goals_action"),
    path('goals/<str:pk>' , views.GoalDetailView.as_view() , name="goal_info"),
    path('goals/add' , views.CreateGoalView.as_view() , name="create_goal"),
    path('goals/<str:pk>/delete' , views.DeleteGoalView.as_view() , name="delete_goal"),

    # Development Tracking
    path('additions_discounts/' , views.ListAdditionsDiscountsView.as_view() , name="additions_discounts"),
    path('additions_discounts/action' , views.AdditionsDiscountsActionView.as_view() , name="additions_discounts_action"),
    path('additions_discounts/add' , views.CreateAdditionDiscountView.as_view() , name="create_addition_discount"),
    path('additions_discounts/<str:pk>' , views.AdditionDiscountDetailView.as_view() , name="addition_discount_info"),
    path('additions_discounts/<str:pk>/delete' , views.DeleteAdditionDiscountView.as_view() , name="delete_addition_discount"),

    path('skills/' , views.ListSkillsView.as_view() , name="skills_list"),
    path('skills/action' , views.SkillsActionView.as_view() , name="skills_action"),
    path('skills/<str:pk>' , views.SkillDetailView.as_view() , name="skill_info"),
    path('skills/add' , views.CreateSkillView.as_view() , name="create_skill"),
    path('skills/<str:pk>/delete' , views.DeleteSkillView.as_view() , name="delete_skill"),

    path('departments/' , views.ListDepartmentsView.as_view() , name="departments"),
    path('departments/add' , views.CreateDepartmentView.as_view() , name="create_department"),
    path('departments/action' , views.DepartmentsActionView.as_view() , name="departments_action"),
    path('departments/<str:pk>' , views.DepartmentDetailView.as_view() , name="department_info"),
    path('departments/<str:pk>/delete' , views.DeleteDepartmentView.as_view() , name="delete_department"),

    path('positions/' , views.ListPositionsView.as_view() , name="positions"),
    path('positions/add' , views.CreatePositionView.as_view() , name="create_position"),
    path('positions/action' , views.PositionsActionView.as_view() , name="positions_action"),
    path('positions/<str:pk>' , views.PositionDetailView.as_view() , name="position_info"),
    path('positions/<str:pk>/delete' , views.DeletePositionView.as_view() , name="delete_position"),

    path('courses/' , views.ListCoursesView.as_view() , name="courses"),
    path('courses/add' , views.CreateCourseView.as_view() , name="create_course"),
    path('courses/add/employee/<str:id>' , views.CreateCourseEmployeeView.as_view() , name="create_course_employee"),
    path('courses/action' , views.CoursesActionView.as_view() , name="courses_action"),
    path('courses/<str:id>' , views.CourseDetailView.as_view() , name="course_info"),
    path('courses/<str:id>/delete' , views.DeleteCourseView.as_view() , name="delete_course"),

    path('loans/' , views.ListHRLoansView.as_view() , name="hr_loans"),
    path('loans/add' , views.CreateHRLoanView.as_view() , name="create_hr_loan"),
    path('loans/action' , views.HRLoansActionView.as_view() , name="hr_loans_action"),
    path('loans/<str:pk>' , views.HRLoanDetailView.as_view() , name="hr_loan_info"),
    path('loans/<str:pk>/delete' , views.DeleteHRLoanView.as_view() , name="delete_hr_loan"),

    path('hr_settings/' , views.SettingsView.as_view() , name="hr_settings")
    
]
