import qrcode
import base64
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.db import transaction
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
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

@transaction.atomic
@api_view(['POST'])
def handle_booking(request):
    user = request.data.get('user')
    bus_booked = request.data.get('bus_booked')
    number_of_seats_booked = request.data.get('number_of_seats_booked')

    if not user or not bus_booked or number_of_seats_booked or str(number_of_seats_booked).strip() == "":
        return Response({"error":"All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if number_of_seats_booked < 1:
        return Response({"error":"The minimum number of seats you can book is 1"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # check if there any available seats
        bus = get_object_or_404(Bus, pk=bus_booked)
        if bus.available_seats < number_of_seats_booked:
            return Response({"error":"The number of seats requested isn't available"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the user has enough balance on their balance
        account = get_object_or_404(Account, user=user)
        if int(bus.fare) > int(account.balance):
            return Response({"error":"You don't have enough money on your account to book the bus"}, status=status.HTTP_400_BAD_REQUEST)
        
        # deduct the fare from the account balance
        new_account_balance = int(account.balance) - int(bus.fare)
        account.balance = new_account_balance
        account.save()
        
        booking_made = Booking.objects.create(
                                    user=user,
                                    bus_booked=bus_booked,
                                    number_of_seats_booked=number_of_seats_booked,
                                    fare=bus.fare,
                                    
        )

        # send email containing the QR code after successful booking
        # get the user's first and last name
        user_details = get_object_or_404(CustomUser, pk=user)
        first_name = user_details.first_name
        last_name = user_details.last_name

        # concatenate the first name and the last name to form the fullname
        full_name = f"{first_name} {last_name}"
        subject = 'Booking confirmation'
        message = render_to_string('booking.html', {
            'customer_name' : full_name,
            'booking_id' : booking_made.id,
            'bus_name' : booking_made.bus_booked,
            'number_of_seats_booked' : booking_made.number_of_seats_booked,
            'fare' : booking_made.fare
        })
        plain_message = strip_tags(message) # Strip HTML tags for the plain text version
        from_email = "TransportHub Uganda <aina.isaac2002@gmail.com>"
        to_email = user_details.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=message)

        return Response({ "message":"Booking made successfully" }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error":f"Failed to handle booking: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)