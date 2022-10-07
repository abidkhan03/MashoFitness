from django.db import models
from django.utils import timezone
from employees.models import EmployeeRecord
# Create your models here.

class Team(models.Model):
    team_name=models.CharField(max_length=25)
    captain_name=models.CharField(max_length=25)
    contact_number=models.IntegerField()
    # team_attended_by=models.CharField(max_length=25)
    member_created_at = models.DateField(default=timezone.now)
    member_updated_at = models.DateField(auto_now=True)
    team_attended_by = models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, null=True)


class Booking(models.Model):
    time = models.CharField(max_length=25, default="")
    meridiem = models.CharField(max_length=5)
    booking_date = models.DateField()
    status = models.BooleanField(default=False)


class Match(models.Model):
    
    date = models.DateField(default=timezone.now)
    fee = models.IntegerField()
    paid= models.CharField(max_length=10, default="Unpaid")
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    booking_time = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_time')
    match_attended_by = models.ForeignKey(EmployeeRecord, on_delete=models.SET_NULL, related_name='match_attended_by', null=True)
