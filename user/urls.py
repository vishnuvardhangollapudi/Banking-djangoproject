from django.urls import path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import home_view, billpayment_view, creditcard_view, recharge_view, payment_view, registration_view, \
    login_view, loans_view, myaccount_view, newuser_view, payloan_view, loanpayment_view, logut_view, transcation_view, \
    amountsaclist_view, pivot_data, landingpage_view, about_us, aboutus_view, loancalculator, \
    applyloanuser_view, sendmessage, usermessages

urlpatterns = [
    path('home/billpayment/', billpayment_view, name="billpayment"),
    path('home/billpayment/recharge/', recharge_view, name="recharge"),
    path('home/billpayment/creditcard/', creditcard_view, name="creditcard"),
    path('home/', home_view, name="home"),
    path('home/payloan/loanpayment/', loanpayment_view, name="loanpayment"),
    path('login/newuser/', newuser_view, name="newuser"),
    path('home/payloan/', payloan_view, name="payloan"),
    path('registration/', registration_view, name="regisration"),
    path('login/', login_view, name="login"),
    path('loans/', loans_view, name="loans"),
    path('myaccount/', myaccount_view, name="myaccount"),
    path('aboutus/', aboutus_view, name="aboutus"),
    path('logut/', logut_view, name="logut"),
    path('piechart/', pivot_data, name="piechart"),
    path('home/payment-transfer/', payment_view, name="payment"),
    path('landingpage/', landingpage_view, name="landingpage"),
    path('home/amountsactionlist/', amountsaclist_view, name="amountsaclist"),
    path('home/transactions/',transcation_view, name="transactions"),
    path('about/',about_us,name='about'),
    path('loancalculate/',loancalculator,name='loancalculate'),
    path('applyloanuser/', applyloanuser_view, name='applyloanuser'),
    path('home/customerservice/', sendmessage, name='customerservice'),
    path('home/usermessages/', usermessages, name='usermessages'),
]

urlpatterns += staticfiles_urlpatterns()