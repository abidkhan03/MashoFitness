from employees.models import EmployeeRecord
from .models import RentalData, rentalPayment


def null_check(value):
    if value=="":
        return None
    else:
        return value

def bill_status(data):
    if data=='on':
        return True
    else:
        return False


def addRental(request):
    try:

        add_rental = RentalData.objects.create(Full_name=request.POST.get('full-name'), contact_no=request.POST.get('contact-no'), 
                    cnic_no=null_check(request.POST.get('cnic-no')), reference=null_check(request.POST.get('reference')), 
                    shop_no=request.POST.get('shop-flat-no'), electric_bill=null_check(request.POST.get('electric-bill')),
                    gas_bill=null_check(request.POST.get('gas-bill')),payment_status=request.POST.get('payment-status'),
                    description=null_check(request.POST.get('description')),rent_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get('attended-by')).first())
        add_rental.save()

        payment= rentalPayment.objects.create(rent_amount=request.POST.get('rent-amount'), payment_mode=null_check(request.POST.get('payment-mode')),
                    rent_pay_date=request.POST.get('rent-pay-date'), rent_duration=request.POST.get('rent-duration'),
                    total_rent=request.POST.get('total-rent'), rent_end_date=request.POST.get('rent-end-date'),
                    rental_id=add_rental,rent_pay_by=request.POST.get('rent-pay-from'),
                    payment_gas_bill=True, payment_electric_bill=True,
                    rent_payment_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get('attended-by')).first())
        payment.save()
        add_rental.active_rent_id=payment
        add_rental.save()
        print("successfully added")
                    
    except Exception as e:
        print("Error In Add Rental: ", e)



def editRental(request):
    try:
        print(request.POST.get('rental-id'))
        RentalData.objects.filter(id=request.POST.get('rental-id')).update(Full_name=request.POST.get('full-name'), contact_no=request.POST.get('contact-no'), 
                    cnic_no=null_check(request.POST.get('cnic-no')), reference=null_check(request.POST.get('reference')), 
                    shop_no=request.POST.get('shop-flat-no'), electric_bill=null_check(request.POST.get('electric-bill')),
                    gas_bill=null_check(request.POST.get('gas-bill')),payment_status=request.POST.get('payment-status'),
                    description=null_check(request.POST.get('description')))

        rentalPayment.objects.filter(id=request.POST.get('active-fee-id')).update(rent_amount=request.POST.get('rent-amount'), payment_mode=null_check(request.POST.get('payment-mode')),
                    rent_pay_date=request.POST.get('rent-pay-date'), rent_duration=request.POST.get('rent-duration'),
                    rent_pay_by=request.POST.get('rent-pay-from'),
                    total_rent=request.POST.get('total-rent'), rent_end_date=request.POST.get('rent-end-date'),
                    )

    except Exception as e:
        print("Error In Update Rental: ", e)

def renew(request):
    try:
        payment=rentalPayment.objects.create(
            rent_amount=request.POST.get('renew-rent'),
            payment_mode='Cash',
            rent_pay_date=request.POST.get('renew-start-date'),
            rent_duration=request.POST.get('renew-duration'),
            rent_pay_by=request.POST.get('renew-pay-from'),
            total_rent=request.POST.get('renew-total'),
            rent_end_date=request.POST.get('renew-end-date'),
            payment_gas_bill=bill_status(request.POST.get("renew-gas-bill")),
            payment_electric_bill=bill_status(request.POST.get("renew-ele-bill")),
            rental_id=RentalData.objects.filter(id=request.POST.get('rent-id')).first(),
            rent_payment_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get('attended-by')).first()
            )
        payment.save()
        RentalData.objects.filter(id=request.POST.get('rent-id')).update(active_rent_id=payment.id,payment_status=request.POST.get('paymentstatus'))
    except Exception as e:
        print("Error In Renew Rental: ", e)