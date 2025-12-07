from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from users.forms import SignUpForm, CustomSignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomSignInForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
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
            user = form.save(commit= False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            
            
            messages.success(request, "A confirmation mail has been sent to your mail!")
            return redirect('sign_in')
            
    return render(request, 'registration/sign_up.html', {'form': form})



def sign_in(request): 
    form = CustomSignInForm()
    if request.method == 'POST': 
        form = CustomSignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        # user = authenticate(request, username = username, password = password)
        # if user is not None: 
        #     login(request, user)
        #     return redirect('home')    
    return render(request, 'registration/sign_in.html', {'form': form})


# 
@login_required
def sign_out(request): 
    if request.method == 'POST': 
        logout(request)
        return redirect('sign_in')




def activate_user(request, user_id, token): 
    try: 
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else: 
            return HttpResponse("Invalid ID")
    except User.DoesNotExist: 
        return HttpResponse("User Not Found!")

# test for users 
def is_admin(user):
    return user.groups.filter(name = 'admin').exists()




@login_required
@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request): 
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    )
    for user in users: 
        if user.all_groups: 
            user.group_name = user.all_groups[0].name
        else: 
            user.group_name = "No Group Name"
    return render(request, 'admin/dashboard.html', {'users': users})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, user_id): 
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == 'POST': 
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() #remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to {role.name} role")
            return redirect('admin_dashboard')
        
    return render(request, 'admin/assign_role.html', {'form': form})




@login_required
@user_passes_test(is_admin, login_url='no_permission')
def create_group(request): 
    form = CreateGroupForm()
    if request.method == 'POST': 
        form = CreateGroupForm(request.POST)
        if form.is_valid(): 
            group = form.save()
            messages.success(request, f"Group {group.name} has been Created successfully")
            return redirect('create_group')
    return render(request, 'admin/create_group.html', {'form': form})



@login_required
@user_passes_test(is_admin, login_url='no_permission')
def group_list(request): 
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})