from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Permission, Group
from django import forms
from django.contrib.auth import get_user_model
import re
from tasks.forms import StyleMixin
from users.models import CustomUser

User = get_user_model()

class SignUpForm(UserCreationForm): 
    class Meta: 
        model = User
        fields = ['first_name', 'last_name','email', 'username', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        
        
        
class CustomSignUpForm(StyleMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta: 
        model = User 
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'confirm_password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border-2 border-blue-300 shadow-sm focus:border-red-500 mb-4 rounded-lg w-full p-3',
                'placeholder': f"Enter {field.label}"
            })
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        errors = []
        if len(password1) < 8 :
            errors.append("Password Must contain 8 characters")
        
        if not re.search(r'[A-Z]', password1):
            errors.append("password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password1):
            errors.append("password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password1):
            errors.append("password must contain at least one digit")
        if not re.search(r'[!@#$]', password1):
            errors.append("password must contain at least one special char")
        if re.search(r'[&^*()_+{}/;:]', password1):
            errors.append(
                "password must contain the following characters: &,^,*,(,),_,+,},{,/,;,:,")
            
        if errors: 
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean_email(self): 
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email = email).exists()
        if(email_exist):
            raise forms.ValidationError("This Email Is already Signed Up")
        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password1 != confirm_password: 
            raise forms.ValidationError("password do not match")
        
        

class CustomSignInForm(StyleMixin, AuthenticationForm): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border-2 border-blue-300 shadow-sm focus:border-red-500 mb-4 rounded-lg w-full p-3',
                'placeholder': f"Enter {field.label}"
            })
        
        
        
class AssignRoleForm(StyleMixin, forms.Form): 
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= "select a role"
    )
    

class CreateGroupForm(StyleMixin, forms.ModelForm): 
    class Meta: 
        model = Group 
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(), 
        }
        lables ={
            'permissions': 'Assign Permission'
        }
        
class CustomPasswordChangeForm(StyleMixin, PasswordChangeForm): 
    pass

class CustomPasswordResetForm(StyleMixin, PasswordResetForm): 
    pass

class CustomPasswordConfirmForm(StyleMixin, SetPasswordForm): 
    pass

"""
class EditProfileForm(StyleMixin, forms.ModelForm): 
    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')
    
    class Meta: 
        model = User
        fields = ['email', 'first_name', 'last_name']
        
        
    def __init__(self, *args, **kwargs): 
        self.userprofile = kwargs.pop("userprofile", None)
        super().__init__(*args, **kwargs)
        print("forms", self.userprofile)
        if self.userprofile: 
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image
        
    def save(self, commit = True): 
        user = super().save(commit =False)
        if self.userprofile: 
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')
            if commit: 
                self.userprofile.save()
        if commit: 
            user.save()
        return user
"""

class EditProfileForm(StyleMixin, forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image'] 
    