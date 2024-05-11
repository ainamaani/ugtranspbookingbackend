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
        
def handle_deposit(request):
    amount_to_deposit = request.data.get('amount')
    acc_no = request.data.get('acc_no')

    if not amount_to_deposit or str(amount_to_deposit).strip() == "" or not acc_no or str(acc_no).strip() == "":
        return Response({"error":"Both fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(acc_no) < 10:
        return Response({"error": "Account number can't be less than 10 digits, enter the correct one"})
    
    if int(amount_to_deposit) < 1000:
        return Response({"error":"The minimum amount you can deposit is 1,000 UGX"})
    
    try:
        account = get_object_or_404(Account, account_number=acc_no)
        current_balance = int(account.balance)
        new_balance = current_balance + int(amount_to_deposit)
        account.balance = str(new_balance)
        account.save()
        return Response({"message":f"Deposit successful, new balance: {account.balance}"})
    except Exception as e:
        return Response({"error":f"Failed to handle deposit: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

