from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
from django.db.models import Count
import string
from django.shortcuts import render, redirect
from .models import Worker, Task, TaskCompletion, Notification
from .forms import WorkerCreationForm


from django.db.models import Count
from .forms import WorkerCreationForm
from .models import Worker
from django.contrib.auth.models import User

def create_account_view(request):
    if request.method == 'POST':
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = generate_random_password()  # Generate a random password
            try:
                user = User.objects.create_user(email=email, username=email, password=password)  # Create a new user account
                worker = Worker.objects.create(user=user)  # Create a worker profile
                send_account_credentials_email(email, password)
                worker_count = Worker.objects.aggregate(count=Count('id'))['count']
                return render(request, 'create/side-menu-light-users-layout-1.html', {'email': email, 'success': True, 'worker_count': worker_count})
            except:
                return render(request, 'create/side-menu-light-users-layout-1.html', {'email': email, 'success': False})
    else:
        form = WorkerCreationForm()
    
    worker_count = Worker.objects.aggregate(count=Count('id'))['count']
    return render(request, 'create/side-menu-light-users-layout-1.html', {'form': form, 'worker_count': worker_count})


def generate_random_password(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def send_account_credentials_email(email, password):
    subject = 'Account Created'
    message = f'Your account has been created.\n\nEmail: {email}\nPassword: {password}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        # Create the task
        task = Task.objects.create(title=title, description=description, deadline=deadline)
        # Redirect or display a success message
        return redirect('task_list')
    return render(request, 'create_task.html')

def complete_task(request, task_id):
    if request.method == 'POST':
        worker = request.user.worker
        task = Task.objects.get(id=task_id)
        # Mark the task as completed by the worker
        TaskCompletion.objects.create(worker=worker, task=task, is_completed=True)
        # Create a notification for the directory
        Notification.objects.create(worker=worker, task=task)
        # Redirect or display a success message
        return redirect('task_list')
    return render(request, 'complete_task.html')

def task_list(request):
    worker = request.user.worker
    tasks = Task.objects.filter(taskcompletion__worker=worker)
    return render(request, 'task_list.html', {'tasks': tasks})

def notification_list(request):
    worker = request.user.worker
    notifications = Notification.objects.filter(worker=worker)
    return render(request, 'notification_list.html', {'notifications': notifications})


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        # Create the task
        task = Task.objects.create(title=title, description=description, deadline=deadline)
        # Redirect or display a success message
        return redirect('task_list')
    return render(request, 'create_task.html')

@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        worker = request.user.worker
        task = Task.objects.get(id=task_id)
        # Mark the task as completed by the worker
        TaskCompletion.objects.create(worker=worker, task=task, is_completed=True)
        # Create a notification for the directory
        Notification.objects.create(worker=worker, task=task)
        # Redirect or display a success message
        return redirect('task_list')
    return render(request, 'complete_task.html')

@login_required
def task_list(request):
    worker = request.user.worker
    tasks = Task.objects.filter(taskcompletion__worker=worker)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def notification_list(request):
    worker = request.user.worker
    notifications = Notification.objects.filter(worker=worker)
    return render(request, 'notification_list.html', {'notifications': notifications})