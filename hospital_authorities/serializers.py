from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HospitalAuthority

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class AllHospitalAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalAuthority
        fields = '__all__'


class HospitalAuthoritySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = HospitalAuthority
        fields = ['id', 'image', 'phone', 'hospital_name', 'user', 'location']
    
    def create(self, validate_data):
        image_url = validate_data.pop('image', None)

        hospitalAuthority = HospitalAuthority.objects.create(**validate_data)
        if image_url:
            hospitalAuthority.image = image_url
            hospitalAuthority.save()
        
        return hospitalAuthority