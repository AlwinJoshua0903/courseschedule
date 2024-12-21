from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    course_option = models.CharField(max_length=100)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.course_option}"
class schedule(models.Model):
    batch_id=models.IntegerField(unique=True)
    trainer=models.CharField(max_length=50)    
    course_name=models.CharField(max_length=20)
    batch_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f"{self.course_name} - {self.batch_id}"
class coursetaken(models.Model):
    student_id=models.IntegerField(unique=True)
    studentname=models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email=models.EmailField()
    batch_id=models.IntegerField(unique=True)
    trainer=models.CharField(max_length=50)    
    course_name=models.CharField(max_length=20)
    batch_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f"{self.student_id} - {self.studentname} - {self.batch_id} - {self.trainer}"