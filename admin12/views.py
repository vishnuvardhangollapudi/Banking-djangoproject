from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.views.generic.base import View
from rest_framework.views import APIView

# Create your views here.
from django.utils import timezone
from pip._vendor.requests import Response

from user.models import Registration, Loans, Studyloan, Homeloan, Personalloan, Vechileloan, Bussinessloan, \
    Newuser, Amounttaken, Transactions,BankList,Usermessages
from django.views.generic import View
from rest_framework.templatetags.rest_framework import data

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Adminmessages


def addmoney_view(request):
    if request.method == 'POST':
        actno1 = request.POST['actno1']
        amount = int(request.POST['amount'])
        if actno1 and amount:
            try:
                employee = Registration.objects.get(actno=actno1)
            except Registration.DoesNotExist:
                employee = None
            if employee == None:
                return render(request, "addmoney.html", {'message': "AccountNumber Not Found"})

            else:
                amount1 = employee.balance
                print(amount1 + amount)
                employee.balance = amount1 + amount

                trac = Transactions()
                trac.Email_Id = employee.email
                trac.Account_Number = employee.actno
                trac.Type_Of_Transaction = "Admin Added money"
                trac.Date = datetime.now()
                trac.Status = "Credited"
                trac.Amount = amount
                trac.save()

                employee.save()
                return render(request, "addmoney.html", {'message': "Successfully Added"})


        else:
            return render(request, "addmoney.html", {'message': "Enter all Fields"})



    else:
        return render(request, "addmoney.html")


def loanslist_view(request):
    if request.method == 'POST' and 'submit' in request.POST:
        email = request.POST['submit']
        print(email)
        request.session['approved_loan'] = email

        return redirect('approveloan')
    elif request.method == 'POST' and 'delete' in request.POST:
        email = request.POST['delete']
        loandetails = Loans.objects.get(email=email)
        loandetails.delete()
        return redirect('loanslist')
    else:
        loanslist = Loans.objects.filter()
        return render(request, 'loanslist.html', {'loanslist': loanslist})


def approveloan_view(request):
    if request.method == 'POST':
        amount = int(request.POST['amountapproved'])
        email = request.session['approved_loan']
        print(email)
        loandetails = Loans.objects.get(email=email)
        if loandetails.loantype == "StudyLoan":
            loantype = Studyloan()
            loantype.loanactno = "STUDY" + loandetails.actno
        elif loandetails.loantype == "HomeLoan":
            loantype = Homeloan()
            loantype.loanactno = "HOME" + loandetails.actno
        elif loandetails.loantype == "PersonalLoan":
            loantype = Personalloan()
            loantype.loanactno = "PERSONAL" + loandetails.actno
        elif loandetails.loantype == "VechileLoan":
            loantype = Vechileloan()
            loantype.loanactno = "VECHILE" + loandetails.actno
        elif loandetails.loantype == "BussinessLoan":
            loantype = Bussinessloan()
            loantype.loanactno = "BUSINESS" + loandetails.actno

        propertyvalue = Registration.objects.get(email=email)
        propertyvalue.propertyamount = int(request.POST['propertyamount'])
        propertyvalue.save()
        if(loandetails.amount<amount):
            return render(request,"approveloan.html",{'message':"Amount Request Exceeded"})

        loantype.email = loandetails.email
        loantype.actno = loandetails.actno
        loantype.loantype = loandetails.loantype
        loantype.interest = loandetails.interest
        loantype.date = loandetails.date
        loantype.timeperiod = loandetails.timeperiod
        loantype.salary = loandetails.salary
        loantype.bankname=loandetails.bankname
        def emi1(p, r, t):
            t=t/12
            emi=(p*t*r)/100

            return emi
        loantype.emi = emi1(amount,loantype.interest,loantype.timeperiod)
        loantype.amount = amount
        loantype.amounttaken = 0
        loantype.amountbalance = amount
        loantype.amounthavetopay = 0
        loantype.amounttopayed = 0
        loantype.save()
        del request.session['approved_loan']
        loandetails.delete()

        return render(request,"approveloan.html",{'message':"Loan Approved"})
    else:
        return render(request, "approveloan.html")


def newuserlist_view(request):
    if request.method == 'POST' and 'submit' in request.POST:
        email = request.POST['submit']
        user = Newuser.objects.get(email=email)
        try:
            adduser = Registration()
            adduser.name = user.name
            adduser.email = user.email
            adduser.panno = user.panno
            adduser.adharno = user.adharno
            adduser.dob = user.dob
            adduser.branch = user.branch
            adduser.city = user.city
            adduser.gender = user.gender
            adduser.phnnum = user.phnnum
            adduser.actcif = "987" + user.phnnum
            adduser.actno = user.adharno
            adduser.actifsc = user.branch + "12345"
            adduser.save()
            user.delete()
        except:
            return render(request, 'newuserlist.html', {'message': "Details Alreasy Exist"})


        return redirect('newuserlist')
    elif request.method == 'POST' and 'delete' in request.POST:
        email = request.POST['delete']
        user = Newuser.objects.get(email=email)
        user.delete()
        return redirect('newuserlist')
    else:
        newuserlist = Newuser.objects.all()
        return render(request, 'newuserlist.html', {'newuserlist': newuserlist})


def approveloanamount_view(request):
    if request.method == 'POST':
        loanactno = request.POST['loanactno']
        actno = request.POST['actno']
        loantype = request.POST['loantype']
        amount = int(request.POST['amount'])

        if loanactno and actno and loantype and amount:
            if loantype == "StudyLoan":
                try:
                    loan = Studyloan.objects.get(loanactno=loanactno)
                except:
                    return render(request, "aproveloanamount.html", {'message': "Enter Valid Loan "})
            elif loantype == "HomeLoan":
                try:
                    loan = Homeloan.objects.get(loanactno=loanactno)
                except:
                    return render(request, "aproveloanamount.html", {'message': "Enter Valid Loan"})
            elif loantype == "PersonalLoan":
                try:
                    loan = Personalloan.objects.get(loanactno=loanactno)
                except:
                    return render(request, "aproveloanamount.html", {'message': "Enter Valid Loan "})
            elif loantype == "VechileLoan":
                try:
                    loan = Vechileloan.objects.get(loanactno=loanactno)
                except:
                    return render(request, "aproveloanamount.html", {'message': "Enter Valid Loan"})
            elif loantype == "BussinessLoan":
                try:
                    loan = Bussinessloan.objects.get(loanactno=loanactno)
                except:
                    return render(request, "aproveloanamount.html", {'message': "Enter Valid Loan "})
            else:
                loan=None


            if(loan.amount<amount):
                return render(request, "aproveloanamount.html", {'message': "Amount Exceeded "})

            if loan==None:
                return render(request,"aproveloanamount.html",{'message':"User Not Found"})

            if (loan.actno == actno):

                amountlist = Amounttaken()
                amountlist.loanactno = loan.loanactno
                amountlist.actno = loan.actno
                amountlist.loantype = loan.loantype
                amountlist.date = datetime.now()
                amountlist.amount = amount
                amountlist.interest = loan.interest

                date1 = datetime.now(timezone.utc)
                date = loan.date
                dy = (date1 - date).days
                dy = dy / (12 * 12)
                emi = (amount * loan.interest * ((loan.timeperiod / 12) - dy)) / 100
                print( loan.amounttaken )
                print(amount)
                try:
                    user = Registration.objects.get(actno=actno)
                except:
                    user = None
                user.balance = user.balance + amount
                user.save()

                loan.amounttaken = loan.amounttaken + amount
                loan.amountbalance = loan.amount - amount
                loan.amounthavetopay = loan.amounttaken - loan.amountpayed + emi
                amountlist.amountemi = emi
                amountlist.save()

                trac = Transactions()
                trac.Email_Id = loan.email
                trac.Account_Number = loan.actno
                trac.Type_Of_Transaction = "Loan Amount"
                trac.Date = datetime.now()
                trac.Status = "Credited"
                trac.Amount = amount
                trac.save()


                loan.save()


                return render(request, "aproveloanamount.html", {'message': "Amount Approved"})
            else:
                return render(request,"aproveloanamount.html",{'message':"Enter Correct Account Number "})

        else:
            return render(request,"aproveloanamount.html",{'message':"Enter All Fields"})

    else:
        return render(request, 'aproveloanamount.html')


def adminlogin_view(request):
    if request.method == 'POST':
        email1=request.POST['email']
        password=request.POST['pwd']
        if email1 and password:
            if email1 == "admin@gmail.com" and password == "admin@1234":
                request.session['adminemail'] = email1
                return redirect('adminhome')
            else:
                return redirect('adminlogin')
        else:
            return redirect('adminlogin')



    else:
        return render(request,'adminlogin.html')

def adminhome_view(request):
    if 'adminemail' in request.session:
        email1 = request.session['adminemail']
    else:
        return redirect('adminlogin')

    return render(request,'adminhomepage.html')


def banklist_view(request):
    if request.method=="POST":
        bankname = request.POST['bankname']
        loantype = request.POST['loantype']
        intrest = request.POST['intrest']
        description = request.POST['description']
        if bankname and loantype and intrest and description:
            banklist=BankList()
            banklist.bankname=bankname
            banklist.loantype=loantype
            banklist.intrest=int(intrest)
            banklist.description=description
            banklist.save()
            return render(request,'addbanklist.html')
        else:
            return render(request,'addbanklist.html',{'message':"enter all felds"})
    else:
        return render(request, 'addbanklist.html')



def Banks(request):
    if request.method=='POST':
        bank=request.POST['bank']
        email='190030520@kluniversity.in'
        print(bank)
        if(bank=='SBI BANK'):
            data=[]
            data=Loans.objects.filter(bank='State Bank of India',email=email)
            len(data)
            message='SBI BANK'
            context={
                'dataset':data,
                'message':message
            }
            print('entered')

            return render(request,'loanlist.html',context)
        elif (bank=='ICICI Bank'):
            data = []
            data = Loans.objects.filter(bank='ICICI Bank',email=email)
            message = 'ICICI BANK'
            context = {
                'dataset': data,
                'message': message
            }

            return render(request, 'loanlist.html', context)
        elif (bank=='AXES'):
            data = []
            data = Loans.objects.filter(bank='Central Bank of India',email=email)
            message = 'Central Bank of India'
            context = {
                'dataset': data,
                'message': message
            }

            return render(request, 'loanlist.html', context)
        else:
            return render(request,'login.html')
    else:
        return render(request,'sbi.html')



def adminuserloanlist(request):

    loan = []
    try:
        studyloan = Studyloan.objects.filter()
        loan.extend(studyloan)
    except Studyloan.DoesNotExist:
        studyloan = None


    try:
        personalloan = Personalloan.objects.filter()
        loan.extend(personalloan)

    except Personalloan.DoesNotExist:
        personalloan = None

    try:
        homeloan = Homeloan.objects.filter()
        loan.extend(homeloan)
    except Homeloan.DoesNotExist:
        homeloan = None

    try:
        vechileloan = Vechileloan.objects.filter()
        loan.extend(vechileloan)



    except Vechileloan.DoesNotExist:
        vechileloan = None

    try:
        businessloan = Bussinessloan.objects.filter()
        loan.extend(businessloan)

    except Bussinessloan.DoesNotExist:
        businessloan = None



    return render(request, 'adminuserloanlist.html', {'loans': loan})








class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'adminloanscharts.html')


####################################################

## if you don't want to user rest_framework

# def get_data(request, *args, **kwargs):
#
# data ={
#             "sales" : 100,
#             "person": 10000,
#     }
#
# return JsonResponse(data) # http response


#######################################################

## using rest_framework classes

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'studyloan',
            'homeloan',
            'personalloan',
            'vehicalloan',
            'businessloan'
        ]
        chartLabel = "my data"
        chartdata=[]
        s=0,
        h=0
        p=0
        v=0
        b=0
        s=len(Studyloan.objects.all())
        chartdata.append(s)
        h = len(Homeloan.objects.all())
        chartdata.append(h)
        p = len(Personalloan.objects.all())
        chartdata.append(p)
        v = len(Vechileloan.objects.all())
        chartdata.append(v)
        b = len(Bussinessloan.objects.all())
        chartdata.append(b)
        print(chartdata)

        data = {
            "labels": labels,
            "chartLabel": chartdata,
            "chartdata": chartdata,
        }
        return Response(data)

def userlist(request):
    data=[]
    data=Registration.objects.filter()
    a=len(Registration.objects.filter())
    context={
        'dataset':data,
        'message':a
    }
    return render(request,'userdetails.html',context)


def sendmessageuser(request):
    if request.method=='POST':
        message=request.POST['message']
        email=request.POST['email']

        if message and email:
            message1=Usermessages()
            message1.message=message
            try:
                user=Registration.objects.get(email=email)
            except:
                user=None
            if(user!=None):
                message1.email=email
                message1.save()
                return render(request,'sendmessageuser.html',{'message':"successfully sent"})
            else:
                return render(request, 'sendmessageuser.html', {'message': "User not Found"})
        else:
            return render(request, 'sendmessageuser.html', {'message': "enter all fields"})
    else:
        return render(request, 'sendmessageuser.html')

def messagefromuser(request):
    message=[]
    try:
        message=Adminmessages.objects.filter()
        return render(request,'messagefromuser.html',{'message':message})
    except:
        message=None
        return render(request, 'messagefromuser.html', {'message1': "No messages"})

