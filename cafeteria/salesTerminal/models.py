from django.db import models
from django.utils import timezone
from cafeteria.customers.models import CafeteriaCustomer
# Create your models here.
class Order(models.Model):
    order_date = models.DateField(default=timezone.now)
    order_status = models.CharField(max_length=50, default="Completed")
    order_total_discount = models.IntegerField(default=0)
    order_total_price = models.IntegerField(default=0)
    customer_id = models.ForeignKey(CafeteriaCustomer, on_delete=models.CASCADE, related_name="customer_id", null=True)

class OrderHistory(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    order_item_name = models.CharField(max_length=50)
    order_item_quantity = models.IntegerField(default=0)
    order_item_price = models.IntegerField(default=0)
    order_item_total = models.IntegerField(default=0)
    order_item_discount = models.IntegerField(default=0)
