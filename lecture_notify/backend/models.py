from django.db import models
from datetime import date, time


class Student(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    faculty = models.CharField(max_length=250, default='Unknown Faculty')
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255, default="Unknown Faculty")
    venue = models.CharField(max_length=255, default="Unknown Venue")
    department = models.CharField(max_length=255, default="Unknown Department")
    course_title = models.CharField(max_length=255, default="Unknown Course_title")
    course_code = models.CharField(max_length=255, default="Unknown Course_code")
    date = models.DateField(default=date.today)
    time = models.TimeField(default=time(hour=8))
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name


    
