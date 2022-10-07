from django.db import models
from employees.models import EmployeeRecord


class snookerIncome(models.Model):
    description = models.CharField(max_length=300)
    snooker_attened_by = models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, related_name='snooker_attened_by', null=True)
    date = models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)
    

class snookerTableIncome(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    table_number = models.CharField(null=False, blank=False, max_length=10)
    minutes_per_table = models.CharField(max_length=50,null=False, blank=False)
    snooker_id = models.ForeignKey(snookerIncome, on_delete=models.CASCADE)




    
