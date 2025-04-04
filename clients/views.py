from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets
from . import models, serializers  
from marketing_executives.models import MarketingExecutive
from hospital_authorities.models import HospitalAuthority
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import localtime




# Create your views here.
class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        return models.Location.objects.filter(is_selected=False)


class AllLocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReportsSerializer

    def get_queryset(self):
        # This will return all reports
        return models.Reports.objects.all()

    @action(detail=False, methods=['get'], url_path='today')
    def today_reports(self, request):
        # Get current time in local timezone
        now_local = localtime(timezone.now())

        # Calculate the boundaries for today in the local timezone
        today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now_local.replace(hour=23, minute=59, second=59, microsecond=999999)
 

        # Filter reports based on local timezone's boundaries
        reports_today = models.Reports.objects.filter(
            created_at__gte=today_start,
            created_at__lte=today_end
        )

        # Serialize and return today's reports
        serializer = self.get_serializer(reports_today, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    


class UserReportsViewSet(viewsets.ReadOnlyModelViewSet):
    """Shows only the reports related to the logged-in user (Marketing Executive or Hospital Authority)"""

    serializer_class = serializers.ReportsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Marketing Executive Case
        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            return models.Reports.objects.filter(location=marketing_executive.location)
        except MarketingExecutive.DoesNotExist:
            pass  # If not a marketing executive, check next case

        # Hospital Authority Case
        try:
            hospital_authority = HospitalAuthority.objects.get(user=user)

            # Ensure hospital exists before filtering
            if hospital_authority:
                return models.Reports.objects.filter(hospital=hospital_authority)
            else:
                print(f"Hospital Authority {user} has no linked hospital.")
        except HospitalAuthority.DoesNotExist:
            pass  # If not a hospital authority, return empty queryset

        return models.Reports.objects.none()  # Return empty if user is neither

    @action(detail=False, methods=['get'], url_path='today')
    def today_reports(self, request):
        user = self.request.user

        # Get current time in local timezone
        now_local = localtime(timezone.now())

        # Calculate start and end of today in local timezone
        today_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now_local.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Debugging: Print the corrected start and end boundaries in the terminal
        print(f"Today's start in local timezone: {today_start}")
        print(f"Today's end in local timezone: {today_end}")

        # Marketing Executive Case
        try:
            marketing_executive = MarketingExecutive.objects.get(user=user)
            reports_today = models.Reports.objects.filter(
                location=marketing_executive.location,
                created_at__gte=today_start,
                created_at__lte=today_end
            )
            serializer = self.get_serializer(reports_today, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MarketingExecutive.DoesNotExist:
            pass  # If not a marketing executive, check next case

        # Hospital Authority Case
        try:
            hospital_authority = HospitalAuthority.objects.get(user=user)
            if hospital_authority:
                reports_today = models.Reports.objects.filter(
                    hospital=hospital_authority,
                    created_at__gte=today_start,
                    created_at__lte=today_end
                )
                serializer = self.get_serializer(reports_today, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except HospitalAuthority.DoesNotExist:
            pass  # If not a hospital authority, return empty queryset

        return Response([], status=status.HTTP_200_OK)  # Return empty list if no reports found

    



