from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from expenses.models import expensesData
from snooker.serializer import CustomSeriazerSnooker
from .models import *
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

snooker_id=None
def snooker(request):
    global total_income,snooker_id
    if request.method == 'POST':
        if request.POST.get('add-table-income'):
            if addTableIncome(request,snooker_id):
                return HttpResponseRedirect(reverse('snooker'))
            else:
                return HttpResponse("add income error")
        
        if request.POST.get('add-snooker-income'):
            if updateSnookerIncome(request,snooker_id):
                snooker_id=addSnookerIncome(request.user.id)
                return HttpResponseRedirect(reverse('snooker'))
            else:
                return HttpResponse("update snooker income error")
    else:
        # if snooker_id is None:
        snooker_id=addSnookerIncome(request.user.id)
        return render(request, 'snooker.html', {
            'totalIncome': snookerIncome.objects.filter(id=snookerIncome.objects.last().id).annotate(total_income=Sum('snookertableincome__amount')).last().total_income,
            'record':snookerIncome.objects.all().annotate(total_income=Sum('snookertableincome__amount')).order_by('-id').select_related("snooker_attened_by"),
            'today_snooker_income':f"{zeroValue(snookerTableIncome.objects.select_related('snooker_id').filter(snooker_id__date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('amount'))['amount__sum']):,}",
            'snooker_expenses':f"{zeroValue(expensesData.objects.filter(expenses_for='Snooker').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
            
            })

def updateSnooker(request):
    global snooker_id
    if request.method=="POST":
        print(request.method)
        if request.POST.get("delete-button"):
            try:
                snookerTableIncome.objects.filter(id=request.POST.get("table-id")).delete()
                return render(request, 'updateSnooker.html' ,{
                'record':snookerTableIncome.objects.filter(snooker_id=request.POST.get("snooker-id")).select_related('snooker_id'),
                "day_details":snookerIncome.objects.filter(id=request.POST.get('snooker-id')).annotate(total_income=Sum('snookertableincome__amount')).select_related("snooker_attened_by").last()
                # "day_details":snookerIncome.objects.raw(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id where s.id=={int(request.POST.get('snooker-id'))} GROUP by t.snooker_id_id order by s.id desc;")[0],
                })
            except IndexError as e:
                return HttpResponseRedirect(reverse('snooker'))
        if request.POST.get("update-button"):
            return render(request,"editSnooker.html",
            {'record':snookerTableIncome.objects.filter(id=request.POST.get("table-id"))[0]})

        if request.POST.get("update-income"):
            snookerIncome.objects.filter(id=request.POST.get("income-id")).update(
                description=request.POST.get("description"), date=request.POST.get("date")
            )
            return HttpResponseRedirect(reverse('snooker'))
    else:
        
        return render(request, 'updateSnooker.html' ,{
            'record':snookerTableIncome.objects.filter(snooker_id=request.GET.get("data")).select_related('snooker_id'),
            "day_details":snookerIncome.objects.filter(id=request.GET.get('data')).annotate(total_income=Sum('snookertableincome__amount')).select_related("snooker_attened_by").last()
            # "day_details":snookerIncome.objects.raw(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id where s.id=={int(request.GET.get('data'))} GROUP by t.snooker_id_id order by s.id desc;")[0],
        })


def editSnooker(request):
    if request.method == "POST":
        if request.POST.get("edit-table-income"):
            row_id=request.POST.get("row-id")
            s_id=request.POST.get("snooker-id")
            snookerTableIncome.objects.filter(id=row_id).update(
                    amount=request.POST.get("amount"), table_number=request.POST.get("table-number"),
                    minutes_per_table=request.POST.get("minutes-per-table")
            )
            return render(request, 'updateSnooker.html' ,{
            'record':snookerTableIncome.objects.filter(snooker_id=s_id).select_related('snooker_id'),
            "day_details":snookerIncome.objects.filter(id=s_id).annotate(total_income=Sum('snookertableincome__amount')).select_related("snooker_attened_by").last()
            # "day_details":snookerIncome.objects.raw(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id where s.id=={int(s_id)} GROUP by t.snooker_id_id order by s.id desc;")[0],

        })

# api for snooker

@api_view(['GET'])
def deleteSnookerRecord(request):
    try:
        delete_list=request.GET.getlist('arr[]')
        print(delete_list)
        if delete_list is not None:
            for i in delete_list:
                print(i)
                snookerIncome.objects.filter(id=int(i)).delete()
            return Response(CustomSeriazerSnooker(snookerIncome.objects.all().annotate(total_income=Sum('snookertableincome__amount')).order_by('-id').select_related("snooker_attened_by").select_related('snooker_attened_by__user'),many=True).data)
        else:
            # messages.info(request,"No data found")
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})

@api_view(['GET'])
def SearchBySnookerData(request):
    try:
        print(request.GET)
        resultperpage=request.GET.get('resultperpage',None)
        searchbytype=request.GET.get('searchbytype',None)
        if searchbytype!='':
            if resultperpage!="all":
                print("if resultperpage!=all:")
                print(searchbytype)
                return Response(CustomSerializer(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id  where s.attened_by=='{searchbytype}' GROUP by t.snooker_id_id order by s.id desc limit {int(resultperpage)};"))

            else:
                print("if resultperpage==all:")
                return Response(CustomSerializer(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id  where s.attened_by=='{searchbytype}' GROUP by t.snooker_id_id order by s.id desc;"))
        else:
            
            if resultperpage!="all":
                print("if resultperpage!=all:  else if")
                return Response(CustomSerializer(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id GROUP by t.snooker_id_id order by s.id desc limit {int(resultperpage)};;"))
            else:
                print("if resultperpage==all: else else")
                return Response(CustomSerializer(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id GROUP by t.snooker_id_id order by s.id desc;"))
        
    except Exception as e:
        return Response({"error":str(e)})


@api_view(['GET'])
def searchBySnookerDate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        if from_date is not None and to_date is not None:
            return Response(CustomSeriazerSnooker(snookerIncome.objects.filter(date__range=[from_date,to_date]).annotate(total_income=Sum('snookertableincome__amount')).order_by('-id').select_related("snooker_attened_by"),many=True).data)
            # return Response(CustomSerializer(f"select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income from snooker_snookerincome s join snooker_snookertableincome t on s.id=t.snooker_id_id where s.date BETWEEN  '{from_date}' and '{to_date}'  GROUP by t.snooker_id_id order by s.id desc ;"))
        else:
            return Response({"error":str("Please select date")})
    except Exception as e:
        return Response({"error":str(e)})