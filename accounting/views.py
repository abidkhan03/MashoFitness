from django.shortcuts import render
from expenses.models import expensesData
from django.db.models import Sum
from theme.models import Bill
from futsal.models import Match
from snooker.models import snookerTableIncome
from rental.models import rentalPayment
import datetime
from cafeteria.sales.models import Sales


def checkNone(data):
    if data == None:
        return 0
    else:
        return data


def reports(request):
    revenue = checkNone(Sales.objects.filter(order_id__order_date__month=datetime.datetime.now().month).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum']) + checkNone(Bill.objects.aggregate(Sum('paid'))[
        'paid__sum']) + checkNone(Match.objects.aggregate(Sum('paid'))['paid__sum']) + checkNone(snookerTableIncome.objects.aggregate(Sum('amount'))['amount__sum']) + checkNone(rentalPayment.objects.aggregate(Sum('total_rent'))['total_rent__sum'])
    expense = checkNone(expensesData.objects.aggregate(
        Sum('paid_amount'))['paid_amount__sum'])
    return render(request, "reports.html", {
        # Expenses
        'gym_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Gym').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'futsal_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Futsal').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'snooker_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Snooker').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'cafeteria_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'rental_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Rental').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'cafeteria_expense': f"{checkNone(expensesData.objects.filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
        'total_expenses': f"{expense:,}",

        # Revenues
        'gym_revenue': f"{checkNone(Bill.objects.aggregate(Sum('paid'))['paid__sum']):,}",
        'futsal_revenue': f"{checkNone(Match.objects.aggregate(Sum('fee'))['fee__sum']):,}",
        'snooker_revenue': f"{checkNone(snookerTableIncome.objects.aggregate(Sum('amount'))['amount__sum']):,}",
        'rental_revenue': f"{checkNone(rentalPayment.objects.aggregate(Sum('total_rent'))['total_rent__sum']):,}",
        'cafeteria_revenue': f"{checkNone(Sales.objects.filter(order_id__order_date__month=datetime.datetime.now().month).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum']) :,}",
        'total_revenue': f"{revenue:,}",
        "profit": f"{revenue-expense:,}",
    })


def revenue(request):
    if request.method == "POST":
        if request.POST.get("revenue-generate"):
            from_date = request.POST.get("from-date")
            to_date = request.POST.get("to-date")
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            print(from_date, to_date)
            if request.POST.get("check"):
                value = request.POST.get("check")
                if value == "all-check":
                    print("all check")
                    return render(request, "revenue.html", {
                        'MemberData': Bill.objects.filter(bill_created_at__range=[from_date, to_date]).select_related('member_id').select_related('fee_id'),
                        "gym_revenue_total": f"{checkNone(Bill.objects.filter(bill_created_at__range=[from_date,to_date]).aggregate(Sum('paid'))['paid__sum']):,}",
                        "futsal_revenue_total": f"{checkNone(Match.objects.filter(date__range=[from_date,to_date]).aggregate(Sum('fee'))['fee__sum']):,}",
                        "FutsalData": Match.objects.filter(date__range=[from_date, to_date]).select_related('booking_time').select_related('team1').select_related('team2'),
                        "snooker_revenue_total": f"{checkNone(snookerTableIncome.objects.filter(snooker_id__date__range=[from_date,to_date]).select_related('snooker_id').aggregate(Sum('amount'))['amount__sum']):,}",
                        "SnookerData": snookerTableIncome.objects.filter(snooker_id__date__range=[from_date, to_date]).select_related("snooker_id"),
                        'rentalData': rentalPayment.objects.filter(rent_pay_date__range=[from_date, to_date]).select_related('rental_id'),
                        'rental_revenue': f"{checkNone(rentalPayment.objects.filter(rent_pay_date__range=[from_date,to_date]).aggregate(Sum('total_rent'))['total_rent__sum']):,}",
                        "cafeteriaData": Sales.objects.filter(order_id__order_date__range=[from_date, to_date]).select_related("order_id"),
                        'cafeteria_revenue': f"{checkNone(Sales.objects.filter(order_id__order_date__range=[from_date,to_date]).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum']):,}",
                        "All_total": f"{checkNone(Sales.objects.filter(order_id__order_date__range=[from_date,to_date]).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum'])+ checkNone(snookerTableIncome.objects.filter(snooker_id__date__range=[from_date,to_date]).select_related('snooker_id').aggregate(Sum('amount'))['amount__sum'])+ checkNone(Bill.objects.filter(bill_created_at__range=[from_date,to_date]).aggregate(Sum('paid'))['paid__sum'])+ checkNone(Match.objects.filter(date__range=[from_date,to_date]).aggregate(Sum('fee'))['fee__sum']):,}",
                        'from_date': from_date,
                        'to_date': to_date,

                    })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "gym-check":
                    print("gym check")
                    return render(request, "revenue.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      'MemberData': Bill.objects.filter(bill_created_at__range=[from_date, to_date]).select_related('member_id').select_related('fee_id'),
                                      "gym_revenue_total": f"{checkNone(Bill.objects.filter(bill_created_at__range=[from_date,to_date]).aggregate(Sum('paid'))['paid__sum']):,}",
                                  })
                elif value == "futsal-check":
                    print("futsal check")
                    return render(request, "revenue.html", {
                        'from_date': from_date,
                        'to_date': to_date,
                        "futsal_revenue_total": f"{checkNone(Match.objects.filter(date__range=[from_date,to_date]).aggregate(Sum('fee'))['fee__sum']):,}",
                        "FutsalData": Match.objects.filter(date__range=[from_date, to_date]).select_related('booking_time').select_related('team1').select_related('team2'),

                    })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "snooker-check":
                    print("snooker check")

                    return render(request, "revenue.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      "snooker_revenue_total": f"{checkNone(snookerTableIncome.objects.filter(snooker_id__date__range=[from_date,to_date]).select_related('snooker_id').aggregate(Sum('amount'))['amount__sum']):,}",
                                      "SnookerData": snookerTableIncome.objects.filter(snooker_id__date__range=[from_date, to_date]).select_related("snooker_id"),
                                  })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "cafeteria-check":
                    print("cafeteria check")
                    return render(request, "revenue.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      "cafeteriaData": Sales.objects.filter(order_id__order_date__range=[from_date, to_date]).select_related("order_id"),
                                      "cafeteria_revenue_total": f"{checkNone(Sales.objects.filter(order_id__order_date__range=[from_date,to_date]).aggregate(Sum('order_id__order_total_price'))['order_id__order_total_price__sum']):,}",
                                  })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "rental-check":
                    print("rental check")
                    return render(request, "revenue.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      'rentalData': rentalPayment.objects.filter(rent_pay_date__range=[from_date, to_date]).select_related('rental_id'),
                                      'rental_revenue': f"{checkNone(rentalPayment.objects.filter(rent_pay_date__range=[from_date,to_date]).aggregate(Sum('total_rent'))['total_rent__sum']):,}"
                                  })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
            else:
                print("no check")
                return render(request, "revenue.html")
    return render(request, "revenue.html")


def expensesReport(request):
    if request.method == "POST":
        if request.POST.get("revenue-generate"):
            from_date = request.POST.get("from-date")
            to_date = request.POST.get("to-date")
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
            if request.POST.get("check"):
                value = request.POST.get("check")
                if value == "all-check":
                    print("all check")
                    return render(request, "expensesReport.html", {
                        "snooker_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Snooker').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        "SnookerData": expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Snooker'),
                        "futsal_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Futsal').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        "FutsalData": expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Futsal'),
                        'MemberData': expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Gym'),
                        "gym_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Gym').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        "rental_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Rental').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        'rentalData': expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Rental'),
                        'cafeteriaData': expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Cafeteria'),
                        'cafeteria_expense_total': f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        "All_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        'from_date': from_date,
                        'to_date': to_date,
                    })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "gym-check":
                    print("gym check")
                    return render(request, "expensesReport.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      'MemberData': expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Gym'),
                                      "gym_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Gym').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                                  })
                elif value == "futsal-check":
                    print("futsal check")
                    return render(request, "expensesReport.html", {
                        "futsal_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Futsal').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                        "FutsalData": expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Futsal'),
                        'from_date': from_date,
                        'to_date': to_date,
                    })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "snooker-check":
                    print("snooker check")
                    return render(request, "expensesReport.html",
                                  {
                                      'from_date': from_date,
                                      'to_date': to_date,
                                      "snooker_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Snooker').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                                      "SnookerData": expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Snooker'),
                                  })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "cafeteria-check":
                    return render(request, "expensesReport.html",
                                    {
                                        'from_date': from_date,
                                        'to_date': to_date,
                                        "cafeteria_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Cafeteria').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                                        "cafeteriaData": expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Cafeteria'),
                                    })
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
                elif value == "rental-check":
                    print("rental check")
                    return render(request, "expensesReport.html",
                                  {"rental_expense_total": f"{checkNone(expensesData.objects.filter(date__range=[from_date,to_date]).filter(expenses_for='Rental').aggregate(Sum('paid_amount'))['paid_amount__sum']):,}",
                                   'rentalData': expensesData.objects.filter(date__range=[from_date, to_date]).filter(expenses_for='Rental'),
                                   'from_date': from_date,
                                   'to_date': to_date})
                    # return render(request, "revenue.html", {'revenueData':RentalData.objects.filter(rent_date__range=[from_date,to_date])})
            else:
                print("no check")
                return render(request, "expensesReport.html")
    # return render(request, "revenue.html")
    return render(request, "expensesReport.html")
