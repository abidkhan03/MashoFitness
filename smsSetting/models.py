from django.db import models

# Create your models here.
class SmsModle(models.Model):
    smsFor = models.CharField(max_length=20)
    smsModule = models.CharField(max_length=20)
    smsText = models.CharField(max_length=500)