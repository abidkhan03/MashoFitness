from email.policy import default
from django.db import models

class Items(models.Model):
    item_code = models.CharField(max_length=10)
    item_name = models.CharField(max_length=50)
    item_unit = models.CharField(max_length=30)
    item_category = models.CharField(max_length=30)
    item_brand = models.CharField(max_length=30, null=True, default="")
    item_manufacturer = models.CharField(max_length=30, null=True, default="")
    item_selling_price = models.IntegerField()
    item_reorder_level = models.IntegerField()
    item_image = models.ImageField(upload_to='items_images/', null=True)
    item_description= models.CharField(max_length=100, null=True, default='')
    item_status = models.CharField(max_length=20, default='Active', null=True)

class NonStock(models.Model):

    nonStock_item_code = models.CharField(max_length=15, default='')
    nonStock_item_name = models.CharField(max_length=50)
    nonStock_item_unit = models.CharField(max_length=30)
    nonStock_item_category = models.CharField(max_length=30)
    nonStock_item_brand = models.CharField(max_length=30, null=True, default="")
    nonStock_item_manufacturer = models.CharField(max_length=30, null=True, default="")
    nonStock_item_purchase_price = models.IntegerField(default=0)
    nonStock_item_selling_price = models.IntegerField()
    nonStock_item_image = models.ImageField(upload_to='items_images/', null=True)
    nonStock_item_description= models.CharField(max_length=200, null=True, default="")
    nonStock_item_status = models.CharField(max_length=20, null=True, default="")
    





