from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Prudential Super Admin'),
        ('CBHI_ADMIN', 'CBHI Admin'),
        ('MARKETING', 'Marketing Team'),
        ('APPLICANT', 'Community Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='APPLICANT')

    # Add these lines to fix the E304 error
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"