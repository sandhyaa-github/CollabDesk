from django.db import models

from project.models import Project
from user.models import CustomUser

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done")
    ], default="todo")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
