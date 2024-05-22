from django.contrib import admin
from . models import Booking

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','bus_booked')
    list_filter = ('bus_booked',)

admin.site.register(Booking,BookingAdmin)
