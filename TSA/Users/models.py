from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, EmailField
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    PROJECT_MANAGEMENT = 0
    SALES = 1
    REQUIREMENTS = 2
    UX = 3
    DEVELOPMENT = 4
    QA = 5
    TESTING = 6
    MAINTENANCE = 7
    AREAS = (
        (PROJECT_MANAGEMENT, "Project Management"),
        (SALES, "Sales"),
        (REQUIREMENTS, "Requirements"),
        (UX, "User Experience"),
        (DEVELOPMENT, "Development"),
        (QA, "Quality Assurance"),
        (TESTING, "Testing"),
        (MAINTENANCE, "Maintenance"),
    )
    area = models.SmallIntegerField(
        'Area', default=PROJECT_MANAGEMENT, choices=AREAS)
    email = EmailField(unique=True)
    is_leader = BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
