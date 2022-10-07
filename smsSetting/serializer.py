from rest_framework import serializers
from .models import SmsModle

class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsModle
        fields = '__all__'