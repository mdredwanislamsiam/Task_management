from django.shortcuts import redirect
from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, Project
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.views import is_admin
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


User = get_user_model()


''' ------ Function based Views ------- '''

def is_manager(user):
    return user.groups.filter(name="Manager").exists()
def is_employee(user):
    return user.groups.filter(name="Employee").exists()


''' ------- class based Views -------'''


class ManagerUserTestMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_manager(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class EmployeeUserTestMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_employee(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class EmployeeDashboard(LoginRequiredMixin, EmployeeUserTestMixin, TemplateView): 
    template_name = 'dashboard/user-dashboard.html'

class ManagerDashboard(LoginRequiredMixin, ManagerUserTestMixin, ListView):
    model = Task
    template_name = 'dashboard/manager-dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        base_query = Task.objects.select_related(
            'details').prefetch_related('assigned_to')
        type = self.request.GET.get('type', 'all')
        # retriving task data
        if type == 'completed':
            tasks = base_query.filter(status='COMPLETED')
        elif type == 'in_progress':
            tasks = base_query.filter(status='IN_PROGRESS')
        elif type == 'pending':
            tasks = base_query.filter(status='PENDING')
        elif type == 'all':
            tasks = base_query.all()
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counts'] = Task.objects.aggregate(
            total_task=Count('id'),
            completed_task=Count('id', Q(status='COMPLETED')),
            in_progress_task=Count('id', Q(status='IN_PROGRESS')),
            pending_task=Count('id', Q(status='PENDING'))
        )
        return context



class TaskDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView): 
    permission_required = 'tasks.view_taskdetail'
    login_url = 'no_permission'
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs): 
        selected_status = request.POST.get('task_status')
        task = self.get_object()
        task.status = selected_status
        task.save()
        return redirect('task-detail', task.id)
    

class ViewProject(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'project.view_project' 
    login_url = 'no_permission'
    model = Project
    context_object_name = 'projects'
    template_name='show_task.html'
    def get_queryset(self):
        queryset = Project.objects.annotate(num_task = Count('tasks')).order_by('num_task')
        return queryset
    



# class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = 'tasks.add_task'
#     login_url = 'no_permission'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['task_form'] = kwargs.get('task_form', TaskModelForm())
#         context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
#         return context
        
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return render(request, 'task_form.html', context)

#     def post(self, request, *args, **kwargs):
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
#         if task_form.is_valid() and task_detail_form.is_valid():
#             '''for django model form'''
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
#             messages.success(request, "Task Created Succesfully!!")
#             return redirect('create-task')
#         context = self.get_context_data(
#             task_form=task_form,
#             task_detail_form=task_detail_form
#         )
#         return render(request, 'task_form.html', context)
    
    
class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, CreateView): 
    permission_required = 'tasks.add_task'
    login_url = "no_permission"
    
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        context['task_detail_form'] = TaskDetailModelForm()
        return context
    
    def post(self, request, *args, **kwargs): 
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            '''for django model form'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Succesfully!!")
            return redirect('create-task')
        return redirect('create-task')

# class UpdateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
#     permission_required = 'tasks.change_task'
#     login_url = 'no_permission'
    
#     def get_task(self):
#         return Task.objects.get(id=self.kwargs['id'])
    
#     def get_context_data(self, **kwargs):
#         task = self.get_task()
#         context = super().get_context_data(**kwargs)
#         context['task_form'] = kwargs.get('task_form', TaskModelForm(instance= task))
#         context['task_detail_form'] = kwargs.get(
#             'task_detail_form', TaskDetailModelForm(instance=task.details))
#         return context

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return render(request, 'task_form.html', context)

#     def post(self, request, *args, **kwargs):
#         task = self.get_task()
#         task_form = TaskModelForm(request.POST, instance=task)
#         task_detail_form = TaskDetailModelForm(
#             request.POST, request.FILES, instance=task.details)
#         if task_form.is_valid() and task_detail_form.is_valid():
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
#             messages.success(request, "Task Updated Successfully!!")
#             return redirect('update-task', id=task.id)

#         context = self.get_context_data(
#             task_form=task_form,
#             task_detail_form=task_detail_form
#         )
#         return render(request, 'task_form.html', context)


class UpdateTask(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): 
    permission_required = 'tasks.change_task'
    login_url = 'no_permission'
    
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['task_form']=self.get_form()
        if task.details: 
            context['task_detail_form'] = TaskDetailModelForm(instance = task.details)
        else: 
            context['task_detail_form'] = TaskDetailModelForm()
    
        return context
    
    def post(self, request, *args, **kwargs): 
        task = self.get_object()
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(task,'details', None))
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully!!")
            return redirect('update-task', id=task.id)

        return redirect('update-task', id = task.id)


class DeleteTask(LoginRequiredMixin, PermissionRequiredMixin, DeleteView): 
    permission_required = 'tasks.delete_task'
    login_url = 'no_permission'
    model = Task
    context_object_name = 'task'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('manager-dashboard')
    
    
class DashboardView(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs): 
        if is_manager(request.user):
            return redirect("manager-dashboard")
        elif is_employee(request.user):
            return redirect('user-dashboard')
        elif is_admin(request.user):
            return redirect('admin_dashboard')
        return redirect('no_permission')
