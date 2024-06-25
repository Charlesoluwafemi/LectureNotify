from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import viewsets
from .models import Lecture
from .serializers import LectureSerializer
import pandas as pd
from datetime import datetime
from .tasks import send_whatsapp_notification_to_students
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Student
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import openpyxl

import logging

logger = logging.getLogger(__name__)

def root_view(request):
    return HttpResponse("Welcome to Lecture Notify!")

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

class UploadExcelView(View):
    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            excel_file = request.FILES['file']
            try:
                if not excel_file.name.endswith('.xlsx'):
                    return JsonResponse({'error': 'The uploaded file is not an Excel file'}, status=400)
                
                df = pd.read_excel(excel_file, engine='openpyxl')
                print(f"Read {len(df)} rows from the uploaded file.")

                for index, row in df.iterrows():
                    try:
                        name = row['name']
                        department = row['department']
                        course = row['course']
                        date = row['date']
                        time = row['time']
                        
                        # Ensure date and time are in string format if necessary
                        if isinstance(date, pd.Timestamp):
                            date = date.strftime('%Y-%m-%d')
                        if isinstance(time, pd.Timestamp):
                            time = time.strftime('%H:%M:%S')

                        lecture_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

                        lecture = Lecture.objects.create(
                            name=name,
                            department=department,
                            course=course,
                            date=lecture_time.date(),
                            time=lecture_time.time()
                        )

                        # Schedule the SMS reminder 24 hours before the lecture
                        send_whatsapp_notification_to_students(lecture.id, lecture_time)
                    except Exception as e:
                        print(f"Error processing row {index + 1}: {e}")
                        return JsonResponse({'error': f"Error processing row {index + 1}: {e}"}, status=400)

                print("Successfully processed all rows.")
                return JsonResponse({'message': 'File uploaded and lectures added successfully'})
            except Exception as e:
                print(f"Error processing file: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            print("No file provided.")
            return JsonResponse({'error': 'No file provided'}, status=400)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFView(View):
    def get(self, request):
        return JsonResponse({'csrfToken': get_token(request)})
    
@csrf_exempt
def upload_students(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']
        
        try:
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            # Process each row in the sheet
            for row in sheet.iter_rows(min_row=2, values_only=True):
                name, phone_number, faculty, department, course = row
                # Save each student record to the database
                # Student.objects.create(name=name, phone_number=phone_number, faculty=faculty, department=department, course=course)

            return JsonResponse({'message': 'File uploaded successfully'})
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return JsonResponse({'error': 'Error processing file'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
