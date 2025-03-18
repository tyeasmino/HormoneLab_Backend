from rest_framework.decorators import action
from rest_framework import viewsets
from .models import HospitalAuthority
from .serializers import HospitalAuthoritySerializer
from rest_framework.response import Response


# Create your views here.
class HospitalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = HospitalAuthority.objects.all()
    serializer_class = HospitalAuthoritySerializer

    # example link: http://127.0.0.1:8000/hospitals/hospital_authorities/by_location/?location_id=3
    @action(detail=False, methods=['get'])
    def by_location(self, request):
        location_id = request.query_params.get('location_id')
        if not location_id:
            return Response({"error": "location_id is required"}, status=400)

        hospitals = HospitalAuthority.objects.filter(location_id=location_id)
        serializer = self.get_serializer(hospitals, many=True)
        return Response(serializer.data)

    