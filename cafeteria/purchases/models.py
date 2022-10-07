from django.db import models
from cafeteria.Items.models import Items
from cafeteria.suppliers.models import Supplier
from django.utils import timezone

# Create your models here.
class Inventory(models.Model):
    inventory_unit_price = models.IntegerField(default=0)
    inventory_net_price = models.IntegerField(default=0)
    inventory_purchased_quantity = models.IntegerField(default=0)
    # inventory_sub_total = models.IntegerField(default=0)
    inventory_item_total = models.IntegerField(default=0)
    inventory_order_number = models.IntegerField(default=0)
    inventory_reference_number = models.CharField(max_length=20,default=0)
    inventory_stock_in_shop = models.IntegerField(default=0)
    inventory_stock_available=models.IntegerField(default=0)
    inventory_item_id = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="inventory_item_id")
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_id", null=True)


class Purchases(models.Model):
    create_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default="Completed")
    purchases_unit_price = models.IntegerField(default=0)
    purchases_net_price = models.IntegerField(default=0)
    purchases_purchased_quantity = models.IntegerField(default=0)
    # inventory_sub_total = models.IntegerField(default=0)
    purchases_item_total = models.IntegerField(default=0)
    purchases_order_number = models.CharField(max_length=20,default=0)
    purchases_reference_number = models.CharField(max_length=20, default='0')
    purchases_stock_in_shop = models.IntegerField(default=0)
    purchases_stock_available=models.IntegerField(default=0)
    purchases_item_id = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="purchases_item_id", null=True)
    purchases_supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchases_supplier_id", null=True)

class PurchasesReturn(models.Model):
    return_date = models.DateField(default=timezone.now)
    available_stock = models.IntegerField(default=0)
    return_stock = models.IntegerField(default=0)
    tatal_price = models.IntegerField(default=0)
    unit_price = models.IntegerField(default=0)
    purchases_id = models.ForeignKey(Purchases, on_delete=models.CASCADE, related_name="purchases_id", null=True)
    # supplierid = models.ForeignKey(Supplier, on_delete=models.÷, related_name="supplierid")
    # inventoryid = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING, related_name="inventoryid")
