from django.db import models
from datetime import datetime
from employees.models import EmployeeRecord

class RentalData(models.Model):
    Full_name = models.CharField(max_length=100)
    contact_no = models.IntegerField()
    cnic_no = models.CharField(max_length=15, null=True)
    reference = models.CharField(max_length=100, null=True)
    shop_no = models.CharField(max_length=20)
    electric_bill = models.CharField(max_length=30, null=True)
    gas_bill = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateField(default=datetime.now)
    payment_status = models.CharField(max_length=150)
    active_rent_id=models.ForeignKey('rentalPayment', on_delete=models.SET_NULL, related_name='active_rent_id' , null=True)
    rent_attended_by = models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, related_name='rent_attended_by' , null=True)


class rentalPayment(models.Model):
    rent_amount = models.IntegerField()
    payment_mode = models.CharField(max_length=25)
    rent_pay_date = models.DateField()
    rent_duration = models.CharField(max_length=25)
    total_rent = models.IntegerField()
    rent_end_date = models.DateField()
    rent_pay_by = models.CharField(max_length=50)
    payment_gas_bill = models.BooleanField(null=True)
    payment_electric_bill = models.BooleanField(null=True)
    payment_created_at = models.DateField(default=datetime.now)
    rental_id = models.ForeignKey(RentalData, on_delete=models.CASCADE, related_name='rental_id')
    rent_payment_attended_by = models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, related_name='rent_payment_attended_by' , null=True)