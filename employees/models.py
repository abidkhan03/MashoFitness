from django.db import models
from django.contrib.auth.models import User

class EmployeeRecord(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    employee_contact = models.CharField(max_length=12)
    employee_image = models.ImageField(upload_to='profile_images/')
    employee_cnic = models.CharField(max_length=15, null=True, blank=True)
    employee_address = models.CharField(max_length=200, null=True, blank=True)
    employee_gender = models.CharField(max_length=10)
    employee_dob = models.DateField(null=True)
    employee_age = models.IntegerField(null=True)
    employee_blood_group = models.CharField(max_length=10,null=True)
    employee_type = models.CharField(max_length=30)
    employee_pay = models.IntegerField(default=0)
    employee_status = models.CharField(max_length=20)

class EmployeeSalary(models.Model):
    employee_salary = models.ForeignKey(EmployeeRecord,on_delete=models.CASCADE)
    salary_date = models.DateField()
    salary_amount = models.IntegerField()
    salary_attended_by = models.CharField(max_length=20)