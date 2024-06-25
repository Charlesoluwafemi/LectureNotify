from django.contrib import admin
from .models import Lecture
from .models import Student

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'course_title','course_code','venue','date', 'time' )
    list_filter = ('faculty','course_title', 'course_code','venue', 'date')  # Enable filtering by faculty, venue, and date

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'course', 'phone_number']
    list_filter = ['department', 'course']
    search_fields = ['name', 'department', 'course']
    # Add more configurations as needed
# admin.py


class CustomAdminSite(admin.AdminSite):
    site_header = 'Lecture Notify Admin Panel'  # Change to your desired header
    site_title = ' Admin '    # Change to your desired title

admin_site = CustomAdminSite(name='custom-admin')


