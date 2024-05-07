from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from . models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        # hash password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)