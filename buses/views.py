from django.shortcuts import render, get_object_or_404
from . models import Bus
from . serializers import BusSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class BusView(APIView):
    def post(self, request):
        try:
            serializer = BusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ "error":f"Failed to add bus details : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            buses = Bus.objects.all()
            serializer = BusSerializer(buses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)   
        except Exception as e:
            return Response({ "error":f"Failed to fetch buses data : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            bus_to_delete = get_object_or_404(Bus, pk=pk)
            bus_to_delete.delete()
            return Response({ "message":"Bus deleted successfully" }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ "error":f"Failed to delete bus with ID {pk} : {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, pk):
        try:
            bus_to_update = get_object_or_404(Bus, pk=pk)
            serializer = BusSerializer(bus_to_update, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"Failed to update the bus with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SingleBusView(APIView):
    def get(self, request, pk):
        try:
            bus = get_object_or_404(Bus, pk=pk)
            serializer = BusSerializer(bus, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"Failed to fetch bus with ID {pk}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)