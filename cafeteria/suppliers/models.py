from tkinter import N
from django.db import models
from datetime import datetime


# Create your models here.

class Supplier(models.Model):
    supplier_account = models.CharField(max_length=50)
    supplier_name = models.CharField(max_length=50)
    supplier_contact = models.IntegerField()
    supplier_email = models.CharField(max_length=50, null=True, default="")
    supplier_status = models.CharField(max_length=20, null=True, default="")
    supplier_address = models.CharField(max_length=200, null=True, default="")
    supplier_city = models.CharField(max_length=50)
    supplier_country = models.CharField(max_length=50)
    supplier_created_at = models.DateField(default=datetime.now)
    supplier_dues = models.IntegerField(default=0)


class SupplierPayment(models.Model):
    payment_date = models.DateField(default=datetime.now)
    total_amount = models.IntegerField(default=0)
    paid_amount = models.IntegerField(default=0)
    remaining_amount = models.IntegerField(default=0)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # purchase_id = models.ForeignKey('purchases.Purchases', on_delete=models.DO_NOTHING ,default=0,null=True)