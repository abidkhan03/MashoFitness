from django.db import models
from django.db import models
from django.utils import timezone
from cafeteria.salesTerminal.models import Order

class Sales(models.Model):
    sale_date = models.DateField(default=timezone.now)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="Salesorder_id")
    


class SalesReturn(models.Model):
    salesReturn_date = models.DateField(default=timezone.now)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="Returnorder_id")