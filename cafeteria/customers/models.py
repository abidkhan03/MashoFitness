from django.db import models
from datetime import datetime
# Create your models here.

class CafeteriaCustomer(models.Model):
    customer_SerialNo = models.CharField(max_length=50, null=True, default="")
    customer_name = models.CharField(max_length=50)
    customer_contact = models.IntegerField()
    customer_email = models.CharField(max_length=50, null=True, default="")
    customer_status = models.CharField(max_length=20, null=True, default="")
    customer_address = models.CharField(max_length=200, null=True, default="")
    customer_city = models.CharField(max_length=50)
    customer_country = models.CharField(max_length=50)
    customer_created_at = models.DateField(default=datetime.now)
    customer_dues = models.IntegerField(default=0)

class CustomerPayment(models.Model):
    payment_date = models.DateField(default=datetime.now)
    total_amount = models.IntegerField(default=0)
    payment_amount = models.IntegerField(default=0)
    remaining_amount = models.IntegerField(default=0)
    customer_id = models.ForeignKey(CafeteriaCustomer, on_delete=models.CASCADE)