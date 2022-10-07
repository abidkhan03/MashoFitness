from django.urls import path
from . import views
from employees.views import index


urlpatterns = [
    path("index/",index,name="index"),
    path('snooker/', views.snooker, name='snooker'),
    path('updateSnooker/', views.updateSnooker, name='updateSnooker'),
    path('editSnooker/', views.editSnooker, name='editSnooker'),


    # api paths
    path('api/deleteSnookerRecord/',views.deleteSnookerRecord, name='deleteSnookerRecord'),
    path('api/searchBySnookerDate/',views.searchBySnookerDate, name='searchBySnookerDate'),
    path('api/SearchBySnookerData/',views.SearchBySnookerData, name='SearchBySnookerData'),
    
]