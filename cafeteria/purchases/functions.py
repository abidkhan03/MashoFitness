# from pytest import Item
from .models import *
from django.core.files.storage import FileSystemStorage
from cafeteria.suppliers.models import Supplier, SupplierPayment


def UpdateInventory(request):
    # print(request.POST.get("supplier-name"))
    try:
        # print("photo is selected", request.FILES)
        if request.FILES:
            # print("photo is selected", request.FILES['photos'])
            f = request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
        else:
            filename = "default.png"

        # print(request.POST.get("update-id"))
        # print(request.POST.get("available-stock"))
        # print(request.POST.get("item-name"))
        # print(request.POST.get("unit-price"))
        # print(request.POST.get("order-number"))
        # print(request.POST.get("reference-number"))
        # print(request.POST.get("net-price"))
        # print(request.POST.get("purchased-qty"))
        Inventory.objects.filter(id=request.POST.get("update-id")).update(
            inventory_unit_price=request.POST.get("unit-price"),
            inventory_net_price=request.POST.get("net-price"),
            inventory_purchased_quantity=request.POST.get("purchased-qty"),
            # inventory_sub_total=request.POST.get("sub-total"),
            inventory_item_total=request.POST.get(
                "item-total"),
            inventory_order_number=request.POST.get(
                "order-number"),
            inventory_reference_number=request.POST.get(
                "reference-number"),
            # inventory_stock_in_shop=request.POST.get("available-stock-inshop"),
            inventory_stock_available=int(request.POST.get(
                "available-stock"))+int(request.POST.get("purchased-qty")),
            supplier_id=Supplier.objects.filter(
                supplier_name=request.POST.get("supplier-name")).first(),
        )

        purchases=Purchases.objects.create(
            purchases_unit_price=request.POST.get("unit-price"),
            purchases_net_price=request.POST.get("net-price"),
            purchases_purchased_quantity=request.POST.get("purchased-qty"),
            # inventory_sub_total=request.POST.get("sub-total"),
            purchases_item_total=request.POST.get(
                "item-total"),
            purchases_order_number=request.POST.get(
                "order-number"),
            purchases_reference_number=request.POST.get(
                "reference-number"),
            # inventory_stock_in_shop=request.POST.get("available-stock-inshop"),
            purchases_stock_available=int(request.POST.get(
                "available-stock"))+int(request.POST.get("purchased-qty")),
            purchases_supplier_id=Supplier.objects.filter(
                supplier_name=request.POST.get("supplier-name")).first(),
            purchases_item_id=Items.objects.get(id=Inventory.objects.get(
                id=request.POST.get("update-id")).inventory_item_id.id)
        )
        purchases.save()
        AddSupplierDues(request.POST.get("supplier-name"), request.POST.get("item-total"), request.POST.get("net-price"),request.POST.get("remaining"))
        # supplier=Supplier.objects.filter(supplier_name=request.POST.get("supplier-name")).first()
        # supplier.supplier_dues+=int(total_amount)-int(paid_amount)
        print("successfully updated inventory")
    except Exception as e:
        print("No data found {}".format(e))

# def purchases(request):
#     pass


def CustomerPurchasesSerializer(query):
    data = []
    for i in query:
        data.append(
            {
                "id": i.id,
                "inventory_order_number": i.inventory_id.inventory_order_number,
                "inventory_order_number": i.inventory_id.inventory_reference_number,
                "supplier_id": i.inventory_id.supplier_id.supplier_name,
                "inventory_item_total": i.inventory_id.inventory_item_total,
                "status": i.status,
                "create_date": i.create_date,
            }
        )
    return data


def AddReturnPurchases(request):
    try:
        purchases = Purchases.objects.filter(
            purchases_order_number=request.POST.get("order-number")).first()
        PurchasesReturn.objects.create(
            available_stock=request.POST.get("available-stock"),
            return_stock=request.POST.get("return-stock"),
            tatal_price=int(request.POST.get("return-stock")) *
            int(request.POST.get("unit-price")),
            # inventory_sub_total=request.POST.get("sub-total"),
            unit_price=request.POST.get(
                "unit-price"),
            purchases_id=purchases,
            # supplier_id=Supplier.objects.filter(
            #     supplier_name=request.POST.get("supplier-name")).first(),
        )
        # purchases.purchases_stock_available=int(request.POST.get("available-stock"))-int(request.POST.get("return-stock"))
        # purchases.save()
        inventory=Inventory.objects.filter(inventory_order_number=request.POST.get("order-number")).first()
        inventory.inventory_stock_available-=int(request.POST.get("return-stock"))
        inventory.save()
            # inventory_stock_available=int(request.POST.get("available-stock"))-int(request.POST.get("return-stock")))
        purchases.purchases_stock_available=inventory.inventory_stock_available
        purchases.purchases_purchased_quantity-=int(request.POST.get("return-stock"))
        purchases.save()

        suppiler_id=Supplier.objects.filter(id=purchases.purchases_supplier_id.id ).first()
        suppiler_id.supplier_dues-=int(request.POST.get("return-stock"))*int(request.POST.get("unit-price"))
        suppiler_id.save()

        # AddSupplierDues(suppiler_id.supplier_name, int(request.POST.get('model-item-quantity')) , -int(request.POST.get("return-stock"))*int(request.POST.get("unit-price")),-int((request.POST.get("remaining-stock-price")).split('=')[-1]),purchases)
        

        # PurchasesReturn.objects.create(status='Returned', inventory_id=Inventory.objects.get(
        # id=request.POST.get("update-id"))).save()
        supplier=Supplier.objects.filter(id=purchases.purchases_supplier_id.id)
        supplier.supplier_dues-=int(request.POST.get("return-stock"))*int(request.POST.get("unit-price"))
        supplier.save()
        print("successfully Added Return Purchases")
    except Exception as e:
        print("No data found {}".format(e))

def AddSupplierDues(name,total_amount,paid_amount,remaining_amount):
    try:
        supplier=Supplier.objects.filter(supplier_name=name).first()
        supplier.supplier_dues+=int(remaining_amount)
        SupplierPayment.objects.create(
            supplier_id=supplier,
            total_amount=total_amount,
            paid_amount=paid_amount,
            remaining_amount=remaining_amount,
        ).save()
        supplier.save()
        print("successfully Added Supplier Dues")
    except Exception as e:
        print("No data found {}".format(e))