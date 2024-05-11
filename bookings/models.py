from django.db import models
from users.models import CustomUser
from buses.models import Bus

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bus_booked = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number_of_seats_books = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    fare = models.CharField(max_length=8)
    qr_code = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
