from rest_framework import serializers
from .models import MarketingExecutive, Deposites, LabServices


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabServices
        fields = '__all__'



class MarketingExecutiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingExecutive
        fields = '__all__'
    
    def create(self, validate_data):
        image_url = validate_data.pop('image', None)

        marketingExecutive = MarketingExecutive.objects.create(**validate_data)
        if image_url:
            marketingExecutive.image = image_url
            marketingExecutive.save()
        
        return marketingExecutive

class DepositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposites
        fields = '__all__'
    
    def create(self, validated_data):
        image_url = validated_data.pop('deposite_document', None)

        deposite = Deposites.objects.create(**validated_data)
        if image_url:
            deposite.deposite_document = image_url
            deposite.save()
        
        return deposite

