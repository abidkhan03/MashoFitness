from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path('rental/', views.rental, name="rental"),
    path('updateRental/', views.updateRental, name="updateRental"),


    # api paths
    path('api/deleteRentalRecord/', views.deleteRentalRecord, name='deleteRentalRecord'),
    path('api/SearchByRentalField/', views.SearchByRentalField, name='SearchByRentalField'),
    path('api/searchByRentalDate/', views.searchByRentalDate, name='searchByRentalDate'),
]

