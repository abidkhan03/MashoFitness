from django.shortcuts import render
from django.http import HttpResponseRedirect

from cafeteria.sales.models import Sales
from cafeteria.salesTerminal.models import Order
from .models import *
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ItemSerializer, NonStockSerializer
from django.urls import reverse
from django.db.models import Sum
from expenses.models import expensesData
from cafeteria.customers.models import CafeteriaCustomer
def addItem(request):
    if request.method== "POST":
        if request.POST.get("save-button"):
            print("save button save button save button save button ")
            if ItemsAdd(request):
                print("item added success")
                return HttpResponseRedirect(reverse("addItem"))

        if request.POST.get("cancel-button"):
            return HttpResponseRedirect(reverse("addItem"))
        
        if request.POST.get("update-button"):
            print("update update update update update update button")
            UpdateItem(request)
            return HttpResponseRedirect(reverse("addItem"))

    else:
        return render(request, "addItem.html", {'addItems': Items.objects.all()})


def addNonStockItem(request):
    if request.method== "POST":
        if request.POST.get("save-button"):
            print("save button save button save button save button ")
            if addNonStockItems(request):
                print("item added success")
                return HttpResponseRedirect(reverse("addNonStockItem"))

        if request.POST.get("cancel-button"):
           return HttpResponseRedirect(reverse("addNonStockItem"))
        
        if request.POST.get("update-button"):
            print("update update update update update update button")
            updateNonStockItems(request)
            return HttpResponseRedirect(reverse("addNonStockItem"))


    else:
        return render(request, "addNonStockItem.html", {'nonStock': NonStock.objects.all()})

def pos(request):

    return render(request, "pos.html",
    {
        'income':Order.objects.all().aggregate(Sum('order_total_price'))['order_total_price__sum'],
        'expenses':expensesData.objects.filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum'],
        'monthlysales':Sales.objects.filter(order_id__order_date__month=datetime.now().month).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum'],
        'totalcustomers':CafeteriaCustomer.objects.all().count(),
        'totalsupplier':Supplier.objects.all().count(),
    }
    )


def barcodeLabel(request):
    return render(request, "barcodeLabel.html")

# api work
# api for items searching
@api_view(['GET'])
def SearchByItemField(request):
    field=request.GET.get("field")
    value=request.GET.get("value")
    print(field,value)
    try:
        if field=="Name":
            return Response(ItemSerializer(Items.objects.filter(
                        item_name__icontains=value).order_by('-id'),
                        many=True).data)
        elif field=="Code":
            return Response(ItemSerializer(Items.objects.filter(
                        item_code__icontains=value).order_by('-id'),
                        many=True).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})


# api for non-stock search items
@api_view(['GET'])
def SearchByStockField(request):
    field=request.GET.get("field")
    value=request.GET.get("value")
    print(field,value)
    try:
        if field=="Name":
            return Response(NonStockSerializer(NonStock.objects.filter(
                        nonStock_item_name__icontains=value).order_by('-id'),
                        many=True).data)
        elif field=="Code":
            return Response(NonStockSerializer(NonStock.objects.filter(
                        nonStock_item_code__icontains=value).order_by('-id'),
                        many=True).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})


@api_view(['GET'])
def UpdateItemQueryCall(request):
    value=request.GET.get("id")
    try:
        return Response(ItemSerializer(Items.objects.filter(id=value),many=True).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})


@api_view(['GET'])
def UpdateNonStockQueryCall(request):
    value=request.GET.get("nonStock-id")
    try:
        return Response(NonStockSerializer(NonStock.objects.filter(id=value),many=True).data)
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})


@api_view(['GET'])
def ItemCodeCheck(request):
    try:
        item_code=request.GET.get("item_code")
        # print(item_code)
        if Items.objects.filter(item_code=item_code).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def ItemNameCheck(request):
    try:
        item_name=request.GET.get("item_name")
        # print(item_code)
        if Items.objects.filter(item_name=item_name).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def NonStockItemCodeCheck(request):
    try:
        item_code=request.GET.get("item_code")
        # print(item_code)
        if NonStock.objects.filter(nonStock_item_code=item_code).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})

@api_view(['GET'])
def NonStockItemNameCheck(request):
    try:
        item_name=request.GET.get("item_name")
        # print(item_code)
        if NonStock.objects.filter(nonStock_item_name=item_name).exists():
            # print('if')
            return Response({"status":'fail'})
        else:
            # print('else')
            return Response({"status":'success'})
    except Exception as e:
        return Response({"message":"No data found {}".format(e)})