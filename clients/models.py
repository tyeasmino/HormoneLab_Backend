from django.db import models

# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length=100)
    is_selected = models.BooleanField(default=False)
    slug = models.SlugField(max_length=80)

    def __str__(self):
        return f"{self.location_name} - is selected" if self.is_selected else f"{self.location_name}"


class Hospital(models.Model):
    location_name = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    hostpital_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location_name} - {self.hostpital_name}" 


class Reports(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100, blank=True, null=True)
    report_file = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.location.location_name} - {self.hospital.hostpital_name} hospital"