import os
import openpyxl
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from applications.models import Applicant
from cbhi.models import CBHI

class Command(BaseCommand):
    help = 'Import data from Cleaned_data.xlsx'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'Cleaned_data.xlsx')
        
        # 1. Clear database to avoid duplicates
        Applicant.objects.all().delete()
        self.stdout.write("Database cleared.")

        # 2. Load Excel file
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        
        # 3. Get headers from the first row
        headers = [str(cell.value) for cell in sheet[1]]
        self.stdout.write(self.style.NOTICE(f"DEBUG: Headers found in Excel: {headers}"))

        cbhi_obj, created = CBHI.objects.get_or_create(
            name="Primary Health Facility",
            defaults={'community_name': 'Kivulu'}
        )
        
        count = 0
        # 4. Iterate through rows (skipping header)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Create a dictionary of the row data
            row_data = dict(zip(headers, row))
            
            try:
                # Map columns (Update these if your debug output shows different names)
                name = row_data.get('interviewe') or row_data.get('name') or 'Unknown'
                
                Applicant.objects.create(
                    cbhi=cbhi_obj,
                    full_name=name,
                    age=int(float(row_data.get('age', 0))),
                    income_source=str(row_data.get('livelihood', 'N/A')),
                    payment_method=str(row_data.get('payment_me', 'cash')),
                    tenure_status=str(row_data.get('tenure_sta', 'tenant')),
                    latitude=float(row_data.get('feature_x', 0)),
                    longitude=float(row_data.get('feature_y', 0)),
                    status='approved',
                    preferred_interview_date=timezone.now().date()
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Skipping row: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} applicants!'))