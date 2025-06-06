from django.db import models
from django.contrib.auth.models import User
from clients.models import Location


TEST_CATEGORY_CHOICES = [
    ('BIOCHEMICAL TEST', 'BIOCHEMICAL TEST'),
    ('REPRODUCTIVE HORMONE', 'REPRODUCTIVE HORMONE'),
    ('URINE ANALYSIS', 'URINE ANALYSIS'),
    ('KIDNEY FUNCTION TEST (KFT)', 'KIDNEY FUNCTION TEST (KFT)'),
    ('SPECIAL BIOCHEMICAL TEST', 'SPECIAL BIOCHEMICAL TEST'),
    ('METABOLIC HORMONE', 'METABOLIC HORMONE'),
    ('CANCER MARKER', 'CANCER MARKER'),
    ('LIVER FUNCTION TEST (LFT)', 'LIVER FUNCTION TEST (LFT)'),
]

SAMPLE_CHOICES = [
    ('Serum','Serum'),
    ('Pus','Pus'),
    ('Blood (EDTA Tube)','Blood (EDTA Tube)'),
    ('Blood (PT Tube)','Blood (PT Tube)'),
    ('Blood (RBS Tube)','Blood (RBS Tube)'),
    ('Blood (Red Tube)','Blood (Red Tube)'),
    ('Body Fluid','Body Fluid'),
    ('Urine','Urine')
]

REPORTING_CHOICES = [
    ('One Day','One Day'),
    ('Two Days','Two Days'),
    ('Three Days','Three Days'),
    ('Four Days','Four Days'),
    ('Five Days','Five Days'),
    ('Seven Days','Seven Days'),
    ('Ten Days','Ten Days'),
]


# Create your models here.
class LabServices(models.Model):
    test_category = models.CharField(max_length=100, choices=TEST_CATEGORY_CHOICES, default='BIOCHEMICAL TEST')
    test_name = models.CharField(max_length=100)
    test_description = models.CharField(max_length=255) 
    patient_rate = models.IntegerField()
    test_sample = models.CharField(max_length=20, choices=SAMPLE_CHOICES, default='Serum')
    test_reporting = models.CharField(max_length=20, choices=REPORTING_CHOICES, default='One Day')
    tg_rate = models.IntegerField(blank=True, null=True)
    tg2_rate = models.IntegerField(blank=True, null=True)
    tg3_rate = models.IntegerField(blank=True, null=True)
    tg4_rate = models.IntegerField(blank=True, null=True)
    tg5_rate = models.IntegerField(blank=True, null=True)
    sd_rate = models.IntegerField(blank=True, null=True)
    sd2_rate = models.IntegerField(blank=True, null=True)
    nr_rate = models.IntegerField(blank=True, null=True)
    nrm_rate = models.IntegerField(blank=True, null=True)
    nr2_rate = models.IntegerField(blank=True, null=True)
    feni_rate = models.IntegerField(blank=True, null=True)
    mkg_rate = models.IntegerField(blank=True, null=True)
    ks_rate = models.IntegerField(blank=True, null=True)
     
    def __str__(self):
        return f"{self.test_name} - {self.patient_rate}"


class MarketingExecutive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.DO_NOTHING)
    due = models.IntegerField(default=0)
    extra_paid = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, null=True, blank=True)


    def set_location(self, location):
        # Unset the previously selected location (if any)
        if self.location:
            self.location.is_selected = False
            self.location.save()

        # Set the new location
        self.location = location
        self.location.is_selected = True
        self.location.save()

        self.save()


    def get_rates_for_location(self):
        if self.location:
            location_name = self.location.location_name  
            lab_service = LabServices.objects.first()  
            patient_rate, location_rate = lab_service.get_rates_for_location(location_name)
            return patient_rate, location_rate
        return None, None
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Deposites(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    deposite_amount = models.IntegerField()
    deposite_document = models.URLField(max_length=255)
    deposite_date = models.DateField()
    deposite_ref = models.CharField(max_length=255, blank=True, null=True)
    is_valid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.deposite_amount}"
    

    def save(self, *args, **kwargs):
        if self.is_valid:
            try:
                marketing_executive = MarketingExecutive.objects.get(user=self.user)
                print(marketing_executive)
                deposit_amount = self.deposite_amount
                current_due = marketing_executive.due

                if current_due >= deposit_amount:
                    marketing_executive.due -= deposit_amount
                else:
                    marketing_executive.extra_paid += (deposit_amount - current_due)
                    marketing_executive.due = 0
                marketing_executive.save()

            except MarketingExecutive.DoesNotExist:
                print("marketing executive is not found")
                pass   
        super(Deposites, self).save(*args, **kwargs)