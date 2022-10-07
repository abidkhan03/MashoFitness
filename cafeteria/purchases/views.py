from django.shortcuts import render
from cafeteria.Items.models import NonStock
from .models import Inventory, Purchases, PurchasesReturn
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import InventorySerializer, PurchasesSerializer, PurchasesReturnSerializer
from django.urls import reverse
from cafeteria.suppliers.models import Supplier
from .functions import AddReturnPurchases, UpdateInventory
from cafeteria.Items.serializer import NonStockSerializer
# Create your views here.
def inventory(request):
    if request.method=="POST":
        if request.POST.get("add-inventory-data"):
            print("add inventory data")
            UpdateInventory(request)
            
            return HttpResponseRedirect(reverse("inventory"))
    else:
        return render(request, "inventory.html", {
                    # 'addItems': Items.objects.all(),
                    'inventoryData': Inventory.objects.all().select_related('inventory_item_id'),
                    "suppliersName":Supplier.objects.all().values_list('supplier_name',flat=True).distinct(),
                    })  

def purchases(request):
    if request.method=="POST":
        print("purchases")
        if request.POST.get("return-stock-btn"):
            # print("add purchase return data")
            print(request.POST.get("model-id"))
            AddReturnPurchases(request)
            # UpdateInventory(request)
            return HttpResponseRedirect(reverse('purchaseReturn'))
            # HttpResponseRedirect(reverse('viewMembers'))
    else:
        return render(request, "purchases.html", {'purchases': Purchases.objects.all().select_related('purchases_item_id').select_related('purchases_supplier_id').order_by('-id'),})

def purchaseReturn(request):
    
    return render(request, "purchaseReturn.html",
    {
        'purchases': PurchasesReturn.objects.all().select_related('purchases_id').order_by('-id'),
    }
    )

@api_view(['GET'])
def updateInventoryQueryCall(request):
    value=request.GET.get("inventory-id")
    print(value)
    try:
        print(Inventory.objects.filter(id=value))
        return Response(InventorySerializer(Inventory.objects.filter(id=value),many=True).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})


@api_view(['GET'])
def addToCart(request):
    value=request.GET.get("id")
    # print(value)
    try:
        return Response(InventorySerializer(Inventory.objects.filter(inventory_item_id__item_name=value).first()).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def addToCartNonStock(request):
    value=request.GET.get("id")
    try:
        return Response(NonStockSerializer(NonStock.objects.filter(nonStock_item_name=value).first()).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def search_inventory_ItemName(request):
    if request.method == "GET":
        name=request.GET.get("item_name")
        print(name,'namem')
        inventory = Inventory.objects.filter(inventory_item_id__item_name__icontains=name).select_related('inventory_item_id').order_by("-id")
        if inventory:
            serializer = InventorySerializer(inventory, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"No inventory found"})

@api_view(['GET'])
def search_inventory_ItemCode(request):
    if request.method == "GET":
        code=request.GET.get("item_code")
        # print(name,'namem')
        inventory = Inventory.objects.filter(inventory_item_id__item_code__icontains=code).select_related('inventory_item_id').order_by("-id")
        if inventory:
            serializer = InventorySerializer(inventory, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"No inventory found"})


@api_view(['GET'])
def search_purchases_supplierName(request):
    if request.method == "GET":
        name=request.GET.get("supplier_name")
        print(name,'namem')
        purchases = Purchases.objects.filter(purchases_supplier_id__supplier_name__icontains=name).select_related('purchases_item_id').select_related('purchases_supplier_id').order_by("-id")
        if purchases:
            serializer = PurchasesSerializer(purchases,many=True).data
            return Response(serializer)
        else:
            return Response({"message":"No inventory found"})

@api_view(['GET'])
def search_purchases_orderNumber(request):
    if request.method == "GET":
        code=request.GET.get("order_name")
        # print(name,'namem')
        purchases = Purchases.objects.filter(purchases_order_number__icontains=code).select_related('purchases_item_id').select_related('purchases_supplier_id').order_by("-id")
        if purchases:
            serializer = PurchasesSerializer(purchases,many=True).data
            return Response(serializer)
        else:
            return Response({"message":"No inventory found"})



@api_view(['GET'])
def purchaseReturnCall(request,pk):
    if request.method == "GET":
        # print(name,'namem')
        purchases = Purchases.objects.filter(id=pk).select_related('purchases_item_id').select_related('purchases_supplier_id')
        print(purchases,'purchases')
        if purchases:
            serializer = PurchasesSerializer(purchases,many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"No inventory found"})

@api_view(['GET'])
def checkOrderNumber(request):
    try:
        code=request.GET.get("code")
        # print(item_code)
        if Purchases.objects.filter(purchases_order_number=code).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def checkRefferenceNumber(request):
    try:
        code=request.GET.get("code")
        # print(item_code)
        if Purchases.objects.filter(purchases_order_number=code).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def search_purchasesReturn_supplierName(request):
    if request.method == "GET":
        name=request.GET.get("supplier_name")
        print(name,'namem')
        purchases = PurchasesReturn.objects.filter(purchases_id__purchases_supplier_id__supplier_name__icontains=name).select_related('purchases_id').order_by("-id")
        if purchases:
            serializer = PurchasesReturnSerializer(purchases,many=True).data
            return Response(serializer)
        else:
            return Response({"message":"No inventory found"})

@api_view(['GET'])
def search_purchasesReturn_orderNumber(request):
    if request.method == "GET":
        code=request.GET.get("order_name")
        print(code,'namem')
        purchases = PurchasesReturn.objects.filter(purchases_id__purchases_order_number__icontains=code).select_related('purchases_id').order_by("-id")
        if purchases:
            serializer = PurchasesReturnSerializer(purchases,many=True).data
            return Response(serializer)
        else:
            return Response({"message":"No inventory found"})