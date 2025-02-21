from uuid import uuid4
from django.db import models
from django.db.models import OneToOneField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    class Roles(models.TextChoices):
        ADMIN = 'admin'
        CINEMAPHILE = 'cinemaphile'
    
    id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=128, null=False)
    roles = ArrayField(models.CharField(max_length=32, choices=Roles.choices), default=list, null=False)

    city = models.CharField(max_length=128, null=True)
    country = models.CharField(max_length=128, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    telegram_id = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"User: {self.roles} {self.full_name}"
