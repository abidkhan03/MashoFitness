from rest_framework import serializers

from cafeteria import suppliers
from .models import Supplier, SupplierPayment

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierPaymentSerializer(serializers.ModelSerializer):
    supplier_id = SupplierSerializer(read_only=True)
    class Meta:
        model = SupplierPayment
        fields = '__all__'