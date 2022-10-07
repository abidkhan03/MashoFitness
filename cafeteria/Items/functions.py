from .models import *
from django.core.files.storage import FileSystemStorage
from cafeteria.purchases.models import Inventory, Purchases
from cafeteria.suppliers.models import Supplier

# create the item data  in database table name Items from models
def ItemsAdd(request):
    '''
    add_item=Items.objects.create(the column names defined in models one by one) # to create objects in a table
    add_item.save() # to save the item data into a table
    '''
    try:
        print("photo is selected",request.FILES)
        if request.FILES:
            print("photo is selected",request.FILES['photos'])
            f=request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
        else:
            filename="default.png"

        add_item = Items.objects.create(item_code=request.POST.get("item-code"),
                        item_name=request.POST.get("item-name"), item_unit=request.POST.get("unit-measure"),
                        item_category=request.POST.get("item-category"), item_brand=request.POST.get("item-brand"),
                        item_manufacturer=request.POST.get("manufacturer"), item_selling_price=request.POST.get("selling-price"),
                        item_reorder_level=0, item_image=filename,
                        item_description=request.POST.get("item-description"),
                        item_status=request.POST.get("status")
                        )
        add_item.save()
    #     inventory_unit_price = models.IntegerField(default=0)
    # inventory_net_price = models.IntegerField(default=0)
    # inventory_purchased_quantity = models.IntegerField(default=0)
    # inventory_sub_total = models.IntegerField(default=0)
    # inventory_item_total = models.IntegerField(default=0)
    # inventory_order_number = models.IntegerField(default=0)
    # inventory_reference_number = models.IntegerField(default=0)
    # inventory_stock_in_shop = models.IntegerField(default=0)

    # inventory_item_id = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="inventory_item_id")
    # supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_id")
        # count=Purchases.objects.all().last().id
        # print("count",count)
        add_inventory = Inventory.objects.create(
                        inventory_unit_price= 0,
                        inventory_net_price= 0,
                        inventory_purchased_quantity=0,
                        # inventory_sub_total= 0,
                        inventory_item_total=0,
                        inventory_stock_in_shop=0,
                        inventory_item_id=add_item
                        )
        # print(Supplier.objects.get('supplier_name'))
        add_inventory.save()
        return add_item
    except Exception as e:
        print("Error in adding items", e)
        return False

# update the item data 
def UpdateItem(request):
    ''' a function that update the items from database
    if photo is selected by user
    fs = FileSystemStorage() to store the picture in system
    filename=fs.save(f.name,f) and save the file name 
    uploaded_file_url=fs.url(filename)
    else
    filename="default.png" the default png pic will save in database
    '''
    try:
        print("photo is selected",request.FILES)
        if request.FILES:
            print("photo is selected",request.FILES['update-photos'])
            f=request.FILES["update-photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        else:
            filename="default.png"
        print(filename)
        print("update id recieved:",request.POST.get("update-id"))
        update_item = Items.objects.filter(id=request.POST.get("update-id")).update(item_code=request.POST.get("update-item-code"),
                        item_name=request.POST.get("update-item-name"), item_unit=request.POST.get("update-unit-measure"),
                        item_category=request.POST.get("update-item-category"), item_brand=request.POST.get("update-item-brand"),
                        item_manufacturer=request.POST.get("update-item-manufacturer"), item_selling_price=request.POST.get("update-selling-price"),
                        item_reorder_level=0, item_image=filename,
                        item_description=request.POST.get("update-item-description"),
                        item_status=request.POST.get("update-status")
                        )

        return update_item
    except Exception as e:
        print("Error in adding items", e)
        return False

# function for products to add in Product table 
# def addProducts(request):
#     try:
#         if request.FILES:
#             f=request.FILES["photo"]
#             fs = FileSystemStorage()
#             filename = fs.save(f.name, f)
#             uploaded_file_url = fs.url(filename)
#         else:
#             filename="default.png"

#         add_product =   Product.objects.create(product_code=request.POST.get("product-code"),
#                         product_name=request.POST.get("product-name"), product_unit=request.POST.get("product-measure"),
#                         product_category=request.POST.get("product-category"), product_brand=request.POST.get("product-brand"),
#                         product_manufacturer=request.POST.get("manufacturer"), product_selling_price=request.POST.get("selling-price"),
#                         product_max_selling_quantity=request.POST.get("max-selling-qty"), product_min_selling_quantity=request.POST.get("min-selling-qty"),
#                         product_image=filename, product_expire_date=request.POST.get("expiry-date"), 
#                         product_description=request.POST.get("item-description"), product_status=request.POST.get("status")
#                         )
#         add_product.save()

#         return add_product
#     except Exception as e:
#         print("Error in adding items", e)
#         return False

# function for non-stock items to add in NonStock table
def addNonStockItems(request):
    try:
        print("photo is selected",request.FILES)
        if request.FILES:
            print("photo is selected",request.FILES['photos'])
            f=request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
        else:
            filename="default.png"

        add_nonStock_item = NonStock.objects.create(nonStock_item_code=request.POST.get("item-code"),
                        nonStock_item_name=request.POST.get("item-name"), 
                        nonStock_item_unit=request.POST.get("unit-measurement"),
                        nonStock_item_category=request.POST.get("item-category"), 
                        nonStock_item_brand=request.POST.get("item-brand"),
                        nonStock_item_manufacturer=request.POST.get("manufacturer"),
                        nonStock_item_purchase_price=request.POST.get("purchase-price"),
                        nonStock_item_selling_price=request.POST.get("selling-price"),nonStock_item_image=filename, 
                        nonStock_item_description=request.POST.get("description"),
                        nonStock_item_status=request.POST.get("status")
                        )
        add_nonStock_item.save()



        return add_nonStock_item
    except Exception as e:
        print("Error in adding items", e)
        return False


# function for non-stock items to update the NonStock table's values
def updateNonStockItems(request):
    try:
        print("photo is selected",request.FILES)
        if request.FILES:
            print("photo is selected",request.FILES['update-photos'])
            f=request.FILES["update-photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        else:
            filename="default.png"
        print(filename)
        print(request.POST.get("update-id"))
        update_nonStock_item = NonStock.objects.filter(id=request.POST.get("update-id")).update(nonStock_item_code=request.POST.get("item-code"),
                        nonStock_item_name=request.POST.get("item-name"), 
                        nonStock_item_unit=request.POST.get("unit-measurement"),
                        nonStock_item_category=request.POST.get("item-category"), 
                        nonStock_item_brand=request.POST.get("item-brand"),
                        nonStock_item_manufacturer=request.POST.get("manufacturer"),
                        nonStock_item_purchase_price=request.POST.get("purchase-price"),
                        nonStock_item_selling_price=request.POST.get("selling-price"),
                        nonStock_item_status=request.POST.get("status"),
                        nonStock_item_image=filename,  
                        nonStock_item_description=request.POST.get("description"),
                        )

        return update_nonStock_item
    except Exception as e:
        print("Error in adding items", e)
        return False



