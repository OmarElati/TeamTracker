from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): # Custom user model that extends Django's AbstractUser
    pass

class Worker(models.Model): # Model representing a worker
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Task(models.Model): # Model representing a task
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()


class TaskCompletion(models.Model): # representing the completion of a task by a worker
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

class Notification(models.Model): # representing a notification for a worker regarding a task
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
