from django.db import models

from organization.models import Organization
from user.models import CustomUser

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)