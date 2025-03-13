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
    tg_rate = models.IntegerField()
    tg2_rate = models.IntegerField()
    tg3_rate = models.IntegerField()
    tg4_rate = models.IntegerField()
    tg5_rate = models.IntegerField()
    sd_rate = models.IntegerField()
    sd2_rate = models.IntegerField()
    nr_rate = models.IntegerField()
    nrm_rate = models.IntegerField()
    nr2_rate = models.IntegerField()
    feni_rate = models.IntegerField()
    mkg_rate = models.IntegerField()
    ks_rate = models.IntegerField()

    def get_rates_for_location(self, location_name):
        location_rate_map = {
            'Savar': self.sd_rate,
            'Savar-2': self.sd2_rate,
            'Narsingdi': self.nr_rate,
            'Gazipur-1': self.tg_rate,
        }
        
        location_rate = location_rate_map.get(location_name, None)       
        return self.patient_rate, location_rate
    
    
    def __str__(self):
        return f"{self.test_name} - {self.patient_rate}"


class MarketingExecutive(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.DO_NOTHING)
    due = models.IntegerField(default=0)
    extra_paid = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, null=True, blank=True)


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