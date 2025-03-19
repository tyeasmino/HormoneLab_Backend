from rest_framework import serializers
from .models import Location, Hospital, Reports

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'



class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'

    def validate(self, data):
        """ Ensure at least one of 'location' or 'hospital' is provided """
        if not data.get('location') and not data.get('hospital'):
            raise serializers.ValidationError("At least one of 'location' or 'hospital' must be provided.")
        return data

    def create(self, validated_data):
        report_url = validated_data.pop('report_file', None)
        report = Reports.objects.create(**validated_data)

        if report_url:
            report.report_file = report_url
            report.save()

        return report
