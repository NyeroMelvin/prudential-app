from django import forms
from .models import Applicant

class ApplicantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'cbhi', 'full_name', 'age', 'phone_number', 
            'nin', 'dependents', 
            'preferred_interview_date', 'consent'
        ]
        widgets = {
            'preferred_interview_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'cbhi': 'Select Community Health Shield',
            'nin': 'National ID Number',
        }

class InterviewSurveyForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['interview_completed', 'interview_date_conducted', 'income_bracket', 'survey_notes']
        widgets = {
            'interview_date_conducted': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'survey_notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Enter household survey observations...'}),
            'income_bracket': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Low Income'}),
            'interview_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'interview_completed': 'Mark Interview as Completed',
            'interview_date_conducted': 'Date of Interview',
            'survey_notes': 'Observations / Survey Notes'
        }