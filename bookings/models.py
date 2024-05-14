from django.db import models
from users.models import CustomUser
from buses.models import Bus
from django.core.validators import MinValueValidator
import qrcode
import base64
import hmac
import hashlib
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bus_booked = models.ForeignKey(Bus, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=15, null=True)
    number_of_seats_booked = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)],null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    fare = models.CharField(max_length=8)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True)

    def __str__(self) -> str:
        return self.user.username
    
    
    def save(self, *args, **kwargs):
        # Concatenate all booking details into a single string
        booking_info = (
        f"User: {self.user.first_name} {self.user.last_name}\n"
        f"Booking ID: {self.booking_id}\n"
        f"Bus Booked: {self.bus_booked.number_plate}\n"
        f"Number of Seats Booked: {self.number_of_seats_booked}\n"
        f"Fare: {self.fare}"
    )   

        
        # Create QR code with booking information
        qrcode_image = qrcode.make(booking_info)
        
        # Determine the minimum size required for the canvas
        min_canvas_size = max(qrcode_image.size[0], qrcode_image.size[1])
        
        # Set the canvas size to be slightly larger than the QR code size
        canvas_size = (min_canvas_size + 10, min_canvas_size + 10)
        
        canvas = Image.new('RGB', canvas_size, 'white')
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([0, 0, canvas_size[0] - 1, canvas_size[1] - 1], outline="black")  # Add border
        
        # Calculate the position to paste the QR code in the center of the canvas
        qr_position = ((canvas_size[0] - qrcode_image.size[0]) // 2, (canvas_size[1] - qrcode_image.size[1]) // 2)
        
        canvas.paste(qrcode_image, qr_position)
        qr_name = f'QR-Code-{self.user.username}.png' 
        buffer = BytesIO()
        canvas.save(buffer, format='PNG')
        
        # Save QR code image to the qr_codes directory
        self.qr_code.save(qr_name, File(buffer), save=False)
        canvas.close()
        
        super().save(*args, **kwargs)

    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
