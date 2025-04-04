from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets
from . import models, serializers  
from marketing_executives.models import MarketingExecutive
from hospital_authorities.models import HospitalAuthority



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
    queryset = models.Reports.objects.all()
    serializer_class = serializers.ReportsSerializer


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
