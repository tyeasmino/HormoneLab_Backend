from datetime import date

from django.db.models import Count, Q, Sum
from django.utils import timezone
from HormoneLab_Backend.permissions import IsSuperAdminOrDoctorOwner
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (BillPayment, DoctorProfile, DoctorReport, ReportType,
                     SizeOption)
from .serializers import (BillPaymentSerializer, DashboardReportSerializer,
                          DoctorListSerializer, DoctorRegistrationSerializer,
                          DoctorReportSerializer, ReportTypeSerializer,
                          SizeOptionSerializer)


class DoctorRegistrationView(generics.CreateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorRegistrationSerializer

class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorListSerializer

class DoctorReportViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # যদি doctor হয়
        if hasattr(user, 'doctor_profile'):
            return DoctorReport.objects.filter(doctor=user.doctor_profile)
        # অন্য admin/staff হলে সব দেখাবে
        return DoctorReport.objects.all()


class ReportTypeListView(generics.ListAPIView):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer


class SizeOptionListView(generics.ListAPIView):
    queryset = SizeOption.objects.all()
    serializer_class = SizeOptionSerializer


class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = request.user.doctor_profile
        today = date.today()

        # GET parameters (optional)
        month = request.GET.get('month')
        year = request.GET.get('year')

        if month and year:
            # Filter by selected month/year
            reports = DoctorReport.objects.filter(
                doctor=doctor,
                receive_date__month=month,
                receive_date__year=year
            )
        else:
            # Default = only today's data
            reports = DoctorReport.objects.filter(
                doctor=doctor,
                receive_date=today
            )

        # Totals
        total_reports = reports.count()
        total_amount = reports.aggregate(total=Sum('bill_amount'))['total'] or 0
        total_paid = reports.filter(is_paid=True).aggregate(total=Sum('bill_amount'))['total'] or 0
        total_due = total_amount - total_paid

        # Summary
        type_summary = reports.values('report_type__name').annotate(
            count=Count('id'),
            amount=Sum('bill_amount')
        )

        unsigned_reports = DashboardReportSerializer(
            reports.filter(signed=False), many=True
        ).data

        paid_reports = DashboardReportSerializer(
            reports.filter(is_paid=True), many=True
        ).data

        data = {
            'date': today if not (month and year) else None,
            'month': int(month) if month else None,
            'year': int(year) if year else None,
            'total_reports': total_reports,
            'total_amount': total_amount,
            'total_paid': total_paid,
            'total_due': total_due,
            'type_summary': list(type_summary),
            'unsigned_reports': unsigned_reports,
            'paid_reports': paid_reports,
        }
        return Response(data)



class BillPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = BillPaymentSerializer
    permission_classes = [IsSuperAdminOrDoctorOwner]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return BillPayment.objects.all()
        if hasattr(user, "doctor_profile"):
            return BillPayment.objects.filter(doctor=user.doctor_profile)
        return BillPayment.objects.none()


    @action(detail=True, methods=['patch']) 
    def approve(self, request, pk=None):
        payment = self.get_object()
        user = request.user


        # Only owning doctor can approve
        if not hasattr(user, "doctor_profile") or payment.doctor != user.doctor_profile:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)


        if payment.is_approved:
            return Response({"detail": "Payment already approved"}, status=status.HTTP_400_BAD_REQUEST)


        # Approve payment
        payment.approve(user.doctor_profile)


        return Response({"detail": "Payment approved successfully"}, status=status.HTTP_200_OK)
    
    