from django.db import models
from django.contrib.auth import get_user_model

from user.models import CustomUser

# Create your models here.
User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organizations_created")
    members = models.ManyToManyField(
        User, related_name="organizations_joined", through="OrganizationMember")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"
