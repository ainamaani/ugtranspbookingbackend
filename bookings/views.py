import qrcode
import base64
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.db import transaction
from email.mime.image import MIMEImage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
import qrcode.constants
from . models import Booking
from . serializers import BookingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from buses.models import Bus
from accounts.models import Account
from users.models import CustomUser

# Create your views here.
class BookingView(APIView):
    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "error":f"Failed to add booking details : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            bookings = Booking.objects.all()
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Exception as e:
            return Response({ "error":f"Failed to fetch bookings data : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            booking_to_delete = get_object_or_404(Booking, pk=pk)
            booking_to_delete.delete()
            return Response({ "message":"Booking deleted successfully" }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error":f"Failed to delete booking with ID {pk} : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            booking_to_update = get_object_or_404(Booking, pk=pk)
            serializer = BookingSerializer(booking_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"Failed to update the booking with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SingleBookingView(APIView):
    def get(self, request, pk):
        try:
            booking = get_object_or_404(Booking, pk=pk)
            serializer = BookingSerializer(booking, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Failed to fetch booking with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_booking_id():
    while True:
        booking_id = get_random_string(length=15)
        # check if the generated booking_id already exists
        if not Booking.objects.filter(booking_id=booking_id).exists():
            return booking_id

@api_view(['POST'])
def handle_booking(request):
    user = request.data.get('user')
    bus_booked = request.data.get('bus_booked')
    number_of_seats_booked = request.data.get('number_of_seats_booked')

    if not user or not bus_booked or str(number_of_seats_booked).strip() == "":
        return Response({"error":"All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if number_of_seats_booked < 1:
        return Response({"error":"The minimum number of seats you can book is 1"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # check if there any available seats
            bus = get_object_or_404(Bus, pk=bus_booked)
            if bus.available_seats < number_of_seats_booked:
                return Response({"error":"The number of seats requested isn't available"}, status=status.HTTP_400_BAD_REQUEST)
            
            # check if the user has enough balance on their balance
            account = get_object_or_404(Account, user=user)
            if int(bus.fare) > int(account.balance):
                return Response({"error":"You don't have enough money on your account to book the bus"}, status=status.HTTP_400_BAD_REQUEST)
            
            # compute the bus fare dependingon the number of seats
            fare_charged = int(number_of_seats_booked) * int(bus.fare)

            # deduct the fare from the account balance
            new_account_balance = int(account.balance) - fare_charged
            account.balance = new_account_balance
            account.save()

            # reduce the number of available seats
            current_available_seats = int(bus.available_seats) - int(number_of_seats_booked)
            bus.available_seats = current_available_seats
            bus.save()

            generated_booking_id = generate_booking_id()

            user_details = get_object_or_404(CustomUser, pk=user)
            
            booking_made = Booking.objects.create(
                                        user=user_details,
                                        bus_booked=bus,
                                        number_of_seats_booked=number_of_seats_booked,
                                        fare=bus.fare,
                                        booking_id=generated_booking_id
                                        
            )
            booking_made.save()

            # send email containing the QR code after successful booking
            # get the user's first and last name
            first_name = user_details.first_name
            last_name = user_details.last_name

            # concatenate the first name and the last name to form the fullname
            full_name = f"{first_name} {last_name}"
            subject = 'Booking confirmation'
            message = render_to_string('booking.html', {
                'customer_name' : full_name,
                'booking_id' : booking_made.booking_id,
                'bus_name' : booking_made.bus_booked.company,
                'number_of_seats_booked' : booking_made.number_of_seats_booked,
                'fare' : booking_made.fare,
                'booking_date': booking_made.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
            })
            plain_message = strip_tags(message) # Strip HTML tags for the plain text version
            from_email = "TransportHub Uganda <aina.isaac2002@gmail.com>"
            to_email = user_details.email

            # Create EmailMultiAlternatives object
            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(message, "text/html")

            # Attach QR code image as inline content
            qr_code_path = booking_made.qr_code.path
            with open(qr_code_path, 'rb') as f:
                qr_code_data = f.read()
                email_img = MIMEImage(qr_code_data)
                email_img.add_header('Content-ID', '<qr_code>')
                email.attach(email_img)

            email.send()

            # send_mail(subject, plain_message, from_email, [to_email], html_message=message)

            return Response({ "message":"Booking made successfully" }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({"error":f"Failed to handle booking: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def verify_booking_id(request):
    booking_id = request.data.get('booking_id')

    try:
        customer = Booking.objects.get(booking_id=booking_id)
        if customer:
            return Response({"message":"Booking is authentic"}, status=status.HTTP_202_ACCEPTED)
        return Response({"message":"Booking doesn't exist in the DB"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response({"error":f"Failed to verify the booking: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)