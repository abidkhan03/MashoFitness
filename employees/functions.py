import email
from .models import EmployeeRecord,EmployeeSalary
# from theme.functions import NoneValue
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import sys, os

def NoneValue(value):
    if value=="":
        return None
    else:
        return value


def CreateAdminUserFirst():
    try:
        if EmployeeRecord.objects.filter(user__is_superuser=True).exists():
            print("admin exists")
            return False
        else:
            print("super user not exists")
            user=User.objects.create(first_name='admin',username="admin",password=make_password('admin'),is_superuser=True,email="")
            EmployeeRecord.objects.create(
                employee_contact="1234567890",
                employee_image="default.png",
                employee_cnic=None,
                employee_address=None,
                employee_gender="Male",
                employee_dob=None,
                employee_age=None,
                employee_blood_group="",
                employee_type="Active",
                employee_pay=0,
                user=user,
            ).save()
            return True
    except Exception as e:
        print("Admin error ", e)
def addEmployee(request):
    try:
        if request.FILES:
            f=request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        else:
            filename="default.png"
        if request.POST.get("emp-email"):
            emails=request.POST.get("emp-email")
        else:
            emails=""
        user = User.objects.create(first_name=request.POST.get("emp-name"),username=request.POST.get("emp-username"),password=make_password(request.POST.get("emp-password")),email=emails,is_superuser=False)
        employee_data = EmployeeRecord.objects.create(
                    employee_contact=request.POST.get('emp-contact'),
                    employee_image=filename,
                    employee_cnic=NoneValue(request.POST.get('emp-cnic')),
                    # employee_email=NoneValue(request.POST.get('emp-email')),
                    employee_address=NoneValue(request.POST.get('emp-address')),
                    employee_gender=request.POST.get('emp-gender'),
                    employee_dob=NoneValue(request.POST.get('dateofbirth')),
                    employee_age=NoneValue(request.POST.get('emp-age')),
                    employee_blood_group=NoneValue(request.POST.get('emp-blood-group')),
                    employee_type=request.POST.get('emp-type'),
                    # employee_username=NoneValue(request.POST.get('emp-username')),
                    # employee_password=NoneValue(request.POST.get('emp-password')),
                    employee_pay= request.POST.get('emp-pay'),
                    employee_status=request.POST.get('emp-status'),
                    user=user)

        employee_data.save()

        return employee_data
    except Exception as e:
        print("Employee error ", e)
        return False


def updateEmployee(request):
    try:
        if request.FILES:
            f=request.FILES["photos"]
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            uploaded_file_url = fs.url(filename)
        else:
            filename="default.png"
        if request.POST.get("emp-email"):
            emails=request.POST.get("emp-email")
        else:
            emails=""
        if request.POST.get("emp-password")=="****":
            User.objects.filter(id=request.POST.get("emp-id")).update(first_name=request.POST.get("emp-name"),username=request.POST.get("emp-username"),email=emails)
        else:
            User.objects.filter(id=request.POST.get("emp-id")).update(first_name=request.POST.get("emp-name"),username=request.POST.get("emp-username"),password=make_password(request.POST.get("emp-password")),email=emails)
        EmployeeRecord.objects.filter(id=request.POST.get('emp-id')).update(
                    employee_contact=request.POST.get('emp-contact'),
                    employee_image=filename,
                    employee_cnic=NoneValue(request.POST.get('emp-cnic')),
                    # employee_email=NoneValue(request.POST.get('emp-email')),
                    employee_address=NoneValue(request.POST.get('emp-address')),
                    employee_gender=request.POST.get('emp-gender'),
                    employee_dob=NoneValue(request.POST.get('dateofbirth')),
                    employee_age=NoneValue(request.POST.get('emp-age')),
                    employee_blood_group=NoneValue(request.POST.get('emp-blood-group')),
                    employee_type=request.POST.get('emp-type'),
                    # employee_username=NoneValue(request.POST.get('emp-username')),
                    # employee_password=NoneValue(request.POST.get('emp-password')),
                    employee_pay= request.POST.get('emp-pay'),
                    employee_status=request.POST.get('emp-status'))
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("Employee update error ", e)
        return False

def renewSalary(request):
    try:
        emp=EmployeeRecord.objects.filter(id=request.POST.get("emp-id")).first()
        EmployeeSalary.objects.create(
            employee_salary=emp,
            salary_amount=request.POST.get("total-salary"),
            salary_date=request.POST.get("pay-date"),
            salary_attended_by=request.POST.get("pay-by"),)
        return True
    except Exception as e:
        print("Employee salary error ", e)
        return False