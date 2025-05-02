from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from documents.models import Document, DocumentGroup
from users.models import User
from form_builder.models import CustomForm
from tasks.models import Task
from hr_tool.models import Employee
from form_builder.form_utils import create_dynamic_form
from form_builder.cursor_db import insert_record_with_fields
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self,request):
        total_documents = Document.objects.count()
        total_groups = DocumentGroup.objects.count()
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        total_forms = CustomForm.objects.count()
        total_tasks = Task.objects.count()
        total_finished_tasks = Task.objects.filter(status='finished').count()
        total_employees = Employee.objects.count()
        return render(request , 'dashboard.html', {'total_documents': total_documents, 'total_groups': total_groups, 'total_users': total_users, 'active_users': active_users, 'total_forms': total_forms, 'total_tasks': total_tasks, 'total_finished_tasks': total_finished_tasks, 'total_employees': total_employees})


class FormView(View):
    def get(self, request, slug):
        custom_form = CustomForm.objects.get(slug=slug)
        form_name = custom_form.name
        
        # Create a dynamic form based on table structure
        DynamicForm = create_dynamic_form(form_name)
        form = DynamicForm()
        context = {
            'form': form,
            'form_name': form_name,
            'form_id': custom_form.id,
            'logo': custom_form.logo,
            'active_tab': '1'  # Always show first tab for new forms or after submission
        }
        
        if custom_form.template == '1':
            return render(request, 'form_builder/form_view.html', context)
        elif custom_form.template == '2':
            return render(request, 'form_builder/form_view2.html', context)


    def post(self, request, slug):
        try:
            custom_form = CustomForm.objects.get(slug=slug)
            form_name = custom_form.name
            
            # Create dynamic form and validate data
            DynamicForm = create_dynamic_form(form_name)
            form = DynamicForm(request.POST)
            
            if form.is_valid():
                # Extract validated data
                cleaned_data = form.cleaned_data
                
                # Get fields and values for insertion
                fields = list(cleaned_data.keys())
                values = [cleaned_data[field] for field in fields]
                
                # Insert the record using our utility function
                insert_record_with_fields(form_name, fields, values)
                
                # Create a fresh form and pass success=True in context
                form = DynamicForm()
                context = {
                    'form': form,
                    'form_name': form_name,
                    'form_id': custom_form.id,
                    'logo': custom_form.logo,
                    'success': True,
                    'active_tab': '1'  # Show first tab after successful submission
                }
                
                if custom_form.template == '1':
                    return render(request, 'form_builder/form_view.html', context)
                elif custom_form.template == '2':
                    return render(request, 'form_builder/form_view2.html', context)
            else:
                # If form is invalid, show errors
                context = {
                    'form': form,
                    'form_name': form_name,
                    'form_id': custom_form.id,
                    'logo': custom_form.logo,
                    'active_tab': request.POST.get('active_tab', '1')  # Keep user on the same tab
                }
                
                if custom_form.template == '1':
                    return render(request, 'form_builder/form_view.html', context)
                elif custom_form.template == '2':
                    return render(request, 'form_builder/form_view2.html', context)
                
        except CustomForm.DoesNotExist:
            return redirect('form_builder')
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })




class handler404(View):
    def get(self, request):
        return render(request, '404.html')

class handler500(View):
    def get(self, request):
        return render(request, '500.html')
