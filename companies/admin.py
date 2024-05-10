from django.contrib import admin
from . models import BusCompany

# Register your models here.

class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name','company_manager')
    list_filter = ('company_name',)

admin.site.register(BusCompanyAdmin, BusCompany)
