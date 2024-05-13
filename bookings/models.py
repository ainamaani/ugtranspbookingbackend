from django.db import models
from users.models import CustomUser
from buses.models import Bus
from django.core.validators import MinValueValidator
import qrcode
import base64
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bus_booked = models.ForeignKey(Bus, on_delete=models.CASCADE)
    number_of_seats_booked = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    fare = models.CharField(max_length=8)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args, **kwargs):
        # create QR code
        qrcode_image = qrcode.make(self.user.username)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        qr_name = f'QR-Code-{self.user.username}.png' 
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')
        self.qr_code.save(qr_name, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
