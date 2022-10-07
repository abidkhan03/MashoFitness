
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import *
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TeamSerializer, MatchSerializer, BookingSerializer
from django.contrib import messages
from employees.models import EmployeeRecord
from django.db.models import Sum

def zeroValue(value):
    if value is None:
        return 0
    else:
        return value

def futsal(request):
    return render(request, 'futsal.html',
    {"TeamRecord":Team.objects.all().order_by("-id"),
    'futsal_total_team': Team.objects.all().count(),
    'futsal_new_team': Team.objects.filter(member_created_at__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).count(),
    'futsal_pending_game': Match.objects.filter(paid="Unpaid").count(),
    'futsal_today_sales': f"{zeroValue(Match.objects.filter(paid='Paid',date=datetime.today()).aggregate(Sum('fee'))['fee__sum']):,}",
    })

def addTeam(request):
    if request.method=="POST":
        if request.POST.get("add-team"):
            try:
                Team.objects.create(team_name=request.POST.get("team-name"),captain_name=request.POST.get("captain-name"),
                contact_number=request.POST.get("contact-number"),team_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first()).save()
                messages.success(request, 'Match Added Successful')
                return HttpResponseRedirect(reverse('addTeam'))
            except Exception as e:
                messages.error(request, 'Match Added Failed')
                return HttpResponseRedirect(reverse('addTeam'))
    else:
        # code here
        if request.POST.get("edit-team"):
            print(request.POST.get("edit-team"))
        return render(request,"addTeam.html",{"TeamRecord":Team.objects.all().order_by("-id") })


def viewTeam(request):
    return render(request, 'viewTeam.html',{"TeamRecord":Team.objects.all().order_by("-id")})

def teamDetails(request):
    if request.method=="POST":
        if request.POST.get("update-team"):
            Team.objects.filter(id=request.POST.get("id")).update(team_name=request.POST.get("team-name"),
                    captain_name=request.POST.get("captain-name"), contact_number=request.POST.get("contact"), 
                    team_attended_by=EmployeeRecord.objects.filter(user__username=request.POST.get("attended-by")).first())
            return render(request,"addTeam.html",{"TeamRecord":Team.objects.all().order_by("-id")})
    else:
        if request.GET.get("team-details"):
            team_id=request.GET.get("team-details")
            team_details=Team.objects.filter(id=team_id)[0]
            print(team_details.team_name)
            return render(request,"teamDetails.html",{"TeamRecord":team_details})


def futsalMatch(request):
    if request.method=="POST":
        if request.POST.get("add-match"):
            print("add book add book add book")
            
            if addMatchBooking(request):
                messages.success(request, 'Match Added Successful')
                return HttpResponseRedirect(reverse('matches'))
            else:
                messages.error(request, 'Match Added Failed')
                return HttpResponseRedirect(reverse('matches'))
            
    else:
        if request.GET.get("futsal-match"):
            return render(request,"futsalMatch.html", {"TeamRecord":Team.objects.all().filter(id=request.GET.get("futsal-match"))[0],
            "teamNames": Team.objects.all().exclude(id=request.GET.get("futsal-match")),
            'TeamRecords': Match.objects.all().order_by("-id")
            })
        
        return render(request, 'futsalMatch.html', {'TeamRecord': Match.objects.all(),
                    "user":EmployeeRecord.objects.filter(id=request.user.id).first()})

def matches(request):
    if request.method == "POST":
        pass
    else:
        if request.GET.get("match_done_row_id"):
            match_id=request.GET.get("match_done_row_id")
            Match.objects.filter(id=match_id).update(paid="Paid")
            return render(request, "matches.html", {'TeamRecord': Match.objects.all().order_by("-id")})
        if request.GET.get("match_edit_row_id"):
            match=Match.objects.filter(id=request.GET.get("match_edit_row_id"))[0]
            return render(request, "updateFutsalMatch.html", {'TeamRecord': match,
            "teamNames": Team.objects.all().exclude(team_name=match.team1.team_name)})
    
    return render(request, 'matches.html', {'TeamRecord': Match.objects.all().order_by("-id"),
                                "user":EmployeeRecord.objects.filter(id=request.user.id).first()})

def updateFutsalMatch(request):
    if request.method == "POST":
        if request.POST.get("update-detail"):
            print("edit edit edit edit **** ")
            update_match = updateMatchBooking(request)
            print(update_match)
            
    return render(request, 'matches.html', {'TeamRecord': Match.objects.all().order_by("-id"),
                        "user":EmployeeRecord.objects.filter(id=request.user.id).first()})


"""
apis work
"""

@api_view(["GET"])
def searchByTeamData(request):
    try:
        print(request.GET)
        resultperpage = request.GET.get("result-per-page", None)

        if resultperpage!="All":
            print("result per page is not equal to all")
            return Response(TeamSerializer(Team.objects.order_by('-id')[:int(resultperpage)],many=True).data)

        else:
            return Response(TeamSerializer(Team.objects.order_by('-id'),many=True).data)

    except Exception as e:
        return Response({"error": str(e)})


# api work
@api_view(['GET'])
def SearchByFutsalField(request):
    field=request.GET.get("field")
    value=request.GET.get("value")
    try:
        if field=="team_name":
            return Response(TeamSerializer(Team.objects.filter(team_name__icontains=value).order_by('-id'),many=True).data)
        elif field=="captain_name":
            return Response(TeamSerializer(Team.objects.filter(captain_name__icontains=value).order_by('-id'),many=True).data)
        elif field=="contact_number":
            return Response(TeamSerializer(Team.objects.filter(contact_number__icontains=value).order_by('-id'),many=True).data)
    except:
        return Response({"message":"No data found"})

@api_view(['GET'])
def deleteTeamRecord(request):
    # print(request.DELETE.get('delete_array'))
    try:
        delete_list=request.GET.getlist('arr[]')
        print(delete_list)
        if delete_list is not None:
            for i in delete_list:
                print(i)
                Team.objects.filter(id=int(i)).delete()
            return Response(TeamSerializer(Team.objects.all().order_by("-id"),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})

@api_view(['GET'])
def getBookings(request):
    date=request.GET.get('booking_date')
    print(date)
    try:
        return Response(BookingSerializer(createDailyMatchTimeTable(date),many=True).data)
    except Exception as e:
        return Response({"error":str(e)})

# Match page api
@api_view(['GET'])
def deleteTeamMatch(request):
    # print(request.DELETE.get('delete_array'))
    try:
        delete_list=request.GET.getlist('arr[]')
        if delete_list is not None:
            for i in delete_list:
                match_id=Match.objects.filter(id=int(i))[0]
                Booking.objects.filter(id=match_id.booking_time.id).update(status=False)
                Match.objects.filter(id=int(i)).delete()
            return Response(MatchSerializer(Match.objects.all().order_by('-id'),many=True).data)
        else:
            return Response({"error":str("No data selected")})
    except Exception as e:
        print(e)
        return Response({"error":str(e)})


@api_view(['GET'])
def SearchByTeamMatchField(request):
    print(request.GET)
    field=request.GET.get("field")
    value=request.GET.get("value")
    print(value,field)
    try:
        if field=="team_name":
            return Response(MatchSerializer(Match.objects.filter(team1__team_name__icontains=value).select_related("team1"),many=True).data)
        elif field=="contact_number":
            return Response(MatchSerializer(Match.objects.filter(team1__contact_number__icontains=value).order_by('-id'),many=True).data)
    except:
        return Response({"message":"No data found"})

@api_view(['GET'])
def SearchByTeamMatchStatus(request):
    value=request.GET.get("status")
    try:
        return Response(MatchSerializer(Match.objects.filter(paid=value),many=True).data)
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def SearchByFutsalDate(request):
    date=request.GET.get('date')
    print(date)
    try:
        return Response(BookingSerializer(createDailyMatchTimeTable(date),many=True).data)
    except Exception as e:
        return Response({"error":str(e)})

@api_view(['GET'])
def searchByFutsalDate(request):
    try:
        print(request.GET)
        date = request.GET.get("date", None)
        return Response(MatchSerializer(Match.objects.filter(date=date).select_related("team1"),many=True).data)

    except Exception as e:
        return Response({"error": str(e)})