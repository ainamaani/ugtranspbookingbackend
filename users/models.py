from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLES_CHOICE = [
        ('manager' , 'Manager' ),
        ('admin' , 'Admin' ),
        ('customer' , 'Customer')
    ]

    role = models.CharField(max_length=10 , choices=ROLES_CHOICE)
    contact_information = models.CharField(max_length=14)

    def __str__(self) -> str:
        return self.username
