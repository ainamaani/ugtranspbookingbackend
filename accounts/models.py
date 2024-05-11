from django.db import models
from users.models import CustomUser
from django.core.validators import MinValueValidator

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    account_number = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
