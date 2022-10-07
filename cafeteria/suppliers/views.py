from django.shortcuts import render
from .functions import *
from .models import Supplier, SupplierPayment
from django.urls import  reverse
from django.http import HttpResponseRedirect
from .serializer import SupplierSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

def supplier(request):
    if request.method=="POST":
        if request.POST.get("add-supplier-data"):
            print("add supplier data")
            addSupplier(request)
            return HttpResponseRedirect(reverse("supplier"))
    else:
        return render(request, "supplier.html",
         {'supplierData': Supplier.objects.all()})

def updateSupplier(request):
    if request.method== "POST":
        if request.POST.get("update-supplier-data"):
            print("update supplier data")
            updateSupplierData(request)
            return HttpResponseRedirect(reverse("supplier"))
        if request.POST.get("supplier-payment"):
            print("supplier payment")
            PaymentDues(request)
            return HttpResponseRedirect(reverse("updateSupplier")+"?supplier="+request.POST.get('supplier-id'))
    else:
        return render(request, "updateSupplier.html", {'supplierData': Supplier.objects.filter(id=request.GET.get("supplier")).first(),
                                                        "payment": SupplierPayment.objects.filter(supplier_id=request.GET.get('supplier')).select_related('supplier_id').order_by('-id')})  

# api work
@api_view(['GET'])
def SearchBySupplierField(request):
    field=request.GET.get("field")
    value=request.GET.get("value")
    try:
        if field=="name":
            return Response(SupplierSerializer(Supplier.objects.filter(supplier_name__icontains=value).order_by("-id"),many=True).data)
        if field=="email":
            return Response(SupplierSerializer(Supplier.objects.filter(supplier_email__icontains=value).order_by("-id"),many=True).data)
        if field=="number":
            return Response(SupplierSerializer(Supplier.objects.filter(supplier_contact__icontains=value).order_by("-id"),many=True).data)
    except:
        return Response({"message":"No data found"})

@api_view(['GET'])
def deleteSupplier(request):
    try:
        delete_list=request.GET.getlist('arr[]')
        print(delete_list)
        if delete_list is not None:
            for i in delete_list:
                print(i)
                Supplier.objects.filter(id=int(i)).delete()
            return Response(SupplierSerializer(Supplier.objects.all().order_by("-id"),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})
        
@api_view(['GET'])
def getSupplierDetails(request):
    try:
        return Response(SupplierSerializer(Supplier.objects.filter(supplier_name=request.GET.get("supplierName")).first()).data)
    except Exception as e:
        print(e)
        return Response({"error":str(e)})