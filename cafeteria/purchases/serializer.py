# from attr import fields
# from numpy import source
from rest_framework import serializers
from cafeteria.suppliers.serializer import SupplierSerializer
# from cafeteria.suppliers.models import Supplier
from .models import Inventory , Purchases, PurchasesReturn
from cafeteria.Items.serializer import ItemSerializer

class InventorySerializer(serializers.ModelSerializer):
    inventory_item_id=ItemSerializer(read_only=True)
    class Meta:
        model = Inventory
        fields = '__all__'

class PurchasesSerializer(serializers.ModelSerializer):
    purchases_item_id = ItemSerializer(read_only=True)
    purchases_supplier_id = SupplierSerializer( read_only=True)
    # inventory_id = serializers.PrimaryKeyRelatedField( read_only=True)
    # supplier_name=serializers.ReadOnlyField(source=         '')
    # supplier_id=
    class Meta:
        model=Purchases
        fields='__all__'

    # def to_representation(self, obj):
    #     serialized_data = super(PurchasesSerializer, self).to_representation(obj) # original serialized data
    #     job_category_id = serialized_data.get('inventory_id') # get job category id from original serialized data
    #     job_category = Inventory.objects.get(id=job_category_id) # get the object from db
    #     serialized_data['supplier_name'] = job_category.supplier_id.supplier_name # replace id with category name
        # return serialized_data # return modified serialized data


class PurchasesReturnSerializer(serializers.ModelSerializer):
    purchases_id = PurchasesSerializer(read_only=True)
    class Meta:
        model=PurchasesReturn
        fields='__all__'