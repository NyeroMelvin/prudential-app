from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout  # Import logout here
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Count, Avg
import csv
from .forms import ApplicantRegistrationForm, InterviewSurveyForm
from .models import Applicant

# 1. PUBLIC VIEWS
def landing_page(request):
    return render(request, 'applications/index.html')

def register_applicant(request):
    success = False
    form = ApplicantRegistrationForm()
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ApplicantRegistrationForm()
    return render(request, 'applications/register.html', {'form': form, 'success': success})

# 2. STAFF VIEWS
@staff_member_required
def staff_dashboard(request):
    applicants = Applicant.objects.all().order_by('-created_at')
    return render(request, 'applications/dashboard.html', {'applicants': applicants})

@staff_member_required
def update_applicant_status(request, pk, new_status):
    applicant = get_object_or_404(Applicant, pk=pk)
    valid_statuses = [s[0] for s in Applicant.STATUS_CHOICES]
    if new_status in valid_statuses:
        applicant.status = new_status
        applicant.save()
    return redirect('staff_dashboard')

@staff_member_required
def export_applicants_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applicants.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'NIN', 'Status', 'Phone', 'Created At'])
    applicants = Applicant.objects.all()
    for app in applicants:
        writer.writerow([app.id, app.full_name, app.nin, app.status, app.phone_number, app.created_at])
    return response

# 3. MARKETING VIEW
@login_required
def marketing_dashboard(request):
    if not request.user.groups.filter(name='Marketing').exists() and not request.user.is_staff:
        return HttpResponseForbidden("You do not have access to this portal.")
        
    applicants = Applicant.objects.filter(status='approved', interview_completed=False).order_by('full_name')

    # Aggregations
    income_data = Applicant.objects.values('income_source').annotate(count=Count('id'))
    payment_data = Applicant.objects.values('payment_method').annotate(count=Count('id'))
    illness_data = Applicant.objects.values('illness_type').annotate(count=Count('id'))
    risk_data = Applicant.objects.values('risk_index').annotate(count=Count('id'))
    
    # Average Medical Burden
    avg_burden = Applicant.objects.aggregate(Avg('medical_burden'))['medical_burden__avg'] or 0

    # Geospatial Data for Map
    map_data = list(Applicant.objects.values('latitude', 'longitude', 'risk_index', 'illness_type'))

    context = {
        'applicants': applicants,
        'avg_burden': round(avg_burden, 2),
        'income_labels': [item['income_source'] for item in income_data],
        'income_values': [item['count'] for item in income_data],
        'payment_labels': [item['payment_method'] for item in payment_data],
        'payment_values': [item['count'] for item in payment_data],
        'illness_labels': [item['illness_type'] for item in illness_data],
        'illness_values': [item['count'] for item in illness_data],
        'risk_labels': [item['risk_index'] for item in risk_data],
        'risk_values': [item['count'] for item in risk_data],
        'map_data': map_data,
    }
    return render(request, 'applications/marketing_dashboard.html', context)

@login_required
def conduct_interview(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        form = InterviewSurveyForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save() 
            if applicant.interview_completed:
                applicant.status = 'interviewed'
                applicant.save()
            return redirect('marketing_dashboard')
    else:
        form = InterviewSurveyForm(instance=applicant)
    return render(request, 'applications/interview_form.html', {
        'applicant': applicant, 
        'form': form
    })

# applications/views.py
from django.shortcuts import HttpResponse
from django.contrib.auth import get_user_model

def create_admin_user(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        return HttpResponse("Admin user created successfully!")
    return HttpResponse("Admin user already exists.")

def manual_logout(request):
    logout(request)
    # Instead of redirecting to '/', we render the new logout template
    return render(request, 'applications/logout.html')

