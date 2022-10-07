from .models import Supplier, SupplierPayment
from cafeteria.purchases.models import Inventory, PurchasesReturn

def addSupplier(request):
    try:
        add_supplier = Supplier.objects.create(supplier_account=request.POST.get("supplier-account"),
                        supplier_name=request.POST.get("supplier-name"),
                        supplier_contact=request.POST.get("supplier-contact"),
                        supplier_email=request.POST.get("supplier-email"),
                        supplier_status=request.POST.get("supplier-status"),
                        supplier_address=request.POST.get("supplier-address"),
                        supplier_city=request.POST.get("supplier-city"),
                        supplier_country=request.POST.get("supplier-country")
                        )
        add_supplier.save()

        # add_inventory = Inventory.objects.create(
        #                 inventory_unit_price= 0,
        #                 inventory_net_price= 0,
        #                 inventory_purchased_quantity=0,
        #                 inventory_sub_total= 0,
        #                 inventory_item_total=0,
        #                 inventory_order_number=0,
        #                 inventory_reference_number=0,
        #                 inventory_stock_in_shop=0,
        #                 supplier_id=add_supplier,
                        
        #                 )
        # add_inventory.save()
        return add_supplier
    except Exception as e:
        print("Error in adding supplier data", e)
        return False

def updateSupplierData(request):
    try:
        Supplier.objects.filter(id=request.POST.get("update-id")).update(
                        supplier_account=request.POST.get("supplier-account"),
                        supplier_name=request.POST.get("supplier-name"),
                        supplier_contact=request.POST.get("supplier-contact"),
                        supplier_email=request.POST.get("supplier-email"),
                        supplier_status=request.POST.get("supplier-status"),
                        supplier_address=request.POST.get("supplier-address"),
                        supplier_city=request.POST.get("supplier-city"),
                        supplier_country=request.POST.get("supplier-country")
                        )
    except Exception as e:
        print("Error in updating supplier data", e)
        return False

def PaymentDues(request):
    try:
        supplier=Supplier.objects.get(id=request.POST.get('supplier-id'))
        SupplierPayment.objects.create(
                                payment_date=request.POST.get("payment-date"),
                                total_amount=request.POST.get("dues"),
                                paid_amount=request.POST.get("payment"),
                                remaining_amount=request.POST.get("remaining"),
                                supplier_id=supplier,
                                
                                )

        supplier.supplier_dues=request.POST.get("remaining")
        supplier.save()
        print("payment done")
    except Exception as e:
        print("Error in updating payment", e)
        return False