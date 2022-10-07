from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from cafeteria.customers.models import CafeteriaCustomer

from cafeteria.sales.models import Sales
from .models import *
from .functions import CreateAdminUserFirst,addEmployee,updateEmployee,renewSalary
from django.shortcuts import render
from django.contrib import messages
from futsal.models import Match, Team
from snooker.models import snookerTableIncome
from django.db.models import Sum
from expenses.models import  expensesData
import datetime as dt
from theme.models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from cafeteria.salesTerminal.models import Order
# def fetchAllData(dbmodel):
#     data=dbmodel.objects.all()
#     ls=[]
#     for i in data:
#         ls.append(i)
#     return ls
def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

def index(request,employee_type=None):
    if request.user.is_superuser==True:
        print("super user")
        return render(request, 'index.html',
        {
            "total_member":f"{Member.objects.all().count():,}",
            "total_male":f"{Member.objects.filter(member_gender='Male').count():,}",
            "total_female":f"{Member.objects.filter(member_gender='Female').count():,}",
            'member_dues':f"{Fee.objects.filter(status='Unpaid').count():,}",
            'member_income':f"{zeroValue(Payment.objects.all().aggregate(Sum('payment_amount'))['payment_amount__sum']):,}",
            'member_expense':f"{zeroValue(expensesData.objects.filter(expenses_for='Gym').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            'gym_total_dues':f"{zeroValue(Fee.objects.filter(status='Unpaid').aggregate(Sum('remaining'))['remaining__sum']):,}",
            'futsal_total_team': f"{Team.objects.all().count():,}",
            'futsal_income':f"{zeroValue(Match.objects.filter(paid='Paid').aggregate(Sum('fee'))['fee__sum']):,}", 
            'futsal_expense': f"{zeroValue(expensesData.objects.filter(expenses_for='Futsal').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            'total_expenses':f"{zeroValue(expensesData.objects.aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            'today_snooker_income':f"{zeroValue(snookerTableIncome.objects.select_related('snooker_id').aggregate(Sum('amount'))['amount__sum']):,}",
            'snooker_expenses':f"{zeroValue(expensesData.objects.filter(expenses_for='Snooker').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            'cafeteria_enpense':f"{zeroValue(expensesData.objects.filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            'cafeteria_income':f"{zeroValue(Order.objects.all().aggregate(Sum('order_total_price'))['order_total_price__sum']  ):,}",
            'cafeteria_sales':Sales.objects.all().count(),
            'cafeteria_customer':CafeteriaCustomer.objects.all().count(),
        })
    elif request.user.is_superuser==False:
        print("employee user",request)
        if employee_type=='Cafeteria':
            return render(request, 'pos.html',)
        else:
            return render(request, 'index.html')
            
    else:
        return render(request, 'index.html')

# def Userlogin(request):
        if request.method=="POST":
            try:
                if request.POST.get('login-button'):
                    print("login button ********")
                    username=request.POST.get('user-name')
                    password=request.POST.get('password')
                    
                    if User.objects.get(username=username):
                        user=User.objects.get(username=username)
                        auth=authenticate(username=user.username,password=password)
                        
                        if auth:
                            print("auth")
                            login(request,auth)
                            return index(request, EmployeeRecord.objects.filter(id=request.user.id).first().employee_type)
                        else:
                            print("user login failed")
                            messages.error(request,"Invalid username or password")
                            return HttpResponseRedirect(reverse('login'))
                    else:
                        print("user login failed")
                        messages.error(request,"Invalid User")
                        return HttpResponseRedirect(reverse('login'))
            except Exception as e:
                print("login error ",e)
                messages.error(request,"Invalid User")
                return HttpResponseRedirect(reverse('login'))
        else:
            CreateAdminUserFirst()
            return render(request, 'login.html')

def employee(request):
    if request.method == "POST":
        print("post **&*&*&*&*&*&*&*&*&*&*&*& ")
        if request.POST.get('add-employee'):
            print("added employee button ********* ")
            addEmployee(request)
            return HttpResponseRedirect(reverse('employee'))
    else:

        return render(request, 'employee.html', {
            'employee':EmployeeRecord.objects.filter(id=request.user.id).first(),
            'employees': EmployeeRecord.objects.all().order_by("-id")}
            )


def logout_user(request):
    logout(request)
    return render(request,"login.html")


def editEmployee(request):
    if request.method == "POST":
        if request.POST.get("update-employee"):
            print("update employee button ********* ")
            updateEmployee(request)
            return HttpResponseRedirect(reverse('employee'))
        if request.POST.get("salary-renew"):
            print("salary renew button ********* ")
            if renewSalary(request):
                return HttpResponseRedirect(reverse('employee'))
    else:
        return render(request, 'editEmployee.html', {
            'user':EmployeeRecord.objects.filter(id=request.GET.get("e-id")).first(),
            'record':EmployeeSalary.objects.filter(employee_salary__id=request.GET.get("e-id")).select_related('employee_salary').order_by("-id")
            }
            )