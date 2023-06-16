from django.contrib import admin
from django.urls import path, include
from API.views import my_view, listview, login_check,getuserdetails,update_user,login_admin,\
    get_posts_by_user,getproblemdetails,run_python,addFriend,submitresult,get_unsolved_problems


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('API.urls')),
    path('my_view/', my_view),
    path('listview/', listview),
    path('logincheck/', login_check),
    path('getuserdetails/', getuserdetails),
    path('update_user/',update_user),
    path('login_admin/',login_admin),
    path('getpostsByUser/',get_posts_by_user),
    path('getProblem/',getproblemdetails),
    path('addFriend/',addFriend),
    path('run-python/',run_python), 
    path('submitresult/',submitresult),
    path('get_unsolved_problems/',get_unsolved_problems)
]
