from django.db import models

# Create your models here.

class BusCompany(models.Model):
    company_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.company_name
    
    class Meta:
        verbose_name = 'Bus company'
        verbose_name_plural = 'Bus companies'
