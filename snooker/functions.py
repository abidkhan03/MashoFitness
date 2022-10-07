from datetime import datetime
from .models import snookerIncome,snookerTableIncome
from employees.models import EmployeeRecord

record="""
select s.id, s.description, s.attened_by, s.date , sum(t.amount) as total_income
from snooker_snookerincome s
join snooker_snookertableincome t on s.id=t.snooker_id_id GROUP by t.snooker_id_id
order by s.id desc
"""
def addSnookerIncome(id):
    try:
        if snookerIncome.objects.all().exists():
            print('record exist')
            if snookerIncome.objects.last().status is False:
                print('status False',snookerIncome.objects.last().status)
                return snookerIncome.objects.last()
            else:
                print('status True')
                print("snooker income added")
                add=snookerIncome.objects.create(
                description="",
                snooker_attened_by=EmployeeRecord.objects.filter(id=id).first(), # EmployeeRecord.objects.filter(employee_username=request.POST.get("attended-by")).first()
                date=datetime.now()
                )
                add.save()
                return add
        else:
            print("create new record")
            add=snookerIncome.objects.create(
            description="",
            snooker_attened_by=EmployeeRecord.objects.filter(id=id).first(), # EmployeeRecord.objects.filter(employee_username=request.POST.get("attended-by")).first()
            date=datetime.now()
            )
            add.save()
            return add

    except Exception as e:
        print("add income error:",e)

def addTableIncome(request,id):
    try:
        print("add table income")
        add=snookerTableIncome.objects.create(
        amount=request.POST.get("amount"),
        table_number=request.POST.get("table-number"),
        minutes_per_table=request.POST.get("minutes-per-table"),
        snooker_id=id
        )
        add.save()
        print("add table income success")
        return True
    except Exception as e:
        print("add table income error:",e)
        return False
        
def updateSnookerIncome(request,obj):
    try:
        if request.POST.get("description"):
            des=request.POST.get("description")
        else:
            des=''
        snookerIncome.objects.filter(id=obj.id).update(
        description=des,
        status=True,
        snooker_attened_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first(),
        date=request.POST.get("date")
        )
        return True
    except Exception as e:
        print("update income error:",e)
        return False

def CustomSerializer(query):
    join=snookerIncome.objects.raw(query)
    data=[]
    for i in join:
        data.append({"id":i.id,"description":i.description,"attened_by":i.attened_by,"date":i.date,"total_income":i.total_income})
    print("data",data)
    return data