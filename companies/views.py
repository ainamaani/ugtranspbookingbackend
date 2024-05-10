from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from . serializers import BusCompanySerializer
from rest_framework.response import Response
from rest_framework import status
from . models import BusCompany

# Create your views here.
class BusCompanyView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = BusCompanySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "error": f"Failed to add bus company details: {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            companies = BusCompany.objects.all()
            serializer = BusCompanySerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error": f"Failed to fetch bus companies data: {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            company_to_delete = get_object_or_404(BusCompany, pk=pk)
            company_to_delete.delete()
            return Response({"message":"Company deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error": f"Failed to delete company:{str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            company_to_update = get_object_or_404(BusCompany, pk=pk)
            serializer = BusCompanySerializer(company_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "error": f"Failed to update the company details: {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SingleBusCompanyView(APIView):
    def get(self, request, pk):
        try:
            company = get_object_or_404(BusCompany, pk=pk)
            serializer = BusCompanySerializer(company, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "message": f"Failed to fetch the company with ID {pk} :{str(e)} " }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
