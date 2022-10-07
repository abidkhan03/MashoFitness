from django.shortcuts import render
from expenses.models import expensesData
from django.db.models import Sum
from expenses.functions import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from expenses.serializer import *


# Create your views here.
def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

def cafeteriaExpenses(request):
    if request.method == "POST":
        if request.POST.get("add-expenses"):
            try:
                print("add expense")
                addExpense(request)
                messages.success(request, "Expense added successfully")
                return HttpResponseRedirect(reverse('cafeteriaExpenses'))
            except Exception as e:
                print("add expense", e)
                messages.error(request, "Expense added failed")
                return HttpResponseRedirect(reverse('cafeteriaExpenses'))
    else:
        return render(request, 'cafeteriaExpenses.html',
         {'all_expenses': expensesData.objects.filter(expenses_for='Cafeteria').order_by('-id'),
         'total_expenses':f"{zeroValue(expensesData.objects.filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
         'total_expenses_for_today':f"{zeroValue(expensesData.objects.filter(expenses_for='Cafeteria').filter(date=datetime.today()).aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
         })
    # return render(request, "cafeteriaExpenses.html")

def updateCafeteriaExpenses(request):
    if request.method == "POST":
        if request.POST.get("update-expenses"):
            if request.POST.get("comments"):
                comments=request.POST.get("comments")
            else:
                comments=''
            expensesData.objects.filter(id=request.POST.get("id")).update(
                date=request.POST.get("date"),
                account_head=request.POST.get("account-head"),
                paid_amount=request.POST.get("amount-paid"),
                payment_mode=request.POST.get("payment-mode"),
                expenses_for=request.POST.get("expenses-for"),
                receipent_name=request.POST.get("recipient-name"),
                description=request.POST.get("description"),
                comments=comments

            )
            return HttpResponseRedirect(reverse('cafeteriaExpenses'))
    else:
        print(request.GET.get("data"))
        return render(request, 'updateCafeteriaExpense.html',{
            'record': expensesData.objects.filter(id=request.GET.get("data"))[0],
        })
    # return render(request, "updateCafeteriaExpenses.html")



@api_view(['GET'])
def deleteCafeteriaExpense(request):
    # print(request.DELETE.get('delete_array'))
    try:
        delete_list=request.GET.getlist('arr[]')
        if delete_list is not None:
            for i in delete_list:
                print(i)
                expensesData.objects.filter(id=int(i)).delete()
            return Response(expensesSerializer(expensesData.objects.filter(expenses_for='Cafeteria').order_by('-id'),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})






@api_view(['GET'])
def searchByCafeteriaExpenseDate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        if from_date is not None and to_date is not None:
            return Response(expensesSerializer(expensesData.objects.filter(expenses_for='Cafeteria').filter(date__range=[from_date,to_date]).order_by('-id'),many=True).data)
        else:
            return Response({"error":str("Please select date")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchByCafeteriaExpenseHeadOfAccount(request):
    try:
        name=request.GET.get('searchbyname',None)
        if name is not None:
            return Response(expensesSerializer(expensesData.objects.filter(expenses_for='Cafeteria').filter(account_head__icontains=name).order_by('-id'),many=True).data)
        else:
            return Response({"error":str("Please select name")})
    except Exception as e:
        return Response({"error":str(e)})
