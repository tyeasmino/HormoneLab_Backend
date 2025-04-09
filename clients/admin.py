from django.contrib import admin
from .models import Location, Reports, UploadedReport

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('location_name',),}


admin.site.register(Location, LocationAdmin) 
admin.site.register(Reports)


@admin.register(UploadedReport)
class UploadedReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')
    search_fields = ['file']

