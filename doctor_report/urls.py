# doctor_report/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminReportsSummary, BillPaymentViewSet,
                    DoctorDashboardView, DoctorListView,
                    DoctorRegistrationView, DoctorReportViewSet,
                    ReportTypeListView, SizeOptionListView)

router = DefaultRouter()
router.register(r'reports', DoctorReportViewSet, basename='doctor-report')
router.register(r'bill-payments', BillPaymentViewSet, basename='bill-payment')


urlpatterns = [
    path("", include(router.urls)),
    path("list/", DoctorListView.as_view(), name="doctor-register"),
    path("register/", DoctorRegistrationView.as_view(), name="doctor-register"),
    path('report-types/', ReportTypeListView.as_view(), name='report-types'),
    path('report-sizes/', SizeOptionListView.as_view(), name='report-sizes'),
    path('dashboard/', DoctorDashboardView.as_view(), name='doctor-dashboard'),
    path('summary/', AdminReportsSummary.as_view(), name='doctor-reports-summary'), 
]

