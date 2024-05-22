from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from . models import Payment
from . serializers import PaymentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class PaymentView(APIView):
    def post(self, request):
        try:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "error":f"Failed to add payment details : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Exception as e:
            return Response({ "error":f"Failed to fetch payments data : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            payment_to_delete = get_object_or_404(Payment, pk=pk)
            payment_to_delete.delete()
            return Response({ "message":"Payment deleted successfully" }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error":f"Failed to delete payment with ID {pk} : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            payment_to_update = get_object_or_404(Payment, pk=pk)
            serializer = PaymentSerializer(payment_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"Failed to update the payment with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SinglePaymentView(APIView):
    def get(self, request, pk):
        try:
            payment = get_object_or_404(Payment, pk=pk)
            serializer = PaymentSerializer(payment, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Failed to fetch payment with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)