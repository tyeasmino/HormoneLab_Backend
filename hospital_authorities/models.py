from django.db import models
from django.contrib.auth.models import User
from clients.models import Location

# Create your models here.
class HospitalAuthority(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=11, null=True, blank=True)
    hospital_name = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"