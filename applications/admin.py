from django.contrib import admin
from .models import Applicant

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'cbhi', 'status', 'created_at')
    list_filter = ('status', 'cbhi', 'gender')
    search_fields = ('full_name', 'nin')