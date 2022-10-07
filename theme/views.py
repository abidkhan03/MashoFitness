from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
# from theme.functions import fetchUniqueCategoryName
from .models import MembershipCategory, Member, BodyAssesments
from .serializers import MembershipCategorySerializer, MemberSerializer,PaymentSerializer,BillSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .functions import *
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponseRedirect
from expenses.models import  expensesData
import datetime as dt
from employees.models import EmployeeRecord
from smsSetting.models import SmsModle
from django.db.models import Q

def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

def fetchAllData(dbmodel):
    data=dbmodel.objects.all()
    ls=[]
    for i in data:
        ls.append(i)
    return ls

checkMemberStarus()


def viewRecord(request):
    checkMemberStarus()
    if request.method=="GET":
        bill=Bill.objects.filter(member_id=request.GET.get("cid")).select_related("member_id").select_related("fee_id").select_related("subscription_id").order_by("-id")
        return render(request, "viewRecord.html", {"member_name":bill[0].member_id.member_name,"memberID":bill[0].member_id.id,'member_serial':bill[0].member_id.member_serial_no,"bill":bill})
                        



def printform(request):
    return render(request,"printform.html")

def gymSetting(request):
    if request.method == "POST":
        if request.POST.get("addcategory"):
            category = request.POST.get("membershipcategory")
            duration = request.POST.get("membershipduration")
            fee = request.POST.get("membershipfee")
            gender = request.POST.get("membershipgender") 
            add_date = MembershipCategory.objects.create(category_name=category ,category_class=request.POST.get("membership-class"), category_months=duration, category_fee=fee, category_gender=gender)
            add_date.save()
            return HttpResponseRedirect(reverse("gymSetting"))
        if request.POST.get("editcall"):
            return render(request,"GymSetting/editGymSetting.html",
             {'all_data': MembershipCategory.objects.all().filter(id=request.POST.get("cid"))[0]})

    else:
        
        return render(request,"GymSetting/gymSetting.html", {'all_data': fetchAllData(MembershipCategory)})

def editGymSetting(request):
    if request.method == "POST":
        if request.POST.get("update-category"):
            MembershipCategory.objects.all().filter(id=request.POST.get("cid")).update(
                category_name=request.POST.get("membershipcategory"), category_class=request.POST.get("membership-class"),
                category_months=request.POST.get("membershipduration"),
                category_fee=request.POST.get("membershipfee"), category_gender=request.POST.get("membershipgender"))
            return HttpResponseRedirect(reverse('gymSetting'))
    else:
        return HttpResponseRedirect(reverse('gymSetting'))

def gymManagement(request):
    checkMemberStarus()
    return render(request,"gymManagement.html",{
        "zipdata":Member.objects.all().select_related('member_membership_id').order_by("-id")[:10],
        "total_member":Member.objects.all().count(),
        "total_male":Member.objects.filter(member_gender="Male").count(),
        "total_female":Member.objects.filter(member_gender="Female").count(),
        'member_dues':Member.objects.filter(active_fee_id__status="Unpaid").count(),
        'income':f"{zeroValue(Payment.objects.filter(payment_created_at__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('payment_amount'))['payment_amount__sum']):,}",
        'expense':f"{zeroValue(expensesData.objects.filter(expenses_for='Gym').filter(date__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'total_dues':f"{zeroValue(Fee.objects.filter(status='Unpaid').aggregate(Sum('remaining'))['remaining__sum']):,}",
        'sms_list':SmsModle.objects.values_list('smsModule',flat=True).distinct(),
        'active_member':Member.objects.filter(~Q(active_fee_id__status="Expired")).count(),
        
        
        # 'zipdata':Member.objects.raw("SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;"),
    })

def memberDetails(request):
    if request.method == "POST":
        if request.POST.get("edit-member"):
            return render(request,"memberDetails.html",
            {'all_data': Member.objects.all().filter(id=request.POST.get("cid")).select_related("member_membership_id")[0]
            })
        
        if request.POST.get("update-button"):
            if request.FILES:
                f=request.FILES["photo"]
                fs = FileSystemStorage()
                filename = fs.save(f.name, f)
                uploaded_file_url = fs.url(filename)
            
                Member.objects.all().filter(id=request.POST.get("cid")).update(member_name=request.POST.get("name"), 
                    member_father_name=request.POST.get("father_name"), 
                    member_cnic=NoneValue(request.POST.get("cnic")), 
                    member_occupation=NoneValue(request.POST.get("occupation")), 
                    member_gender=request.POST.get("gender"), 
                    member_address=NoneValue(request.POST.get("address")),
                    member_contact=request.POST.get("contact"), 
                    member_emergency_contact=NoneValue(request.POST.get("alternative-number")),
                    member_dob=NoneValue(request.POST.get("dob")), 
                    member_age=NoneValue(request.POST.get("age")), 
                    member_blood_group=NoneValue(request.POST.get("blood_group")), 
                    member_card_id=request.POST.get("card_id"),
                    member_serial_no=request.POST.get("serial-no"), 
                    member_target=NoneValue(request.POST.get("target")),
                    member_image=filename )
            else:
                    Member.objects.all().filter(id=request.POST.get("cid")).update(
                    member_name=request.POST.get("name"), 
                    member_father_name=request.POST.get("father_name"), 
                    member_cnic=NoneValue(request.POST.get("cnic")), 
                    member_occupation=NoneValue(request.POST.get("occupation")), 
                    member_gender=request.POST.get("gender"), 
                    member_address=NoneValue(request.POST.get("address")),
                    member_contact=request.POST.get("contact"), 
                    member_emergency_contact=NoneValue(request.POST.get("alternative-number")),
                    member_dob=NoneValue(request.POST.get("dob")), 
                    member_age=NoneValue(request.POST.get("age")), 
                    member_blood_group=NoneValue(request.POST.get("blood_group")), 
                    member_card_id=request.POST.get("card_id"),
                    member_serial_no=request.POST.get("serial-no"), 
                    member_target=NoneValue(request.POST.get("target")))
            Fee.objects.filter(member_id=request.POST.get("cid")).update(status=request.POST.get("paymentstatus"))
            return HttpResponseRedirect(reverse('viewMembers'))
        if request.POST.get("pay-installment"):
            if update_payment_installment(request):
                bill=Bill.objects.filter(member_id=request.POST.get("cid")).select_related("member_id").select_related("fee_id").select_related("subscription_id").order_by("-id")
                return render(request, "viewRecord.html", {"member_name":bill[0].member_id.member_name,
                    'bill': bill,})
                # return render(request, "viewMembers.html", {'zipdata':Member.objects.all().select_related('member_membership_id').select_related('active_fee_id').order_by('-id') ,})
            else:
                return HttpResponse(request,"error  in update intallment")
                # return render(request, "viewMembers.html", {'zipdata':Member.objects.all().select_related('member_membership_id').select_related('active_fee_id').order_by('-id') ,})
        if request.POST.get("submit-button"):
            if request.POST.get("paidamount") and request.POST.get("remainingamount"):
                renewSubscription(request,False)
                # bill=Bill.objects.filter(member_id=request.POST.get("cid")).select_related("member_id").select_related("fee_id").select_related("subscription_id").order_by("-id")
                return HttpResponseRedirect(reverse("viewRecord")+"?cid="+request.POST.get("cid"))
            else:
                renewSubscription(request,True)
                # bill=Bill.objects.filter(member_id=request.POST.get("cid")).select_related("member_id").select_related("fee_id").select_related("subscription_id").order_by("-id")
                return HttpResponseRedirect(reverse("viewRecord")+"?cid="+request.POST.get("cid"))
    else:
        member=Member.objects.all().filter(id=request.GET.get('data')).select_related("member_membership_id").select_related("active_fee_id")[0]
        payment=Payment.objects.filter(fee_id=member.active_fee_id).aggregate(Sum('payment_amount'))
        
        return render(request,"memberDetails.html",
            {'all_data': member,
            "payment":payment['payment_amount__sum'],
            "category":fetchUniqueCategoryName(MembershipCategory)
            })

def addMember(request):
    if request.method=="POST":
        if request.POST.get("addmembersubmit"):
            try:
                if request.POST.get("paidamount") and request.POST.get("remainingamount"):
                    addMemberRecord(request,False)
                    # join=Member.objects.raw("SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;")
                    messages.success(request, 'User Added Successful') # Any message you wish
                    # return render(request,"addMember.html", 
                    # {
                    #     'category':fetchUniqueCategoryName(MembershipCategory),
                    #     'zipdata':Member.objects.all().select_related('member_membership_id').order_by('-id'),
                    # })    
                    return HttpResponseRedirect(reverse('addMember'))               

                else:
                    addMemberRecord(request,True)
                    # join=Member.objects.raw("SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;")
                    messages.success(request, 'User Added Successful') # Any message you wish
                    # return render(request,"addMember.html", 
                    # {
                    #     'category':fetchUniqueCategoryName(MembershipCategory),
                    #     'zipdata':Member.objects.all().select_related('member_membership_id').order_by('-id'),
                    # })
                    return HttpResponseRedirect(reverse('addMember'))

            except Exception as e:
                    print("add member call",e)
                    messages.error(request, f'Add member error {e}') # Any message you wish
                    # return render(request,"addMember.html", 
                    # {
                    #     'category':fetchUniqueCategoryName(MembershipCategory),
                    #     'zipdata':Member.objects.all().select_related('member_membership_id').order_by('-id'),
                    # })
                    return HttpResponseRedirect(reverse('addMember')) 

        if request.POST.get("edit"):
            form_data = Member.objects.all().filter(id=request.POST.get("id"))[0]
            print(form_data)
            return render(request, "MemberDetails.html", {'update_data': form_data})
      
            
    else:
        # print(Member.objects.all().select_related("membershp_id")[0].payment_status)
        # join=Member.objects.raw("SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;")
        return render(request, "addMember.html",
             {
                        "user":EmployeeRecord.objects.filter(id=request.user.id).first(),
                        'category':fetchUniqueCategoryName(MembershipCategory),
                        'zipdata':Member.objects.all().select_related('member_membership_id').select_related('active_fee_id').order_by('-id'),
                        'sms_list':SmsModle.objects.values_list('smsModule',flat=True).distinct(),
                    })   

def viewMembers(request):
    if request.method=="POST":
        if request.POST.get("edit-member"):
            # Member.objects.raw(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id where theme_member.id={request.POST.get('cid')} ;")
            return render(request,"memberDetails.html",
            {'all_data': Member.objects.all().filter(id=request.POST.get("cid"))[0]
            })
            # form_data = Member.objects.all().filter(id=request.POST.get("cid"))[0]
            # print(form_data)
            # return render(request, "MemberDetails.html", {'all_data': form_data})
        
    else:
        # Member.objects.raw("SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;")
        return render(request, 'viewMembers.html',{
            'zipdata':Member.objects.all().select_related('member_membership_id').order_by('-id'),
            'sms_list':SmsModle.objects.values_list('smsModule',flat=True).distinct(),
        })

def bodyAssesments(request):
    print("requset data **** ", request.method)
    if request.method == "POST":
        if request.POST.get("add-button"):
            print(Member.objects.filter(id=request.POST.get("member_id")))
            addBodyAssesment(request) 
            return HttpResponseRedirect(reverse('bodyAssesments')+"?data="+request.POST.get("member_id"))

    else:
        try:
            if request.GET.get("delete_id"):
                member_id=BodyAssesments.objects.filter(id=request.GET.get("delete_id"))[0].member_id.id
                BodyAssesments.objects.filter(id=request.GET.get("delete_id")).delete()
                print(BodyAssesments.objects.filter(member_id=member_id).select_related("member_id").order_by("-id"))
                return HttpResponseRedirect(reverse('bodyAssesments')+"?data="+str(member_id))
            else:
                print(Member.objects.filter(id=request.GET.get('data')))
                return render(request, "bodyAssesments.html", {"all_data": Member.objects.all().filter(id=request.GET.get('data'))[0],
                                        'zipdata': BodyAssesments.objects.filter(member_id=request.GET.get("data")).select_related("member_id").order_by("-id"), })
        except Exception as e:
            print(e)


# """"
# API WORK 
# """

@api_view(['GET'])
def get_membershipCategory(request):
    print(request.method)
    if request.method == "GET":
        category_name=request.query_params.get('category_name',None)
        category_class=request.query_params.get('category_class',None)
        category_gender=request.query_params.get("category_gender",None)
        print(category_class,category_name)
        if category_class is not None and category_class is not None and category_gender is not None:
            try:
                return Response(MembershipCategorySerializer(MembershipCategory.objects.all().filter(category_name=category_name).filter(category_class=category_class).filter(category_gender=category_gender),many=True).data)
            except Exception as e:
                return Response({"error":e})
        

@api_view(['GET'])
def deleteMember(request):
    # print(request.DELETE.get('delete_array'))
    try:
        delete_list=request.GET.getlist('arr[]')
        if delete_list is not None:
            for i in delete_list:
                print(i)
                Member.objects.filter(id=int(i)).delete()
            return Response(MemberSerializer(Member.objects.all().select_related('member_membership_id').select_related('active_fee_id').order_by('-id'),many=True).data)
        else:
            messages.info(request,"No data found")
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})


@api_view(['GET'])
def searchbydata(request):
    try:
        print(request.GET)
        resultperpage=request.GET.get('resultperpage',None)
        searchbytype=request.GET.get('searchbytype',None)
        print(resultperpage)
        print(type(resultperpage))
        if searchbytype!='':
            if resultperpage!="all":
                print("if resultperpage!=all:")
                # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id where  theme_payment.payment_status='{searchbytype}' order by theme_member.id DESC LIMIT {int(resultperpage)};")
                return Response(MemberSerializer(Member.objects.all().select_related('member_membership_id').select_related("active_fee_id").filter(active_fee_id__status=searchbytype).order_by('-id')[:int(resultperpage)],many=True).data)
            else:
                print("if resultperpage==all:")
                # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id where  theme_payment.payment_status='{searchbytype}' order by theme_member.id DESC;")
                return Response(MemberSerializer(Member.objects.all().select_related('member_membership_id').select_related("active_fee_id").filter(active_fee_id__status=searchbytype).order_by('-id'),many=True).data)
        else:
            if resultperpage!="all":
                print("if resultperpage!=all:  else if")
                # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC LIMIT {int(resultperpage)};")
                return Response(MemberSerializer(Member.objects.all().select_related('member_membership_id').select_related("active_fee_id").order_by('-id')[:int(resultperpage)],many=True).data)
            else:
                print("if resultperpage==all: else else")
                # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id order by theme_member.id DESC;")
                return Response(MemberSerializer(Member.objects.all().select_related('member_membership_id').select_related("active_fee_id").order_by('-id'),many=True).data)
    except Exception as e:
        return Response({"error":str(e)})


@api_view(['GET'])
def searchbydate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        if from_date is not None and to_date is not None:
            # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id where  theme_member.member_created_at between '{from_date}' and '{to_date}' order by theme_member.id DESC;")
            return Response(MemberSerializer(Member.objects.all().select_related("member_membership_id").select_related("active_fee_id").order_by('-id').filter(member_created_at__range=[from_date,to_date]),many=True).data)
        else:
            return Response({"error":str("Please select date")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchbyname(request):
    try:
        name=request.GET.get('searchbyname',None)
        if name is not None:
            # CustomizeSerializer(f"SELECT * from theme_member JOIN theme_membershipcategory on theme_member.member_membership_id_id=theme_membershipcategory.id join theme_payment on theme_member.id=theme_payment.member_id_id where  theme_member.member_name like '%{name}%' order by theme_member.id DESC;")
            return Response(MemberSerializer(Member.objects.all().select_related("member_membership_id").select_related("active_fee_id").order_by('-id').filter(member_name__icontains=name),many=True).data)
        else:
            return Response({"error":str("Please select name")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def testing(request):
    try:
        return Response(PaymentSerializer(Payment.objects.all().filter(fee_id__member_id=28),many=True).data)
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchBillDate(request):
    try:
        from_date=request.GET.get('fromdate',None)
        to_date=request.GET.get('todate',None)
        id=request.GET.get('id',None)
        if from_date is not None and to_date is not None:
            return Response(BillSerializer(Bill.objects.filter(member_id=id).filter(bill_created_at__range=[from_date,to_date]),many=True).data)
        else:
            return Response({"error":str("Please select date")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def ViewBillCall(request):
    try:
        id=request.GET.get('id',None)
        print("bill id",id)
        if id is not None:
            return Response(BillSerializer(Bill.objects.filter(id=id)[0],many=False).data)
        else:
            return Response({"error":str("Please select bill id")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def getExpireRemainingDays(request):
    try:
        if id is not None:
            date = dt.date.today()
            start_week = date - dt.timedelta(date.weekday())
            end_week = start_week + dt.timedelta(6)
            entries = Member.objects.filter(member_membership_expiry_date__range=[start_week, end_week])
            return Response(MemberSerializer(entries,many=True).data)
        else:
            return Response({"error":str("Please select member id")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def checkSerialNo(request):
    try:
        serial_no=request.GET.get('serial_no',None)
        if serial_no is not None:
            if Member.objects.filter(member_serial_no=serial_no).exists():
                return Response({"status":"Serial no already exists"})
            else:
                return Response({"status":str("success")})
        else:
            return Response({"error":str("Please select serial no")})
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchbygender(request):
    try:
        gender=request.GET.get('searchbygender',None)
        bytype=request.GET.get('searchbytype',None)
        print(bytype)
        if bool(bytype):
            print("if")
            if gender is not None:
                return Response(MemberSerializer(Member.objects.filter(member_gender=gender).filter(active_fee_id__status=bytype).order_by('-id'),many=True).data)
            else:
                return Response(MemberSerializer(Member.objects.all().order_by('-id'),many=True).data)
        else:
            if gender is not None:
                return Response(MemberSerializer(Member.objects.filter(member_gender=gender).order_by('-id'),many=True).data)
            else:
                return Response(MemberSerializer(Member.objects.all().order_by('-id'),many=True).data)


    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def deleteBill(request):
    try:
        id=request.GET.get('id',None)
        member_id=Bill.objects.filter(id=id).values('member_id')[0]['member_id']
        print(member_id)
        if id is not None:
            Bill.objects.filter(id=id).delete()
            return Response(BillSerializer(Bill.objects.filter(member_id=member_id),many=True).data)
        else:
            return Response({"error":str("Please select bill id")})
    except Exception as e:
        return Response({"error":str(e)})