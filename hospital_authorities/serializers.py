from rest_framework import serializers
from .models import HospitalAuthority

class HospitalAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalAuthority
        fields = '__all__'
    
    def create(self, validate_data):
        image_url = validate_data.pop('image', None)

        hospitalAuthority = HospitalAuthority.objects.create(**validate_data)
        if image_url:
            hospitalAuthority.image = image_url
            hospitalAuthority.save()
        
        return hospitalAuthority