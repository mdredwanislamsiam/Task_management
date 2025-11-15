from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("Hello World")

def contact(request):
    return HttpResponse("This is contact page")

def show_task(request):
    return HttpResponse("This is Show-task")

def show_specific_task(request, id):
    print("id", id)
    print("id type", type(id))
    return HttpResponse(f"This is Specific task page {id}")