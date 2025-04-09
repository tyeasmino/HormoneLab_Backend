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
from django.http import HttpResponse
import requests
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from datetime import datetime
import os
from rest_framework.parsers import MultiPartParser, FormParser

 
from docx import Document
from rest_framework.views import APIView 
from collections import defaultdict
from .serializers import UploadedReportSerializer
import re
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url












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


    @action(detail=True, methods=['patch'], url_path='toggle-signed')
    def toggle_signed(self, request, pk=None):
        try:
            report = self.get_object()
            report.signed = not report.signed
            report.save()
            serializer = self.get_serializer(report, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Reports.DoesNotExist:
            return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

        

    


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

    



def download_report(request, report_id):
    try:
        report = models.Reports.objects.get(id=report_id)

        file_url = report.report_file
        response = requests.get(file_url)

        if response.status_code != 200:
            return HttpResponse("File could not be downloaded.", status=404)

        file_content = response.content
        current_date = datetime.now().strftime("%d-%m-%y")
        report_name = report.report_name or "report"
        ext = os.path.splitext(file_url)[1]  # Gets '.pdf' or '.docx'
        filename = f"{current_date} {report_name}{ext}" 

        res = HttpResponse(file_content, content_type='application/pdf')
        res['Content-Disposition'] = f'attachment; filename="{smart_str(filename)}"'
        return res

    except models.Reports.DoesNotExist:
        return HttpResponse("Report not found.", status=404)























# class ReportUploadView(APIView):
#     def post(self, request):
#         serializer = serializers.ReportUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             uploaded_file = request.FILES['file']

#             result = upload(uploaded_file, resource_type="raw")
#             file_url = result['secure_url']

#             doc = Document(uploaded_file)

#             slug_pages = defaultdict(list)
#             current_page = []

#             for para in doc.paragraphs:
#                 text = para.text.strip()
#                 if "P. ID" in text:
#                     match = re.search(r"P\. ID\s*:?\s*([A-Z0-9/\-*]+)", text, re.IGNORECASE)
#                     if match:
#                         patient_id = match.group(1)
#                         slug = re.split(r"[-/]", patient_id)[0].upper()
#                         slug_pages[slug].append(current_page)
#                         current_page = []
#                 current_page.append(text)

#             return Response({
#                 "file_url": file_url,
#                 "groups": {k: len(v) for k, v in slug_pages.items()}
#             })

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            # Upload file to Cloudinary
            upload_response = upload(file)
            # Create a record in the database with the Cloudinary URL
            uploaded_report = models.UploadedReport.objects.create(
                file=upload_response['secure_url']
            )
            serializer = UploadedReportSerializer(uploaded_report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)