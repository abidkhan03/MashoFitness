from rest_framework import serializers
from .models import EmployeeRecord


from django.contrib.auth.models import User
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class EmployeeRecordSerializer(serializers.ModelSerializer):
    user=UsersSerializer()
    class Meta:
        model = EmployeeRecord
        fields = '__all__'