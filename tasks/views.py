from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Task
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required, login_required
from django.contrib.auth.models import User
from users.views import is_admin

# Create your views here.
def is_manager(user):
    return user.groups.filter(name="Manager").exists()
def is_employee(user):
    return user.groups.filter(name="Employee").exists()

@user_passes_test(is_manager)
def manager_dashboard(request):
    base_query = Task.objects.select_related(
        'details').prefetch_related('assigned_to')
    
    type = request.GET.get('type', 'all') 
    # retriving task data
    if type == 'completed' : 
        tasks = base_query.filter(status = 'COMPLETED')
    elif type == 'in_progress' : 
        tasks = base_query.filter(status = 'IN_PROGRESS')
    elif type == 'pending' : 
        tasks = base_query.filter(status = 'PENDING')
    elif type == 'all':
        tasks = base_query.all()
    
    
    
    #getting task count 
    counts = Task.objects.aggregate(
            total_task = Count('id'), 
            completed_task = Count('id', Q( status = 'COMPLETED')), 
            in_progress_task = Count('id', Q(status = 'IN_PROGRESS')), 
            pending_task = Count('id', Q(status= 'PENDING'))
    )
    
    
    # total_count = tasks.count()
    # completed_task = Task.objects.filter(status= "COMPLETED").count()
    # in_progress_task = Task.objects.filter(status= "IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status= "PENDING").count()
    
    context = {
        'tasks' : tasks, 
        'counts': counts
        # 'total_task': total_count, 
        # 'completed_task': completed_task, 
        # 'in_progress_task': in_progress_task, 
        # 'pending_task': pending_task
    }
    return render(request, "dashboard/manager-dashboard.html", context)


# @user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")



@login_required
@permission_required('tasks.add_task', login_url='no_permission')
def create_task(request):
    employees = User.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    if(request.method == 'POST'):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            '''for django model form'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Succesfully!!" )
            return redirect('create-task')
        
        
            ''' for django form'''
            # title = form.cleaned_data.get('title')
            # description = form.cleaned_data.get('description')
            # due_date = form.cleaned_data.get('due_date')
            # assigned_to = form.cleaned_data.get('assigned_to')
            # task = Task.objects.create(title = title, description = description, due_date = due_date)
            
            # # assing employee to taks 
            # for emp_id in assigned_to:
            #     emp = Employee.objects.get(id = emp_id) 
            #     task.assigned_to.add(emp)
                
    context = {
        'task_form': task_form , 
        'task_detail_form': task_detail_form
    }
    return render(request, 'task_form.html', context)


@login_required
@permission_required('tasks.view_task', login_url='no_permission')
def view_task(request):
    emps = User.objects.prefetch_related('tasks').all()
    return render(request, 'show_task.html', {"emps": emps} )


@login_required
@permission_required('tasks.change_task', login_url='no_permission')
def update_task(request, id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm(instance = task)
    
    if task.details: 
            task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if (request.method == 'POST'):
        task_form = TaskModelForm(request.POST, instance = task)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance = task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            '''for django model form'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully!!")
            return redirect('update-task', id)
            ''' for django form'''
            # title = form.cleaned_data.get('title')
            # description = form.cleaned_data.get('description')
            # due_date = form.cleaned_data.get('due_date')
            # assigned_to = form.cleaned_data.get('assigned_to')
            # task = Task.objects.create(title = title, description = description, due_date = due_date)

            # # assing employee to takss
            # for emp_id in assigned_to:
            #     emp = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(emp)

    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form
    }
    return render(request, 'task_form.html', context)


@login_required
@permission_required('tasks.delete_task', login_url='no_permission')
def delete_task(request, id): 
    if request.method == 'POST': 
        task = Task.objects.get(id  = id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    

@login_required
@permission_required('tasks.view_taskdetail', login_url='no_permission')
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    if request.method =="POST": 
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-detail', task.id)
    
    return render(request, 'task_details.html', {'task':task, 'status_choices': status_choices})


@login_required
def dashboard(request): 
    if is_manager(request.user): 
        return redirect("manager-dashboard")
    elif is_employee(request.user): 
        return redirect('user-dashboard')
    elif is_admin(request.user): 
        return redirect('admin_dashboard')
    
    return redirect('no-permission')