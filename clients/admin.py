from django.contrib import admin
from .models import Location, Hospital

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('location_name',),}


admin.site.register(Location, LocationAdmin)
admin.site.register(Hospital)
