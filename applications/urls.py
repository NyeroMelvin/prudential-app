# In applications/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_applicant, name='register_applicant'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('marketing-dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('interview/<int:pk>/', views.conduct_interview, name='conduct_interview'),
    path('update-status/<int:pk>/<str:new_status>/', views.update_applicant_status, name='update_status'),
    
    # This is the path that fixes your error
    path('manual-logout/', views.manual_logout, name='manual_logout'),
    
    path('export/', views.export_applicants_csv, name='export_csv'),
]