from django.db import models
from cbhi.models import CBHI

class Applicant(models.Model):
    # ... (Keep all your existing STATUS_CHOICES, PAYMENT_METHOD_CHOICES, etc.) ...
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('interviewed', 'Interviewed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
    ]

    TENURE_CHOICES = [
        ('owner', 'Owner'),
        ('tenant', 'Tenant'),
    ]

    # Links
    cbhi = models.ForeignKey(CBHI, on_delete=models.CASCADE, related_name='applicants')
    
    # --- Personal & Household Details ---
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    nin = models.CharField(max_length=14)
    address = models.CharField(max_length=255, default='N/A')
    dependents = models.IntegerField(default=0)
    tenure_status = models.CharField(max_length=20, choices=TENURE_CHOICES, default='owner')
    income_source = models.CharField(max_length=100, blank=True)
    
    # --- Geolocation ---
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    distance_to_facility = models.FloatField(default=0.0)
    
    # --- Metrics for Dashboard ---
    risk_index = models.IntegerField(default=0, help_text="1-100 scale")
    vulnerability_index = models.IntegerField(default=0, help_text="1-100 scale")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='mobile_money')
    premium_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # --- NEW FIELDS FOR DASHBOARD ---
    illness_type = models.CharField(max_length=100, blank=True, null=True)
    medical_burden = models.FloatField(default=0.0)
    
    # --- Application Flow ---
    preferred_interview_date = models.DateField()
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Marketing/Interview Tracking ---
    interview_completed = models.BooleanField(default=False)
    interview_date_conducted = models.DateField(null=True, blank=True) 
    income_bracket = models.CharField(max_length=50, blank=True, null=True) 
    survey_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.cbhi.name}"