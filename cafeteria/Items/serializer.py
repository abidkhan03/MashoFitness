from rest_framework import serializers
from .models import Items, NonStock

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class NonStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonStock
        fields = '__all__'

