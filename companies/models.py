from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import CustomUser

# Create your models here.

class BusCompany(models.Model):
    company_name = models.CharField(max_length=20)
    company_description = models.CharField(max_length=500)
    contact_information = models.CharField(max_length=14, unique=True)
    company_email = models.EmailField(unique=True)
    company_manager = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    company_bus_image = models.ImageField(
                                upload_to="bus_images/",
                                validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])]
                                        )

    def __str__(self) -> str:
        return self.company_name
    
    
    class Meta:
        verbose_name = 'Bus company'
        verbose_name_plural = 'Bus companies'
