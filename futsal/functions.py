from .models import Match, Booking, Team
from employees.models import EmployeeRecord

def createDailyMatchTimeTable(date):
    
    if Booking.objects.filter(booking_date=date).exists():
        print("booking date already exist:",date)
        return Booking.objects.filter(booking_date=date)
    else:
        print("booking date not exist: craate new booking",date)
        Booking.objects.create(booking_date=date,time="12:00 to 1:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="1:00 to 2:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="2:00 to 3:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="3:00 to 4:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="4:00 to 5:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="5:00 to 6:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="6:00 to 7:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="7:00 to 8:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="8:00 to 9:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="9:00 to 10:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="10:00 to 11:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="11:00 to 12:00",meridiem="PM",status=False)
        Booking.objects.create(booking_date=date,time="12:00 to 1:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="1:00 to 2:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="2:00 to 3:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="3:00 to 4:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="4:00 to 5:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="5:00 to 6:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="6:00 to 7:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="7:00 to 8:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="8:00 to 9:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="9:00 to 10:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="10:00 to 11:00",meridiem="AM",status=False)
        Booking.objects.create(booking_date=date,time="11:00 to 12:00",meridiem="AM",status=False)

        return Booking.objects.filter(booking_date=date)

def addMatchBooking(request):
    try:
        team1=Team.objects.filter(team_name=request.POST.get('team_name1'))[0]
        team2=Team.objects.filter(team_name=request.POST.get('team_name2'))[0]
        booking_time=Booking.objects.filter(time=request.POST.get('book_at')[:-2],
                                            meridiem=request.POST.get('book_at')[-2:],
                                            booking_date=request.POST.get("booking_date"))[0]
        booking_time.status=True
        booking_time.save()
        date=request.POST.get('date')
        fee=request.POST.get('fee')
        payment_status=request.POST.get('payment_status')
        match_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first()

        Match.objects.create(team1=team1,team2=team2,booking_time=booking_time,
        paid=payment_status,fee=fee,date=date, match_attended_by=match_attended_by)
        return True
    except Exception as e:
        print("error in addMatchBooking",e)
        return False

def updateMatchBooking(request):
    try:
        match_id=Match.objects.filter(id=request.POST.get("id"))[0]
        Booking.objects.filter(id=match_id.booking_time.id).update(status=False)
        # team1=Team.objects.filter(team_name=request.POST.get('team_name1'))[0]
        team2=Team.objects.filter(team_name=request.POST.get('team_name2'))[0]
        booking_time=Booking.objects.filter(time=request.POST.get('book_at')[:-2],
                                            meridiem=request.POST.get('book_at')[-2:],
                                            booking_date=request.POST.get("booking_date"))[0]
        booking_time.status=True
        booking_time.save()
        date=request.POST.get('date')
        fee=request.POST.get('fee')
        payment_status=request.POST.get('payment_status')
        match_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first()
        print(team2, booking_time, date, fee,payment_status,match_attended_by)

        Match.objects.filter(id=request.POST.get("id")).update(team2=team2,booking_time=booking_time,
        paid=payment_status,fee=fee,date=date, match_attended_by=match_attended_by)
        return True
    except Exception as e:
        print("error in addMatchBooking",e)
        return False
