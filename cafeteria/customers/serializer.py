
from rest_framework import serializers
from .models import CafeteriaCustomer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeteriaCustomer
        fields = '__all__'