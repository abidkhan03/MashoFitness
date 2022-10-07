from .models import expensesData
from employees.models import EmployeeRecord
def addExpense(request):
        if request.POST.get('comment'):
            comment=request.POST.get('comment')
        else:
            comment=''
        add_data = expensesData.objects.create(
                date=request.POST.get('date'),
                account_head=request.POST.get('account-head'),
                paid_amount=request.POST.get('amount-paid'),
                payment_mode=request.POST.get('payment-mode'),
                expenses_for=request.POST.get('expense-for'),
                receipent_name=request.POST.get('receipent'),
                description=request.POST.get('description'),
                comments=comment,
                expense_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first()
                )

        add_data.save()

