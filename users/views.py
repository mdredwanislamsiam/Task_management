from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from users.forms import CustomSignUpForm, EditProfileForm, CustomSignInForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordConfirmForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

User = get_user_model()


""" ---- Function Based Views ---- """
    
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

def is_admin(user):
    return user.groups.filter(name = 'admin').exists()



""" ---- Class Based Views ---- """


class AdminUserTestMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class GroupListView(LoginRequiredMixin, AdminUserTestMixin, ListView): 
    template_name = 'admin/group_list.html'
    model = Group
    context_object_name = 'groups'
    
    def get_queryset(self):
        groups = Group.objects.prefetch_related('permissions').all()
        return groups
    

class CreateGroupView(LoginRequiredMixin, AdminUserTestMixin, CreateView): 
    form_class = CreateGroupForm 
    template_name = 'admin/create_group.html'
    
    def form_valid(self, form):
        group = form.save()
        messages.success(
            self.request, f"Group {group.name} has been Created successfully")
        return redirect('create_group')
        
    
    

class AssignRole(LoginRequiredMixin, AdminUserTestMixin, UpdateView):
    model = User
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        user = self.get_object()
        user.groups.clear()
        user.groups.add(role)
        messages.success(
            self.request, f"User {user.username} has been assigned to {role.name} role")
        return redirect('admin_dashboard')


class AdminDashboard(LoginRequiredMixin, AdminUserTestMixin, ListView):
    model = User
    template_name = 'admin/dashboard.html'
    context_object_name = 'users'

    def get_queryset(self):
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(),
                     to_attr='all_groups')
        )
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = "No Group Name"

        return users


class SignUpView(CreateView):
    model = User
    form_class = CustomSignUpForm
    context_object_name = 'form'
    template_name = 'registration/sign_up.html'

    def post(self, request, *args, **kwargs):
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, "A confirmation mail has been sent to your mail!")
            return redirect('sign_in')
        return render(request, 'registration/sign_up.html', {'form': form})

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'


class CustomLoginView(LoginView):
    form_class = CustomSignInForm
    template_name = 'registration/sign_in.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ProfileView(LoginRequiredMixin, TemplateView): 
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['profile_image'] = user.profile_image
        context['bio'] = user.bio
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        
        return context
    

class CustomChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change_view.html'
    form_class = CustomPasswordChangeForm
    

class CustomPasswordResetView(PasswordResetView): 
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('sign_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domaim'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "A Reset Email wast sent to your email. Please Check!")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmForm
    template_name = 'registration/password_reset_confirm_form.html'
    success_url = reverse_lazy('sign_in')
    html_email_template_name = 'registration/reset_email.html'
    def form_valid(self, form):
        messages.success(
            self.request, "Password has been successfully reset")
        return super().form_valid(form)


"""class EditProfileView(LoginRequiredMixin, UpdateView): 
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user = self.get_object())
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user = self.get_object())
        print("views", user_profile)
        context["form"] = self.form_class(instance = self.object, userprofile = user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)    
        return redirect('profile')"""
        
class EditProfileView(LoginRequiredMixin, UpdateView): 
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self): 
        return self.request.user

    def form_valid(self, form): 
        form.save()
        return redirect('profile')    