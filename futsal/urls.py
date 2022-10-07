from django.urls import path
from . import views
from employees.views import index


urlpatterns = [
    path("index/",index,name="index"),
    path("viewTeam/", views.viewTeam, name="viewTeam"),
    path("matches/", views.matches, name="matches"),
    path("updateFutsalMatch/", views.updateFutsalMatch, name="updateFutsalMatch"),
    path("teamDetails/", views.teamDetails, name="teamDetails"),path("futsal", views.futsal, name="futsal"),
    path("futsalMatch/", views.futsalMatch, name="futsalMatch"),
    path('addTeam/', views.addTeam, name='addTeam'),



    # # api paths
    path('api/SearchByFutsalField/',views.SearchByFutsalField,name='SearchByFutsalField'),
    path("api/deleteTeamRecord/", views.deleteTeamRecord, name="deleteTeamRecord"),
    path("api/getBookings/", views.getBookings, name="getBookings"),
    path("api/SearchByFutsalDate/", views.SearchByFutsalDate, name="SearchByFutsalDate"),

    # Match page api
    path("api/deleteTeamMatch/", views.deleteTeamMatch, name="deleteTeamMatch"),
    path("api/SearchByTeamMatchField/", views.SearchByTeamMatchField, name="SearchByTeamMatchField"),
    path("api/SearchByTeamMatchStatus/", views.SearchByTeamMatchStatus, name="SearchByTeamMatchStatus"),
    path("api/searchByFutsalDate/", views.searchByFutsalDate, name="searchByFutsalDate"),

]