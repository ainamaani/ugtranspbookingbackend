from django.shortcuts import get_object_or_404, render
from . serializers import AccountSerializer
from . models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class AccountView(APIView):
    def post(self, request):
        try:
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"Failed to add new account: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            accounts = Account.objects.all()
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Exception as e:
            return Response({ "error":f"Failed to fetch accounts data : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            account_to_delete = get_object_or_404(Account, pk=pk)
            account_to_delete.delete()
            return Response({ "message":"Account deleted successfully" }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error":f"Failed to delete account with ID {pk} : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            account_to_update = get_object_or_404(Account, pk=pk)
            serializer = AccountSerializer(account_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"Failed to update the account with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SingleAccountView(APIView):
    def get(self, request, pk):
        try:
            account = get_object_or_404(Account, pk=pk)
            serializer = AccountSerializer(account, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Failed to fetch account with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
