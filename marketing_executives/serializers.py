from rest_framework import serializers
from .models import MarketingExecutive, Deposites, LabServices


class LabServiceSerializer(serializers.ModelSerializer):
    # Always include patient_rate for all users
    patient_rate = serializers.IntegerField()

    # Define the base fields
    test_category = serializers.CharField()
    test_name = serializers.CharField()
    test_description = serializers.CharField()
    test_sample = serializers.CharField()
    test_reporting = serializers.CharField()

    class Meta:
        model = LabServices
        # Exclude 'location_rate' from 'fields' in the Meta class, as it will be dynamically added
        fields = [
            'test_category', 'test_name', 'test_description',
            'patient_rate', 'test_sample', 'test_reporting',
            'tg_rate', 'tg2_rate', 'tg3_rate', 'tg4_rate', 'tg5_rate',
            'sd_rate', 'sd2_rate', 'nr_rate', 'nrm_rate', 'nr2_rate'
        ]

    def get_fields(self):
        # Get the original fields from the parent
        fields = super().get_fields()

        # Get the logged-in user and their location from the request context
        user = self.context['request'].user
        if not user.is_staff:  # Non-admin users
            # Remove all rate fields for non-admin users
            for rate_field in ['tg_rate', 'tg2_rate', 'tg3_rate', 'tg4_rate', 'tg5_rate', 
                               'sd_rate', 'sd2_rate', 'nr_rate', 'nrm_rate', 'nr2_rate']:
                if rate_field in fields:
                    del fields[rate_field]

            # Dynamically add 'location_rate' based on the user's location
            try:
                marketing_executive = MarketingExecutive.objects.get(user=user)
                location = marketing_executive.location.location_name  # Assuming Location model has a 'name' field
            except MarketingExecutive.DoesNotExist:
                location = None

            # Add 'location_rate' based on the user's location
            if location == 'Gazipur-1':
                fields['location_rate'] = serializers.IntegerField(source='tg_rate')
            elif location == 'Savar':
                fields['location_rate'] = serializers.IntegerField(source='sd_rate')
            elif location == 'Dhaka':
                fields['location_rate'] = serializers.IntegerField(source='nr_rate')
            # Add more locations as needed here
            else:
                # Default to showing the `patient_rate` if no specific location match
                fields['location_rate'] = serializers.IntegerField(source='patient_rate')

        return fields



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

