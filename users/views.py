from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import SignUpForm, CustomSignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def sign_up(request):
    if request.method == "GET": 
        form = CustomSignUpForm()

    if request.method == "POST": 
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # confirm_password = form.cleaned_data.get('confirm_password')
            
            # if password == confirm_password: 
            #     User.objects.create(username = username, password = password)
            form.save()
            messages.success(request, "The Sign Up was Successful")
            return redirect('sign_up')
            
    return render(request, 'registration/sign_up.html', {'form': form})

def sign_in(request): 
    
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None: 
            login(request, user)
            return redirect('home')
        
    return render(request, 'registration/sign_in.html')

def sign_out(request): 
    if request.method == 'POST': 
        logout(request)
        return redirect('sign_in')