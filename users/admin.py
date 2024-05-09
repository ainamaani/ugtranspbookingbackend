from django.contrib import admin
from . models import CustomUser,ResetCode

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name","username","email")
    list_filter = ("first_name",)

class ResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "generated_reset_code")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ResetCode, ResetCodeAdmin)