from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from django.db.models import Sum
from employees.models import EmployeeRecord

def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

def expenses(request):
    if request.method == "POST":
        if request.POST.get("add-expenses"):
            try:
                print("add expense")
                addExpense(request)
                messages.success(request, "Expense added successfully")
                return HttpResponseRedirect(reverse('expenses'))
            except Exception as e:
                print("add expense",e)
                messages.error(request, "Expense added failed")
                return HttpResponseRedirect(reverse('expenses'))
    else:
        return render(request, 'expenses.html',
         {'all_expenses': expensesData.objects.order_by('-id'),
         'total_expenses':f"{zeroValue(expensesData.objects.aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
         'total_expenses_for_today':f"{zeroValue(expensesData.objects.filter(date=datetime.today()).aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
         "user":EmployeeRecord.objects.filter(id=request.user.id).first()
         
         })

def updateExpense(request):
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
            return HttpResponseRedirect(reverse('expenses'))
    else:
        print(request.GET.get("data"))
        return render(request, 'updateExpense.html',{
            'record': expensesData.objects.filter(id=request.GET.get("data"))[0],
            "user":EmployeeRecord.objects.filter(id=request.user.id).first()
        })



# api work

# @api_view(['GET'])
# def get_membershipCategory(request):
#     print(request.method)
#     if request.method == "GET":
#         category_name=request.query_params.get('category_name',None)
#         category_class=request.query_params.get('category_class',None)
#         category_gender=request.query_params.get("category_gender",None)
#         print(category_class,category_name)
#         if category_class is not None and category_class is not None and category_gender is not None:
#             try:
#                 return Response(MembershipCategorySerializer(MembershipCategory.objects.all().filter(category_name=category_name).filter(category_class=category_class).filter(category_gender=category_gender),many=True).data)
#             except Exception as e:
#                 return Response({"error":e})
        

@api_view(['GET'])
def deleteExpense(request):
    # print(request.DELETE.get('delete_array'))
    try:
        delete_list=request.GET.getlist('arr[]')
        if delete_list is not None:
            for i in delete_list:
                print(i)
                expensesData.objects.filter(id=int(i)).delete()
            return Response(expensesSerializer(expensesData.objects.order_by('-id'),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})


@api_view(['GET'])
def searchByExpenseData(request):
    try:
        print(request.GET)
        resultperpage=request.GET.get('resultperpage',None)
        searchbytype=request.GET.get('searchbytype',None)
        if searchbytype!='':
            if resultperpage!="all":
                print("if resultperpage!=all:")
                return Response(expensesSerializer(expensesData.objects.order_by('-id').filter(expenses_for=searchbytype)[:int(resultperpage)],many=True).data)

            else:
                print("if resultperpage==all:")
                return Response(expensesSerializer(expensesData.objects.order_by('-id').filter(expenses_for=searchbytype),many=True).data)
        else:
            
            if resultperpage!="all":
                print("if resultperpage!=all:  else if")
                return Response(expensesSerializer(expensesData.objects.order_by('-id')[:int(resultperpage)],many=True).data)
            else:
                print("if resultperpage==all: else else")
                return Response(expensesSerializer(expensesData.objects.order_by('-id'),many=True).data)
        
    except Exception as e:
        return Response({"error":str(e)})



@api_view(['GET'])
def searchByExpenseDate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        if from_date is not None and to_date is not None:
            return Response(expensesSerializer(expensesData.objects.filter(date__range=[from_date,to_date]).order_by('-id'),many=True).data)
        else:
            return Response({"error":str("Please select date")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchByExpenseHeadOfAccount(request):
    try:
        name=request.GET.get('searchbyname',None)
        if name is not None:
            return Response(expensesSerializer(expensesData.objects.filter(account_head__icontains=name).order_by('-id'),many=True).data)
        else:
            return Response({"error":str("Please select name")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchByModule(request):
    try:
        module=request.GET.get('module',None)
        if module is not None:
            return Response({'amount_module':expensesData.objects.filter(expenses_for__icontains=module).aggregate(Sum('paid_amount'))['paid_amount__sum']})
        else:
            return Response({"error":str("Please select module")})
    except Exception as e:
        return Response({"error":str(e)})