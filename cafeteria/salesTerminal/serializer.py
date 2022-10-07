from rest_framework import serializers
from .models import Order,OrderHistory
from cafeteria.customers.serializer import CustomerSerializer
class OrderSerializer(serializers.ModelSerializer):
    customer_id = CustomerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    order_id=OrderSerializer(read_only=True)
    class Meta:
        model = OrderHistory
        fields = '__all__'