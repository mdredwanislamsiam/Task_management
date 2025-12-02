from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms
import re
from tasks.forms import StyleMixin

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