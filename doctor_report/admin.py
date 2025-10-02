from django.contrib import admin

from .models import (BillPayment, DoctorProfile, DoctorRate, DoctorReport,
                     ReportType, SizeOption)

# Register your models here.
admin.site.register(SizeOption)
admin.site.register(ReportType)
admin.site.register(DoctorProfile)
admin.site.register(DoctorRate)
admin.site.register(BillPayment)


@admin.register(DoctorReport)
class DoctorReportAdmin(admin.ModelAdmin):
    list_display = (
        "id", "report_id", "receive_date", "doctor", "patient_name", "patient_age", "specimen",
        "report_type", "size_option", "bill_amount", "is_paid", "signed", 
    )
    list_filter = ("doctor", "report_type", "size_option", "signed", "is_paid")
    search_fields = ("report_id", "patient_name", "doctor__user__username")
    list_editable = ("is_paid", "signed")
