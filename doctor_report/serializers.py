from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Role, UserRole

from .models import (BillPayment, DoctorProfile, DoctorRate, DoctorReport,
                     ReportType, SizeOption)


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    # ---- User fields ----
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(write_only=True, source='user.password')


    class Meta:
        model = DoctorProfile
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password',
            'phone', 'gender', 'date_of_birth',
            'specialization', 'designation', 'qualifications', 'registration_no',
            'years_experience', 'clinic_name', 'clinic_address', 'profile_photo'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Create doctor profile
        doctor = DoctorProfile.objects.create(user=user, **validated_data)

        # Assign doctor role if you have a UserRole model
        doctor_role = Role.objects.get(slug='doctor')
        UserRole.objects.create(user=user, role=doctor_role)

        return doctor


class DoctorListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')


    class Meta:
        model = DoctorProfile
        fields = '__all__'


class DoctorReportSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="DoctorProfile.user.username", read_only=True)
    bill_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DoctorReport
        fields = [
            "id", "doctor", "doctor_name", "report_id", "patient_name", "patient_age", "specimen", "report_type", "size_option",
            "signed", "signed_at", "bill_amount", "is_paid", "doctor_comment", "receive_date", "created_at", "updated_at"
        ]



class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = ['id', 'name', 'code', 'base_price']


class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = ['id', 'name', 'extra_fee']



class DashboardReportSerializer(serializers.ModelSerializer):
    report_type_name = serializers.CharField(source='report_type.name', read_only=True)

    class Meta:
        model = DoctorReport
        fields = [
            "report_id", "report_type_name",
            "patient_name", "patient_age", "specimen",
            "bill_amount", "signed", "is_paid", "receive_date"
        ]
    


class BillPaymentSerializer(serializers.ModelSerializer):
    reports = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DoctorReport.objects.all()
    )
    approved_by_name = serializers.CharField(source='approved_by.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = BillPayment
        fields = [
            'id', 'doctor', 'doctor_name', 'payment_date', 'amount', 'reports',
            'document', 'is_approved', 'approved_at', 'approved_by', 'approved_by_name'
        ]

    def validate(self, attrs):
        doctor = attrs.get("doctor")
        reports = attrs.get("reports", [])
        amount = attrs.get("amount")

        # সব report একই doctor এর হতে হবে
        for r in reports:
            if r.doctor != doctor:
                raise serializers.ValidationError(f"Report {r.report_id} does not belong to this doctor.")

        # already paid হলে error
        for r in reports:
            if r.is_paid:
                raise serializers.ValidationError(f"Report {r.report_id} is already paid.")

        # amount check
        total = sum([r.bill_amount for r in reports])
        if amount != total:
            raise serializers.ValidationError(f"Amount mismatch. Expected {total}, got {amount}.")

        return attrs

    def create(self, validated_data):
        reports = validated_data.pop("reports")
        payment = BillPayment.objects.create(**validated_data)
        payment.reports.set(reports)
        # reports গুলোকে paid=True করে দাও
        for r in reports:
            r.is_paid = True
            r.save()
        return payment



