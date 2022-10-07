from rest_framework import serializers
from .models import Sales
from cafeteria.salesTerminal.serializer import OrderSerializer

class SalesSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer(read_only=True)
    class Meta:
        model = Sales
        fields = '__all__'

class SalesReturnSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer(read_only=True)
    class Meta:
        model = Sales
        fields = '__all__'