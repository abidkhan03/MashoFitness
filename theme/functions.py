import datetime as dt
from theme.gym_scheduler.smsGymScheduler import sendMessageToUser
from .models import MembershipCategory, Member,Payment,Fee,Bill,BodyAssesments
from django.core.files.storage import FileSystemStorage
from employees.models import EmployeeRecord


def fetchUniqueCategoryName(model):
    try:
        obj = model.objects.all()
        ls = []
        for i in obj:
            ls.append(i.category_name)
        return set(ls)
        # return obj
    except model.DoesNotExist:
        return None

def NoneValue(value):
    if value=="":
        return None
    else:
        return value

def checkMemberStarus():
    try:
        if Member.objects.all().exists():
            for i in Member.objects.all():
                if (i.member_membership_expiry_date-dt.date.today()).days<0:
                    id=Member.objects.filter(id=i.id)[0].active_fee_id.id
                    Fee.objects.filter(id=id).update(status="Expired")
    except:
        print("checkMemberStarus")

def addMemberRecord(request,status):
        print("atted by ****** ", request.POST.get("attended-by"))
        print(request.POST.get("membership-start-date"))
        if request.FILES:
            f=request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        else:
            filename="default.png"
        membership_id = MembershipCategory.objects.filter(
                        category_name=request.POST.get("membershipcategory")).filter(
                        category_class=request.POST.get("membership-class")).filter(
                        category_gender=request.POST.get("gender")
                        )[0]
        print(membership_id)
        member_data =Member.objects.create(member_name=request.POST.get("fullname"),
                        member_father_name=request.POST.get("fathername"),
                        member_cnic=NoneValue(request.POST.get("cnicnumber")),
                        member_contact=request.POST.get("contactnumber"),
                        member_emergency_contact=NoneValue(request.POST.get("alternatenumber")),
                        member_email=NoneValue(request.POST.get("email")),
                        member_occupation=NoneValue(request.POST.get("occupation")),
                        member_address=NoneValue(request.POST.get("address")),
                        member_gender=request.POST.get("gender"),
                        member_dob=NoneValue(request.POST.get("dateofbirth")),
                        member_age=NoneValue(request.POST.get("age")),
                        member_blood_group=NoneValue(request.POST.get("bloodgroup")),
                        member_height=NoneValue(request.POST.get("height")),
                        member_weight=NoneValue(request.POST.get("weight")),
                        member_card_id=request.POST.get("cardnumber"),
                        member_target=NoneValue(request.POST.get("target")),
                        member_serial_no=request.POST.get("serial-no"),
                        member_image=filename,
                        member_membership_id=membership_id,
                        member_membership_expiry_date=request.POST.get("membership-expire"),
                        member_membership_start_date=request.POST.get("membership-start-date"),
                        attended_by=EmployeeRecord.objects.filter(id=request.user.id).first(),
                        )
        member_data.save()
        print("member data",member_data)
        if status: # for payment
            fee=Fee.objects.create(total=membership_id.category_fee,
                        discount=request.POST.get("discount"),
                        payable=request.POST.get("payableamount"),
                        remaining=0,
                        status=request.POST.get("paymentstatus"),
                        installment=False,
                        member_id=member_data
                        )
            fee.save()
            Payment.objects.create(
                            payment_amount=request.POST.get("payableamount"),
                            fee_id=fee
                            ).save()
            Member.objects.filter(id=member_data.id).update(
                        active_fee_id=fee
                        )
            add_bill_record(subscription=membership_id,
                        start_date=member_data.member_membership_start_date,
                        end_date=request.POST.get("membership-expire"),
                        amount=membership_id.category_fee,
                        discount=request.POST.get("discount"),
                        payable=request.POST.get("payableamount"),
                        remaining=0,
                        paid=request.POST.get("payableamount"),
                        member=member_data,
                        fee=fee,
                        user_id=request.user.id
                        )
            
        else: # for installment
            fee=Fee.objects.create(total=membership_id.category_fee,
                        discount=request.POST.get("discount"),
                        payable=request.POST.get("payableamount"),
                        remaining=request.POST.get("remainingamount"),
                        status=request.POST.get("paymentstatus"),
                        installment=True,
                        member_id=member_data
                        )
            fee.save()
            
            Payment.objects.create(
                            payment_amount=request.POST.get("paidamount"),
                            fee_id=fee
                            ).save()
            Member.objects.filter(id=member_data.id).update(
                            active_fee_id=fee
                            )
            add_bill_record(subscription=membership_id,
                            start_date=member_data.member_membership_start_date,
                            end_date=request.POST.get("membership-expire"),
                            amount=membership_id.category_fee,
                            discount=request.POST.get("discount"),
                            payable=request.POST.get("payableamount"),
                            remaining=request.POST.get("remainingamount"),
                            paid=request.POST.get("paidamount"),
                            member=member_data,
                            fee=fee,
                            user_id=request.user.id
                            )
        sendMessageToUser(request.POST.get("fullname"),request.POST.get("contactnumber"),f"Welcome to the Masho Fitness Club. Your membership category is {request.POST.get('membershipcategory')} and memership class is {request.POST.get('membership-class')}. your membership expire date is {request.POST.get('membership-expire')}")
    

def update_payment_installment(request):
    try:
        member=Member.objects.filter(id=request.POST.get("cid"))[0]
        if int(request.POST.get("istallment-new-pending-amount"))<=0:
            Fee.objects.filter(id=member.active_fee_id.id).update(
                        remaining=request.POST.get("istallment-new-pending-amount"),
                        status="Paid"
                        )
        else:
            Fee.objects.filter(id=member.active_fee_id.id).update(
                        remaining=request.POST.get("istallment-new-pending-amount"),
                        status="Unpaid"
                        )
        Payment.objects.create(
                            payment_amount=request.POST.get("installment-pay-amount"),
                            fee_id=Fee.objects.filter(id=member.active_fee_id.id)[0]
                            ).save()
        add_bill_record(subscription=MembershipCategory.objects.filter(id=member.member_membership_id.id)[0],
                        start_date=member.member_membership_start_date,
                        end_date=member.member_membership_expiry_date,
                        amount=Fee.objects.filter(id=member.active_fee_id.id)[0].total,
                        discount=Fee.objects.filter(id=member.active_fee_id.id)[0].discount,
                        payable=Fee.objects.filter(id=member.active_fee_id.id)[0].payable,
                        remaining=request.POST.get("istallment-new-pending-amount"),
                        paid=request.POST.get("installment-pay-amount"),
                        member=member,
                        fee=Fee.objects.filter(id=member.active_fee_id.id)[0],
                        user_id=request.user.id
                        )
        
        return True
    except Exception as e:
        print('update_payment_installmente',e)
        return False

def add_bill_record(subscription,
                    start_date,
                    end_date,
                    amount,
                    discount,
                    payable,
                    remaining,
                    paid,member,fee,user_id):
    try:
        Bill.objects.create(
                        subscription_id=subscription,
                        start_date=start_date,
                        end_date=end_date,
                        amount=amount,
                        discount=discount,
                        payable=payable,
                        remaining=remaining,
                        paid=paid,
                        member_id=member,
                        fee_id=fee,
                        bill_attended_by=EmployeeRecord.objects.filter(id=user_id).first()
                        ).save()
        return True

    except Exception as e:
        print('add_bill_record',e)
        return False




def renewSubscription(request,status):
    print(status)
    try:
        membership_id = MembershipCategory.objects.filter(
                        category_name=request.POST.get("model-membershipcategory")).filter(
                        category_class=request.POST.get("model-membership-class")).filter(
                        category_gender=request.POST.get("rew-model-gender")
                        )[0]
        print(membership_id)
        member_data =Member.objects.filter(id=request.POST.get("cid"))[0]
        print("member data",member_data)
        if status: # for payment
            fee=Fee.objects.create(total=membership_id.category_fee,
                        discount=request.POST.get("model-discount"),
                        payable=request.POST.get("model-payableamount"),
                        remaining=0,
                        status="Paid",
                        installment=False,
                        member_id=member_data
                        )
            fee.save()
            Payment.objects.create(
                            payment_amount=request.POST.get("model-payableamount"),
                            fee_id=fee
                            ).save()
            Member.objects.filter(id=member_data.id).update(
                        member_membership_start_date=request.POST.get("model-start-date"),
                        member_membership_expiry_date=request.POST.get("model-membership-expire"),
                        active_fee_id=fee,
                        member_membership_id=membership_id
                        )
        
            add_bill_record(subscription=membership_id,
                        start_date=request.POST.get("model-start-date"),
                        end_date=request.POST.get("model-membership-expire"),
                        amount=membership_id.category_fee,
                        discount=request.POST.get("model-discount"),
                        payable=request.POST.get("model-payableamount"),
                        remaining=0,
                        paid=request.POST.get("model-payableamount"),
                        member=member_data,
                        fee=fee,
                        user_id=request.user.id
                        )
            
        else: # for installment
            fee=Fee.objects.create(total=membership_id.category_fee,
                        discount=request.POST.get("model-discount"),
                        payable=request.POST.get("model-payableamount"),
                        remaining=request.POST.get("remainingamount"),
                        status="Unpaid",
                        installment=True,
                        member_id=member_data
                        )
            fee.save()
            
            Payment.objects.create(
                            payment_amount=request.POST.get("paidamount"),
                            fee_id=fee
                            ).save()
            Member.objects.filter(id=member_data.id).update(
                            member_membership_start_date=request.POST.get("model-start-date"),
                            member_membership_expiry_date=request.POST.get("model-membership-expire"),
                            active_fee_id=fee,
                            member_membership_id=membership_id
                            )
            
            add_bill_record(subscription=membership_id,
                            start_date=request.POST.get("model-start-date"),
                            end_date=request.POST.get("model-membership-expire"),
                            amount=membership_id.category_fee,
                            discount=request.POST.get("model-discount"),
                            payable=request.POST.get("model-payableamount"),
                            remaining=request.POST.get("remainingamount"),
                            paid=request.POST.get("paidamount"),
                            member=member_data,
                            fee=fee,
                            user_id=request.user.id
                            )
        sendMessageToUser(member_data.member_name,member_data.member_contact,f"Your membership successfully renewed. Your membership category is {membership_id.category_name} and memership class is {membership_id.category_class}. your membership expire date is {request.POST.get('model-membership-expire')}")

    except Exception as e:
        print("re new subscription ",e)

def addBodyAssesment(request):
    try:
        Member.objects.filter(id=request.POST.get("member_id")).update(
            member_height=NoneValue(request.POST.get("height")),
            member_weight=NoneValue(request.POST.get("weight")),
        )
        BodyAssesments.objects.create(
            height=request.POST.get("height"),
            weight=request.POST.get("weight"),
            neck=request.POST.get("neck"),
                            shoulder=request.POST.get("shoulder"), chest_extended=request.POST.get("chest-extended"),
                            chest_normal=request.POST.get("chest-normal"), forearms=request.POST.get("forearms"),
                            biceps=request.POST.get("biceps"), wrist=request.POST.get("wrist"),
                            upper_abs=request.POST.get("upper-abs"), lower_abs=request.POST.get("lower-abs"),
                            waist=request.POST.get("waist"), hip=request.POST.get("hip"),
                            thigh=request.POST.get("thigh"), calves=request.POST.get("calves"),
                            ankles=request.POST.get("ankles"), body_fat=request.POST.get("body-fat"),
                            vascular=request.POST.get("vascular"), medical_issue=request.POST.get("medical-issue"),
                            body_target=request.POST.get("body-target"), assesment_date=request.POST.get("assesment-date"),
                            member_id=Member.objects.filter(id=request.POST.get("member_id"))[0]).save()
    
    except Exception as e:
        print("add_body_assesment",e)