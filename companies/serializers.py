from rest_framework import serializers
from . models import BusCompany

class BusCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusCompany
        fields = '__all__'