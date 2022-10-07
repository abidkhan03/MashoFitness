from rest_framework import serializers
from .models import RentalData,rentalPayment
from employees.serializers import EmployeeRecordSerializer

class RentalSerializer(serializers.ModelSerializer):
    rent_attended_by = EmployeeRecordSerializer(read_only=True)
    class Meta:
        model = RentalData
        fields = '__all__'

class RentalPaymentSerializer(serializers.ModelSerializer):
    rental_id = RentalSerializer(read_only=True)
    rent_payment_attended_by = EmployeeRecordSerializer(read_only=True)     
    class Meta:
        model = rentalPayment
        fields = '__all__'

class RentalUpdateSerializer(serializers.ModelSerializer):
    rent_attended_by = EmployeeRecordSerializer(read_only=True)
    active_rent_id=RentalPaymentSerializer(read_only=True)
    class Meta:
        model = RentalData
        fields = '__all__'