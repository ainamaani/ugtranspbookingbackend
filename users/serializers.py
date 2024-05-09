from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from . models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        # hash password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
    
    # def update(self, instance, validated_data):
        # exclude password from generated data if it is not provided
        # if 'password' in validated_data:
        #     del validated_data['password']
        # return super().update(instance, validated_data)

# class ChangePasswordSerializer(serializers.ModelSerializer):
#     current_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate(self, data):
#         current_password = data.get('current_password')
#         new_password = data.get('new_password')

        # retrieve the user associated 

        # check if the current password is the same as the supplied new password
        # if current_password == new_password:
        #     raise serializers.ValidationError("New supplied password must be different from the current password")