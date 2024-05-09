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
    contact_information = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
class ResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    generated_reset_code = models.PositiveIntegerField(max_length=6)


    def __str__(self) -> str:
        return self.user
    
    class Meta:
        verbose_name = 'Reset Code'
        verbose_name_plural = 'Reset Codes'
