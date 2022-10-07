from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Userlogin, name='login'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('employee/', views.employee, name='employee'),
    path('logout/', views.logout_user, name='logout'),
    path('editEmployee/',views.editEmployee,name='editEmployee'),
]