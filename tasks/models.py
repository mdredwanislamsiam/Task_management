from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # Tasks
    def __str__(self):
         return self.name


class Project(models.Model):
    name = models.CharField(max_length= 100)
    description = models.TextField()
    start_date = models.DateField()
    
    def __str__(self):
        return self.name    
        
        
        
class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'), 
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed') 
    ]
    project = models.ForeignKey(Project, on_delete= models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    # std_id = models.CharField(max_length=100)
    task = models.OneToOneField(Task, on_delete= models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"details for Task {self.task.title}"
    
    
    