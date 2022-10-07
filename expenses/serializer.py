from rest_framework import serializers
from .models import *
class expensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = expensesData
        fields = '__all__'