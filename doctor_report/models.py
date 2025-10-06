from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    # 🔑 Basic info
    phone          = models.CharField(max_length=20)
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender         = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)
    date_of_birth  = models.DateField(blank=True, null=True)

    # 🩺 Professional info
    specialization   = models.CharField(max_length=120, blank=True, null=True)  # e.g. Pathologist
    designation      = models.CharField(max_length=120, blank=True, null=True)  # e.g. Consultant
    qualifications   = models.CharField(max_length=200, blank=True, null=True)  # e.g. MBBS, FCPS
    registration_no  = models.CharField(max_length=50, blank=True, null=True)   # BMDC or license no
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    clinic_name      = models.CharField(max_length=150, blank=True, null=True)
    clinic_address   = models.TextField(blank=True, null=True)
    profile_photo    = models.ImageField(upload_to="doctor_photos/", blank=True, null=True)

    # ⚙️ Status & system
    is_active      = models.BooleanField(default=True)       # Control login visibility
    slug           = models.SlugField(max_length=150, unique=True, editable=False)

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.user.username  
        super().save(*args, **kwargs)

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        if not full_name:
            full_name = self.user.username
        return f"({self.specialization or 'Doctor'}) {full_name}"


class ReportType(models.Model):
    """Default report types and their base prices."""
    name = models.CharField(max_length=50, unique=True)       # e.g. Paps, FNAC, Histopathology
    code = models.SlugField(max_length=20, unique=True)       # e.g. paps, fnac, histo
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.base_price}৳)"
  

class SizeOption(models.Model):
    """Optional size modifiers for Histopathology."""
    name = models.CharField(max_length=50, unique=True)       # e.g. Small, Large, Extra Large
    extra_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)         # future use, hide/disable old sizes


    def __str__(self):
        fee = f"+{self.extra_fee}৳" if self.extra_fee else "No extra"
        return f"{self.name} ({fee})"


class DoctorRate(models.Model):
    doctor = models.ForeignKey("doctor_report.DoctorProfile", on_delete=models.CASCADE, related_name="custom_rates")
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    custom_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ("doctor", "report_type")

    def __str__(self):
        return f"{self.doctor.user.username} → {self.report_type.name}: {self.custom_price}৳"


class DoctorReport(models.Model):
    doctor = models.ForeignKey("doctor_report.DoctorProfile", on_delete=models.CASCADE, related_name="doctor_reports")

    report_id = models.CharField(max_length=10, unique=True, blank=True, null=True)    
    patient_name = models.CharField(max_length=255, blank=True, null=True)    
    patient_age = models.CharField(max_length=255, blank=True, null=True)    
    specimen = models.CharField(max_length=255, blank=True, null=True)    
    report_type = models.ForeignKey(ReportType, on_delete=models.PROTECT)
    size_option = models.ForeignKey(SizeOption, on_delete=models.SET_NULL, blank=True, null=True)

    signed       = models.BooleanField(default=False)
    signed_at    = models.DateTimeField(blank=True, null=True)

    bill_amount  = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    is_paid      = models.BooleanField(default=False)

    doctor_comment = models.TextField(blank=True, null=True)

    receive_date = models.DateField(default=now, help_text="Actual sample receive date")
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("doctor", "report_id")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Calculate bill:
        1️⃣ Doctor custom rate if exists,
        2️⃣ else ReportType.base_price
        3️⃣ plus SizeOption.extra_fee if any
        """

        extra = self.size_option.extra_fee if self.size_option else 0


        try:
            custom = DoctorRate.objects.get(doctor=self.doctor, report_type=self.report_type)
            base_price = custom.custom_price
        except DoctorRate.DoesNotExist:
            base_price = self.report_type.base_price

        self.bill_amount = base_price + extra


        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} ↔ {self.report_id} ({self.bill_amount}৳)"


class BillPayment(models.Model):
    doctor = models.ForeignKey(
        "doctor_report.DoctorProfile", 
        on_delete=models.CASCADE, 
        related_name="payments"
    )
    payment_date = models.DateField(auto_now_add=True, help_text="Date of payment entry")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reports = models.ManyToManyField(
        "doctor_report.DoctorReport", 
        related_name="payments"
    )
    document = models.FileField(upload_to="payment_docs/", blank=True, null=True)
    
    # Approval / acknowledgment by doctor
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        "doctor_report.DoctorProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_payments"
    )

    def clean(self):
        """Prevent adding reports that are already marked as paid."""
        for report in self.reports.all():
            if report.is_paid:
                raise ValidationError(f"Report {report.report_id} is already marked as paid.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mark all related reports as paid automatically
        if self.reports.exists():
            self.reports.update(is_paid=True)

    def approve(self, doctor_user):
        """Doctor approves/acknowledges payment received."""
        if not self.is_approved:
            self.is_approved = True
            self.approved_at = timezone.now()
            self.approved_by = doctor_user
            self.save()

    def __str__(self):
        return f"Payment {self.id} - {self.doctor.user.get_full_name()} - {self.amount}৳"





