from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import Task
from django.db.models import QuerySet
from typing import Any
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import user_passes_test
import json
from django.utils.decorators import method_decorator
from utility.permissioms import data_criteria_add_perm, data_criteria_delete_perm, data_criteria_edit_perm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@method_decorator([csrf_exempt, user_passes_test(data_criteria_edit_perm)], name='dispatch')
class TaskStatusUpdate(View):
    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        
        # Get the status from HTMX request
        data = json.loads(request.body.decode('utf-8'))
        new_status = data.get('status')
        print(new_status)
        if new_status in ['Pending', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)

@method_decorator(user_passes_test(data_criteria_add_perm), name='dispatch')
class TaskList(ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if self.request.htmx:
            self.template_name = 'partials/tasks_partial.html'
        if q:
            return super().get_queryset().filter(title__istartswith=q)
        else:
            return super().get_queryset()

@method_decorator(user_passes_test(data_criteria_add_perm), name='dispatch')
class TaskKanban(View):
    def get(self, request):
        tasks = Task.objects.all()
        
        # Handle filter parameters
        priority = request.GET.get('priority', None)
        user_filter = request.GET.get('user', None)
        sort_by = request.GET.get('sort_by', None)
        sort_direction = request.GET.get('sort_direction', 'asc')
        search = request.GET.get('search', None)
        
        # Apply filters
        if priority and priority != 'all':
            tasks = tasks.filter(priority=priority)
            
        if user_filter and user_filter != 'all':
            tasks = tasks.filter(user__username=user_filter)
            
        if search:
            tasks = tasks.filter(title__icontains=search) | tasks.filter(description__icontains=search)
        
        # Apply sorting
        if sort_by:
            order_by = sort_by
            if sort_by == 'user':
                order_by = 'user__username'
                
            if sort_direction == 'desc':
                order_by = f'-{order_by}'
                
            tasks = tasks.order_by(order_by)
        
        context = {
            'tasks': tasks,
            'filters': {
                'priority': priority or 'all',
                'user': user_filter or 'all',
                'sort_by': sort_by or 'title',
                'sort_direction': sort_direction,
                'search': search or ''
            }
        }
        
        # Check if request is from htmx
        if request.headers.get('HX-Request'):
            return render(request, 'partials/tasks_kanban_partial.html', context)
            
        return render(request, 'tasks/tasks_kanban.html', context)

@method_decorator(user_passes_test(data_criteria_add_perm), name='dispatch')
class TaskCreate(CreateView):
    model = Task
    template_name = 'tasks/add_task.html'
    fields = ['title', 'description','user' ,'priority', 'status']
    success_url = reverse_lazy('tasks-list')

@method_decorator(user_passes_test(data_criteria_edit_perm), name='dispatch')
class TaskUpdate(UpdateView):
    model = Task
    template_name = 'tasks/task_info.html'
    fields = ['title', 'description', 'priority', 'status']
    success_url = reverse_lazy('tasks-list')

@method_decorator(user_passes_test(data_criteria_delete_perm), name='dispatch')
class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks-list') 

@method_decorator(user_passes_test(data_criteria_delete_perm), name='dispatch')
class TaskAction(DeleteView): # override
    def post(self,request):
        selected_ids = json.loads(request.POST.get('selected_ids'))
        tasks = Task.objects.filter(id__in=selected_ids)

        # perform DB operation depending on the chosen action
        if request.POST.get('action') == 'delete':
            tasks.delete()
        return redirect('tasks-list')
