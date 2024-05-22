from django.db import models
from bookings.models import Booking

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICE = [
        ('pending','Pending'),
        ('failed', 'Failed'),
        ('completed', 'Completed')
    ]
    booking = models.OneToOneField(Booking, on_delete=models.DO_NOTHING)
    payment_amount = models.CharField(max_length=12)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=9, choices=STATUS_CHOICE)

    def __str__(self) -> str:
        return self.booking
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
