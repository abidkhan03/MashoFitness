from django.db import models
from employees.models import EmployeeRecord

class expensesData(models.Model):
    date = models.DateField()
    account_head = models.CharField(max_length=20)
    paid_amount = models.IntegerField()
    payment_mode = models.CharField(max_length=30)
    expenses_for = models.CharField(max_length=20)
    receipent_name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    comments = models.CharField(max_length=200)
    expense_attended_by=models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, null=True)
    
