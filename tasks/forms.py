from django import forms
from tasks.models import Task, TaskDetail
# django form

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label = 'Task Title')
    description = forms.CharField(widget=forms.Textarea, label ='Text Description')
    due_date = forms.DateField(widget= forms.SelectDateWidget, label = "Due-Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices= [], label='Assigned_To')
    
    
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]
    

# mixin class
class StyleMixin:
    default_classed = "border-2 border-blue-300 shadow-sm focus:border-red-500 mb-4 rounded-lg"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classed} w-full p-3", 
                    'placeholder': f"Enter {field.label.lower()}" 
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classed} w-full p-3", 
                    'placeholder': f"Enter {field.label.lower()}" 
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f"{self.default_classed} p-1"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':f"{self.default_classed} focus:bg-red-200 p-3" 
                })
            else:
                field.widget.attrs.update({
                    'class':f"{self.default_classed}" 
                })

    



# Django Model Form

class TaskModelForm(StyleMixin,forms.ModelForm):
    class Meta:
        model = Task; 
        fields = ['title', 'description', 'due_date', 'assigned_to'] # add assigned_to
        widgets = {
            'due_date':forms.SelectDateWidget, 
            'assigned_to':forms.CheckboxSelectMultiple
        }
        
        '''manual widget'''
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #             'class': " w-full p-2",
        #             'placeholder':"enter task title"
        #         }),
        #     'description': forms.Textarea(attrs={
        #             'class': " w-full p-2",
        #             'placeholder':"enter task title"
        #         }), 
        #     'due_date': forms.SelectDateWidget(attrs={
        #             'class': " p-1 ",
        #             'placeholder':"enter task title"
        #         }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #             'class': " p-2 ",
        #             'placeholder':"enter task title"
        #         })
        # }
    ''' widget using mixins '''
    
        

class TaskDetailModelForm(StyleMixin, forms.ModelForm):
    class Meta: 
        model = TaskDetail
        fields = ['priority', 'notes', 'asset']
    
    