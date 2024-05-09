from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from . models import CustomUser
from . serializers import CustomUserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

class UserRegistration(APIView):
    # User registration
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # get the user's first and last name
            first_name = user.first_name
            last_name = user.last_name

            # concatenate the first name and the last name to form the fullname
            full_name = f"{first_name} {last_name}"

            # Send email after successful registration
            subject = 'Registration successful!'
            message = render_to_string('welcome.html', {
                'customer_name' : full_name,
                'customer_fullname' : full_name
            })
            plain_message = strip_tags(message) # Strip HTML tags for the plain text version
            from_email = "TransportHub Uganda <aina.isaac2002@gmail.com>"
            to_email = user.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=message)

            print("Email sent successfully")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Fetch all users
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Delete a single user
    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response({ 'message':'User deleted successfully' })
    
    # Update user's credentials
    def put(self, request, pk):
        user_to_update = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    # Disable authentication for login view
    authentication_classes = [] 

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autheticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh' : str(refresh),
                'access' : str(refresh.access_token)
            }

            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({ 'error': 'Invalid credentials' }, status=status.HTTP_401_UNAUTHORIZED)
        

class ChangeUserPassword(APIView):
    def post(self, request, pk):
        supplied_current_password = request.data.get('current_password')
        supplied_new_password = request.data.get('new_password')
        # check if the supplied current password and the new password are the same
        if supplied_current_password == supplied_new_password:
            return Response({ 'error': "The current password and the proposed new password should be different" }, status=status.HTTP_400_BAD_REQUEST)
        # retrieve the user associated with the id
        user = get_object_or_404(CustomUser, pk=pk)
        if user is None:
            # raise ValidationError(f"User with ID {pk} doesn't exist")
            return Response({ 'error' : f"User with ID {pk} doesn't exist" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if the supplied current password matches the hashed password stored in the database
            if not check_password(supplied_current_password, user.password):
                return Response({ 'error' : "Supply the correct current user password" }, status=status.HTTP_400_BAD_REQUEST)
            
            # hash new password before saving it
            user.password = make_password(supplied_new_password)
            user.save()
            return Response({ 'message': 'Password changed successfully' }, status=status.HTTP_200_OK)
    
