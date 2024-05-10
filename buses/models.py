from django.db import models
from companies.models import BusCompany

# Create your models here.
class Bus(models.Model):
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=20)
    capacity = models.PositiveSmallIntegerField()
    available_seats = models.PositiveSmallIntegerField()
    departure_location = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    departure_time = models.TimeField()
    fare = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.company
    
    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'
