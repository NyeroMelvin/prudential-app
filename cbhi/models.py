from django.db import models
from django.conf import settings

class CBHI(models.Model):
    STATUS_CHOICES = [
        ('PROPOSED', 'Proposed'),
        ('ACTIVE', 'Active'),
        ('UNDER_REVIEW', 'Under Review'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    name = models.CharField(max_length=200, help_text="e.g. Kivulu Health Shield")
    community_name = models.CharField(max_length=200)
    
    # Geography for map markers
    location_name = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'role': 'CBHI_ADMIN'}
    )
    admin_contact = models.CharField(max_length=100, blank=True)
    
    target_members = models.IntegerField(default=0)
    premium_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_annual_premium_target = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROPOSED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.community_name})"

    @property
    def amount_remaining(self):
        total_collected = self.applicants.filter(status='approved').aggregate(
            models.Sum('premium_paid')
        )['premium_paid__sum'] or 0
        return self.total_annual_premium_target - total_collected

    @property
    def renewal_progress(self):
        total_collected = self.applicants.filter(status='approved').aggregate(
            models.Sum('premium_paid')
        )['premium_paid__sum'] or 0
        if self.total_annual_premium_target == 0:
            return 0
        return (total_collected / self.total_annual_premium_target) * 100