from django.shortcuts import render
from .models import RentalData, rentalPayment
from django.http import HttpResponseRedirect
from .functions import addRental, editRental, renew
from django.urls import reverse
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import RentalUpdateSerializer
import datetime as dt

def checkNone(data):
    if data == None:
        return 0
    else:
        return data

def checkMemberStarus():
    rent=RentalData.objects.all().select_related('active_rent_id')
    if rent:
        for i in rent:
            if (i.active_rent_id.rent_end_date-dt.date.today()).days<0:
                RentalData.objects.filter(id=i.id).update(payment_status="Expired")

def rental(request):
    if request.method == 'POST':
        print("post post post post ")
        if request.POST.get('rental-button'):
            print("rental button......")
            addRental(request)

            print(RentalData.objects.all())
            return HttpResponseRedirect(reverse('rental'))
    
    else:
        checkMemberStarus()
        return render(request, "rental.html",
         {'rentalData':RentalData.objects.all().select_related('active_rent_id').select_related("rent_attended_by")
         })

def updateRental(request):
    if request.method == 'POST':
        if request.POST.get('update-rental'):
            print("update rental button......")
            editRental(request)
            return HttpResponseRedirect(reverse('rental'))
        elif request.POST.get('rental-renew'):
            print("renew rental button......")
            renew(request)
            return HttpResponseRedirect(reverse('updateRental')+"?rent="+request.POST.get('rent-id'))
    else:
        return render(request, "updateRental.html", 
        {
            'rentalData':RentalData.objects.filter(id=request.GET.get('rent')).select_related('active_rent_id').select_related("rent_attended_by").first(),
            'payment':rentalPayment.objects.filter(rental_id=request.GET.get('rent')).select_related('rental_id').select_related('rent_payment_attended_by').order_by('-id'),
        })
    # return render(request, "updateRental.html",)

@api_view(['GET'])
def deleteRentalRecord(request):
    try:
        delete_list=request.GET.getlist('arr[]')
        print(delete_list)
        if delete_list is not None:
            for i in delete_list:
                print(i)
                RentalData.objects.filter(id=int(i)).delete()
            return Response(RentalUpdateSerializer(RentalData.objects.all().order_by("-id"),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})

@api_view(['GET'])
def SearchByRentalField(request):
    field=request.GET.get('field')
    value=request.GET.get('value')
    print(field,value)
    try:
        if field=="Name":
            return Response(RentalUpdateSerializer(RentalData.objects.filter(Full_name__icontains=value).order_by('-id'),many=True).data)

        elif field=="Contact":
            return Response(RentalUpdateSerializer(RentalData.objects.filter(contact_no__icontains=value).order_by('-id'),many=True).data) 
        
        elif field=="Shop":
            return Response(RentalUpdateSerializer(RentalData.objects.filter(shop_no__icontains=value).order_by('-id'),many=True).data)

    except Exception as e:
        print('SearchByRentalField',e)
        return Response({'message':"No data found"})

@api_view(['GET'])
def searchByRentalDate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        if from_date is not None and to_date is not None:
            return Response(RentalUpdateSerializer(RentalData.objects.filter(created_at__range=[from_date,to_date]).order_by('-id'),many=True).data)
    except:
        return Response({'message':"No data found"})

# Create your views here.
