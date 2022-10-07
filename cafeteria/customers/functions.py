from .models import CafeteriaCustomer, CustomerPayment

def addCustomer(request):
    try:
        add_customer = CafeteriaCustomer.objects.create(customer_SerialNo=request.POST.get("customer-account"),
                        customer_name=request.POST.get("customer-name"),
                        customer_contact=request.POST.get("customer-contact"),
                        customer_email=request.POST.get("customer-email"),
                        customer_status=request.POST.get("customer-status"),
                        customer_address=request.POST.get("customer-address"),
                        customer_city=request.POST.get("customer-city"),
                        customer_country=request.POST.get("customer-country")
                        )
        add_customer.save()
    except Exception as e:
        print("Error in adding cafeteria customer data", e)


def updateCustomerData(request):
    try:
        CafeteriaCustomer.objects.filter(id=request.POST.get("update-id")).update(
                        customer_SerialNo=request.POST.get("customer-account"),
                        customer_name=request.POST.get("customer-name"),
                        customer_contact=request.POST.get("customer-contact"),
                        customer_email=request.POST.get("customer-email"),
                        customer_status=request.POST.get("customer-status"),
                        customer_address=request.POST.get("customer-address"),
                        customer_city=request.POST.get("customer-city"),
                        customer_country=request.POST.get("customer-country")
                        )
    except Exception as e:
        print("Error in updating customer data", e)
        return False

def PaymentDues(request):
    try:
        customer=CafeteriaCustomer.objects.get(id=request.POST.get('customer-id'))
        CustomerPayment.objects.create(payment_date=request.POST.get("payment-date"),
                                total_amount=request.POST.get("dues"),
                                payment_amount=request.POST.get("payment"),
                                remaining_amount=request.POST.get("remaining"),
                                customer_id=customer)
        customer.customer_dues = request.POST.get("remaining")
        customer.save()
        print("payment done")
    except Exception as e:
        print("Error in updating customer payment", e)
        return False