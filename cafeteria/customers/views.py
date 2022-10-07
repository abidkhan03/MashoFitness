from django.shortcuts import render
from .models import CafeteriaCustomer
from .functions import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CustomerSerializer
# Create your views here.

def customer(request):
    if request.method == "POST":
        if request.POST.get("add-customer-data"):
            print("add customer data")
            addCustomer(request)
            return HttpResponseRedirect(reverse("customer"))
    else:
        return render(request, "customer.html", {'customerData': CafeteriaCustomer.objects.all()})


def updateCustomer(request):
    if request.method== "POST":
        if request.POST.get("update-customer-data"):
            print("update customer data")
            updateCustomerData(request)
            return HttpResponseRedirect(reverse("customer"))
        if request.POST.get("customer-payment"):
            print("customer payment")
            PaymentDues(request)
            return HttpResponseRedirect(reverse("updateCustomer")+"?customer="+request.POST.get('customer-id'))
    
    else:
        return render(request, "updateCustomer.html", {'customerData': CafeteriaCustomer.objects.filter(id=request.GET.get("customer")).first(),
                                                        "payment": CustomerPayment.objects.filter(customer_id=request.GET.get('customer')).select_related('customer_id')})

# api work
@api_view(['GET'])
def SearchByCustomerField(request):
    field=request.GET.get("field")
    value=request.GET.get("value")
    try:
        if field=="name":
            return Response(CustomerSerializer(CafeteriaCustomer.objects.filter(customer_name__icontains=value).order_by("-id"),many=True).data)
        if field=="number":
            return Response(CustomerSerializer(CafeteriaCustomer.objects.filter(customer_contact__icontains=value).order_by("-id"),many=True).data)
        if field=="status":
            return Response(CustomerSerializer(CafeteriaCustomer.objects.filter(customer_status__icontains=value).order_by("-id"),many=True).data)
    except:
        return Response({"message":"No data found"})

@api_view(['GET'])
def deleteCustomer(request):
    try:
        delete_list=request.GET.getlist('arr[]')
        print(delete_list)
        if delete_list is not None:
            for i in delete_list:
                print(i)
                CafeteriaCustomer.objects.filter(id=int(i)).delete()
            return Response(CustomerSerializer(CafeteriaCustomer.objects.all().order_by("-id"),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})