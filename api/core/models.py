from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ROLE_CHOICES = [(STUDENT, "Student"), (INSTRUCTOR, "Instructor")]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_instructor(self):
        return self.role == self.INSTRUCTOR