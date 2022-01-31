from django.urls import path

from .views import addmoney_view, loanslist_view, approveloan_view, newuserlist_view, approveloanamount_view, \
    adminlogin_view, adminhome_view, HomeView, ChartData, banklist_view, adminuserloanlist, userlist, sendmessageuser, \
    messagefromuser

urlpatterns = [
path('addmoney/', addmoney_view, name="addmoney"),
path('loanslist/', loanslist_view, name="loanslist"),
path('approveloan/', approveloan_view, name="approveloan"),
path('approveloanamount/', approveloanamount_view, name="approveloanamount"),
path('adminlogin/', adminlogin_view, name="adminlogin"),
path('newuserlist/', newuserlist_view, name="newuserlist"),
path('adminhome/', adminhome_view, name="adminhome"),
path('banklist/', banklist_view, name="banklist"),
path('user/',userlist,name='user'),
path('adminuserloanlist/', adminuserloanlist, name="adminuserloanlist"),
path('sendmessageuser/', sendmessageuser, name="sendmessageuser"),
path('messagefromuser/', messagefromuser, name="messagefromuser"),
path('demo/', HomeView.as_view()),
    # path('test-api', views.get_data),
path('api', ChartData.as_view()),
]
