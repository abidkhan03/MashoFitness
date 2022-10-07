from django.urls import path
from employees.views import index
from . import views
urlpatterns = [
    path('index/', index, name='index'),
    path("smshistory/", views.smshistory, name="smshistory"),

    path("api/smsForsearch/", views.smsForsearch, name="smsForsearch"),
    path("api/searchMessage/", views.searchMessage, name="searchMessage"),
]
