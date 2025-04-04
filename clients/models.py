from django.db import models

# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length=100)
    is_selected = models.BooleanField(default=False)
    slug = models.SlugField(max_length=80)

    def __str__(self):
        return f"{self.location_name} - is selected" if self.is_selected else f"{self.location_name}"


class Reports(models.Model):
    location = models.ForeignKey("clients.Location", on_delete=models.DO_NOTHING, blank=True, null=True)
    hospital = models.ForeignKey("hospital_authorities.HospitalAuthority", on_delete=models.DO_NOTHING, blank=True, null=True)
    report_name = models.CharField(max_length=100, blank=True, null=True)
    report_file = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = f"{self.hospital.hospital_name} hospital" if self.hospital else f"{self.location.location_name} location"
        return f"{self.created_at}: {self.report_name} report sent to {target}"
