from django.urls import path
from . import views
from employees.views import index

urlpatterns = [
    path('index/', index, name='index'),
    path('addMember/', views.addMember, name='addMember'),
    path("bodyAssesments/", views.bodyAssesments, name="bodyAssesments"),
    path("gymManagement", views.gymManagement, name="gymManagement"),
    path("GymSetting/gymSetting/", views.gymSetting, name="gymSetting"),
    path("GymSetting/editGymSetting/", views.editGymSetting, name="editGymSetting"),
    path("memberDetails/", views.memberDetails, name="memberDetails"),
    path("printform/", views.printform, name="printform"),
    path("viewMembers/", views.viewMembers, name="viewMembers"),
    path("viewRecord/", views.viewRecord, name="viewRecord"),

    # """
    # API path for the ajex call
    # """
    path("api/get_membershipCategory/", views.get_membershipCategory, name="api_get_membershipCategory"),
    path("api/deleteMember/", views.deleteMember, name="deleteMember"),
    path("api/searchbydata/", views.searchbydata, name="searchbydata"),
    path("api/searchbydate/", views.searchbydate, name="searchbydate"),
    path("api/searchbyname/", views.searchbyname, name="searchbyname"),
    path("api/testing/", views.testing, name="testing"),
    path("api/searchBillDate/", views.searchBillDate, name="searchBillDate"),
    path("api/ViewBillCall/", views.ViewBillCall, name="ViewBillCall"),
    path("api/getExpireRemainingDays/", views.getExpireRemainingDays, name="getExpireRemainingDays"),
    path("api/searchbygender/", views.searchbygender, name="searchbygender"),
    path("api/checkSerialNo/", views.checkSerialNo, name="checkSerialNo"),
    path("api/deleteBill/", views.deleteBill, name="deleteBill"),
    # ex: /polls/
    # path('', views.home, name='home'),
    # path('login', views.login, name='login'),
    # path('signup', views.signup, name='signup'),
    # path('order', views.order, name='order'),
    # path("logout", views.logout, name= "logout"),
    # path('order_details',views.order_details, name='order_details'),
    # path('user_details',views.user_details, name='user_details'),
    # path('admin:index/', admin.site.urls, name='admin'),
    # path('order', views.update, name='update'),

    # path('categories/', views.CategoryView.as_view(), name='categories'),
    # path('BookingCategories/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail')
]