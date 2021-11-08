from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, EmailField
from django.db.models.fields.related import ForeignKey


class Area(models.Model):
    name = models.CharField('Nombre', max_length=50)


class User(AbstractUser):
    area = ForeignKey(Area, on_delete=models.SET_NULL, blank=True,
                      null=True, default=None, verbose_name='Area')
    email = EmailField(unique=True)
    is_leader = BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
