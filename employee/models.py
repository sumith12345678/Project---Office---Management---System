from django.db import models
from account.models import CustomUser,Department
from datetime import datetime

# Create your models here.



class Employee(models.Model):

    fk_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fk_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    e_name = models.CharField(max_length=30)
    e_past_work  = models.TextField(null=True)
    e_photo = models.ImageField(upload_to = "image/")
    e_resume = models.ImageField(upload_to = "resume/")
    e_phone_number = models.CharField(max_length=20, unique=True)
    e_address = models.TextField()
    e_gender = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.e_name
    
    
task_choice = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('bug', 'Bug')
]

class Task(models.Model):
    fk_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.TextField()
    task_pdf = models.FileField(upload_to="task/" , default=None)
    last_date = models.DateField()
    status = models.CharField(max_length=20,choices=task_choice, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

salary_choice = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),

]


class Salary(models.Model):
    fk_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.TextField()
    status = models.CharField(max_length=20,choices=salary_choice, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Attendance(models.Model):
    fk_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Hour = models.CharField(max_length=1, blank=False,default=8)
    Date = models.DateTimeField(default=datetime.now())
    Presence = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.fk_employee}'


class Message(models.Model):
    message = models.TextField()
    subject = models.CharField(max_length=100)
    fk_to = models.ForeignKey(Employee,on_delete=models.PROTECT)
    fk_from = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message    