from django.db import models
from django.contrib.auth.models import AbstractUser


class Appmodel(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    