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
    
    def create(self, validated_data):
        image_url = validated_data.pop('image', None)
        location = validated_data.get('location', None)

        marketingExecutive = MarketingExecutive.objects.create(**validated_data)

        # Set the location using the new method to update is_selected
        if location:
            marketingExecutive.set_location(location)

        if image_url:
            marketingExecutive.image = image_url
            marketingExecutive.save()

        return marketingExecutive

    def update(self, instance, validated_data):
        image_url = validated_data.pop('image', None)
        location = validated_data.get('location', None)

        # Update the location using the new method to update is_selected
        if location:
            instance.set_location(location)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image_url:
            instance.image = image_url

        instance.save()
        return instance

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

