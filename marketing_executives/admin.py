from django.contrib import admin
from .models import LabServices, MarketingExecutive, Deposites


# Register your models here.
class MarketingExecutiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone', 'due', 'extra_paid')

    def save_model(self, request, obj, form, change):
        if obj.location:
            obj.set_location(obj.location)
        super().save_model(request, obj, form, change)

admin.site.register(MarketingExecutive, MarketingExecutiveAdmin)
admin.site.register(LabServices)
admin.site.register(Deposites)