from rest_framework import serializers
from .models import snookerIncome,snookerTableIncome
from employees.serializers import EmployeeRecordSerializer

class SnookerIncomeSerializer(serializers.ModelSerializer):
    snooker_attened_by=EmployeeRecordSerializer(read_only=True)
    class Meta:
        model = snookerIncome
        fields = '__all__'
class snookerTableIncomeSerializer(serializers.ModelSerializer):
    snooker_id=SnookerIncomeSerializer(read_only=True)
    class Meta:
        model = snookerTableIncome
        fields = '__all__'

class CustomSeriazerSnooker(serializers.ModelSerializer):
    snooker_attened_by=EmployeeRecordSerializer(read_only=True)
    total_income = serializers.IntegerField()
    class Meta:
        model=snookerIncome
        fields = ('id','description', 'date', 'status','snooker_attened_by','total_income')