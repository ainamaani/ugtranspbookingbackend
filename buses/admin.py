from django.contrib import admin
from . models import Bus

# Register your models here.
class BusAdmin(admin.ModelAdmin):
    list_display = ("company","number_plate","departure_location","destination")
    list_filter = ("company","departure_location","destination")

admin.site.register(Bus, BusAdmin)
