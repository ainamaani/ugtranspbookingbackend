from django.contrib import admin
from . models import Payment

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'payment_amount','payment_date','payment_status')
    list_filter = ('payment_status',)

admin.site.register(Payment, PaymentAdmin)
