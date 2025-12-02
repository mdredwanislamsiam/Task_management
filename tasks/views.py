from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Task
from django.db.models import Count, Q
from django.contrib import messages
# Create your views here.

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


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    return render(request, 'test.html')


def create_task(request):
    employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    if(request.method == 'POST'):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
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


def view_task(request):
    emps = Employee.objects.prefetch_related('tasks').all()
    return render(request, 'show_task.html', {"emps": emps} )


def update_task(request, id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm(instance = task)
    
    if task.details: 
            task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if (request.method == 'POST'):
        task_form = TaskModelForm(request.POST, instance = task)
        task_detail_form = TaskDetailModelForm(request.POST, instance = task.details)
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

            # # assing employee to taks
            # for emp_id in assigned_to:
            #     emp = Employee.objects.get(id = emp_id)
            #     task.assigned_to.add(emp)

    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form
    }
    return render(request, 'task_form.html', context)


def delete_task(request, id): 
    if request.method == 'POST': 
        task = Task.objects.get(id  = id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')