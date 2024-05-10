import random
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from . models import CustomUser,ResetCode
from . serializers import CustomUserSerializer, ResetCodeSerializer
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
        return Response({ 'message':'User deleted successfully' }, status=status.HTTP_200_OK)
    
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
        

class HandlePasswordResetCode(APIView):
    # function to generate random codes
    @staticmethod
    def generate_reset_code():
        return random.randint(100000, 999999)
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user_forgot_password = CustomUser.objects.get(email=email)
            # check if the code is already sent
            reset_code_exists = ResetCode.objects.filter(user = user_forgot_password).first()
            if reset_code_exists:
                reset_code_exists.generated_reset_code = HandlePasswordResetCode.generate_reset_code()
                reset_code_exists.save()

                # get the user's first and last name
                first_name = user_forgot_password.first_name
                last_name = user_forgot_password.last_name

                # concatenate the first name and the last name to form the fullname
                full_name = f"{first_name} {last_name}"
                # Send email with the reset code
                subject = 'Password reset code'
                message = render_to_string('password_reset_code.html', {
                    'user_name' : full_name,
                    'reset_code' : reset_code_exists.generated_reset_code
                })
                plain_message = strip_tags(message) # Strip HTML tags for the plain text version
                from_email = "TransportHub Uganda <aina.isaac2002@gmail.com>"
                to_email = user_forgot_password.email
                
                send_mail(subject, plain_message, from_email, [to_email], html_message=message)

            else:   
                # call the static method to generate the code
                code = HandlePasswordResetCode.generate_reset_code()
                reset_code_entry = ResetCode.objects.create( user=user_forgot_password,
                                                            generated_reset_code=code
                                                            )
                # get the user's first and last name
                first_name = user_forgot_password.first_name
                last_name = user_forgot_password.last_name

                # concatenate the first name and the last name to form the fullname
                full_name = f"{first_name} {last_name}"
                # Send email with the reset code
                subject = 'Password reset code'
                message = render_to_string('password_reset_code.html', {
                    'user_name' : full_name,
                    'reset_code' : code
                })
                plain_message = strip_tags(message) # Strip HTML tags for the plain text version
                from_email = "TransportHub Uganda <aina.isaac2002@gmail.com>"
                to_email = user_forgot_password.email

                send_mail(subject, plain_message, from_email, [to_email], html_message=message)

                return Response({ 'message' : f"Code { reset_code_entry } generated successfully" }, status=status.HTTP_201_CREATED)
             # Always return a response
            return Response({'message': "Reset code sent successfully"}, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist:
            return Response({ 'error' : "User with this email doesn't exist" }, status=status.HTTP_404_NOT_FOUND)

    # Fetch all reset codes
    def get(self, request):
        reset_codes = ResetCode.objects.all()
        serializer = ResetCodeSerializer(reset_codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class HandleResetForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        reset_code = request.data.get('reset_code')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if email is None or str(email).strip() == "" or reset_code is None or str(reset_code).strip() == "" or password1 is None or str(password1).strip() == "" or password2 is None or str(password2).strip() == "":
            return Response({ "error" : "All fields are required" }, status=status.HTTP_400_BAD_REQUEST)

        try:
            userID = CustomUser.objects.filter(email=email).values_list('id', flat=True).first()
            # check if the user has a reset code
            user_has_code = ResetCode.objects.get(user=userID)
            if user_has_code is None:
                return Response({ "error" : "No reset code has been sent for this user" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # check if the supplied reset code is the same as the one sent
                if user_has_code.generated_reset_code != reset_code:
                    return Response({ "error" : "Input the correct reset code" }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if password1 != password2:
                        return Response({ "error" : "Passwords do not match" }, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user_resetting_password = CustomUser.objects.get(email=email)
                        user_resetting_password.password = make_password(password2)
                        user_resetting_password.save()
                        return Response({"message" : "Password reset successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({ "error" : f"Failed to reset forgotten password: {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        