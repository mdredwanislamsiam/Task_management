# signals
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in list(
            instance.assigned_to.all())]
        # send_mail(
        #     "New Task Assigned",
        #     f"A new task:{instance.title} has be assigned to you. Please Do your job carefully",
        #     "redwanislamsiam13@gmail.com",
        #     assigned_emails,
        #     fail_silently=False,
        # )
