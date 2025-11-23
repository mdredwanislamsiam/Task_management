from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task
# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")
def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    return render(request, 'test.html')


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()
    if(request.method == 'POST'):
        form = TaskModelForm(request.POST)
        if form.is_valid():
            '''for django model form'''
            form.save()
            return render(request, 'task_form.html', {'form' : form , 'message': 'Successfull!!!'})
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
                
            
    context = {'form': form}
    return render(request, 'task_form.html', context)


def view_task(request):
    emps = Employee.objects.prefetch_related('tasks').all()
    return render(request, 'show_task.html', {"emps": emps} )

    
    