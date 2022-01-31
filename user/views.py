from django.contrib import auth
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.utils import timezone

from .models import Registration, Loans, Studyloan, Homeloan, Personalloan, Vechileloan, Bussinessloan, Newuser, \
    Amounttaken, Transactions, BankList, Usermessages
from admin12.models import Adminmessages


def home_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')
    # return response
    return render(request, "homepage.html")


def billpayment_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    return render(request, "billpayment.html")


def creditcard_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')

        cardno = request.POST['cardno']
        name = request.POST['cardname']
        cvv = request.POST['cvv']
        expiry = request.POST['expiry']
        bank = request.POST['selectbank']
        amount = request.POST['amount']

        if cardno and name and cvv and expiry and bank and amount:
            user = Registration.objects.get(email=email)
            amount1 = user.balance
            print(amount1 - int(amount))
            if (amount1 < int(amount)):
                return render(request, "creditcard.html", {'message': "Amount Insufficient"})
            user.balance = amount1 - int(amount)

            trac = Transactions()
            trac.Email_Id = email
            trac.Account_Number = user.actno
            trac.Type_Of_Transaction = "CreditCard Bill"
            trac.Date = datetime.now()
            trac.Status = "Debited"
            trac.Amount = amount
            trac.save()

            user.save()

            return render(request, "creditcard.html", {'message': "Payment Successfull"})
        else:
            return render(request, "creditcard.html", {'message': "Enter All Fields"})

    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')
        return render(request, "creditcard.html")


def recharge_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':

        phnno = request.POST['phnnumber']
        amount = request.POST['phnamount']
        carrier = request.POST['carrier']

        if phnno and amount and carrier:
            if 'user_email' in request.session:
                email = request.session['user_email']
            else:
                return redirect('login')
            amount = int(amount)
            user = Registration.objects.get(email=email)
            amount1 = user.balance
            if (amount1 < amount):
                return render(request, "recharge.html", {'message': "Amount Insufficient"})

            print(amount1 - amount)
            user.balance = amount1 - amount

            trac = Transactions()
            trac.Email_Id = email
            trac.Account_Number = user.actno
            trac.Type_Of_Transaction = "Recharge"
            trac.Date = datetime.now()
            trac.Status = "Debited"
            trac.Amount = amount
            trac.save()

            user.save()

            return render(request, "recharge.html", {'message': "Successfully Recharged"})
        else:
            return render(request, "recharge.html", {'message': "Enter All fields"})

    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')

        return render(request, "recharge.html")


def payment_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':

        actnumber = request.POST['actnumber']
        ifsc = request.POST['actifsc']
        amount = request.POST['actamount']

        if actnumber and ifsc and amount:
            if 'user_email' in request.session:
                email = request.session['user_email']
            else:
                return redirect('login')
            amount = int(amount)
            try:
                user = Registration.objects.get(email=email)
                user1 = Registration.objects.get(actno=actnumber)
                amount2 = user1.balance
            except:
                return render(request, "payment.html", {'message': "AccountNumber Not Found"})

            if user1.actno == actnumber and user1.actifsc == ifsc:
                p = amount2 + amount
                user1.balance = p
                user1.save()
                amount1 = user.balance
                print(amount1 - amount)
                user.balance = amount1 - amount

                trac = Transactions()
                trac.Email_Id = email
                trac.Account_Number = user.actno
                trac.Type_Of_Transaction = "Payment Transfer"
                trac.Date = datetime.now()
                trac.Status = "Debited"
                trac.Amount = amount
                trac.save()

                trac1 = Transactions()
                trac1.Email_Id = user1.email
                trac1.Account_Number = user.actno
                trac1.Type_Of_Transaction = "Payment Transfer"
                trac1.Date = datetime.now()
                trac1.Status = "Credited"
                trac1.Amount = amount
                trac1.save()

                user.save()
                return render(request, "payment.html", {'message': "SucessFully Transfer"})

            else:
                return render(request, "payment.html", {'message': "AccountNumber Not Found or Not Matched"})

        else:
            return render(request, "payment.html", {'message': "Enter all Fields"})

    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')

        return render(request, "payment.html")


def registration_view(request):
    if request.method == "POST":
        if request.POST.get('email') and request.POST.get('actno') and request.POST.get('actcif') and request.POST.get(
                'actifsc') and request.POST.get('branch') and request.POST.get('dob') and request.POST.get('password'):

            email = request.POST.get('email')
            actno = request.POST.get('actno')
            actcif = request.POST.get('actcif')
            actifsc = request.POST.get('actifsc')
            branch = request.POST.get('branch')
            dob = request.POST.get('dob')
            password = request.POST.get('password')

            record = Registration.objects.get(email=email)
            if(record.password!=""):
                return render(request, "registration.html", {'message': "Already a user"})



            if record.actno == actno and record.actcif == actcif and record.actifsc == actifsc and record.branch == branch:
                record.password = password
                record.save()
            else:
                return render(request, "registration.html", {'message': "Invalid Details"})

            return render(request, "registration.html", {'message': "Successfully Registered"})
        else:
            return render(request, "registration.html", {'message': "Enter All Fields"})
    else:
        return render(request, "registration.html")


def login_view(request):
    if request.method == 'POST':
        print('entered')
        email = request.POST['email']
        print(email)
        pwd = request.POST['pwd']
        print(pwd)

        try:
            user = Registration.objects.get(email=email)
        except:
            return render(request, "login.html")
        request.session['user_email'] = user.email


        if (user.password == pwd):
            """""request.session.set_expiry(30)"""""
            return redirect('home')
        else:
            return HttpResponseRedirect("login failed")
    else:
        emi()
        return render(request, "login.html")


def loans_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':
        loantype = request.POST['loantype']
        if loantype == "StudyLoan":
            try:
                loan = Studyloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "HomeLoan":
            try:
                loan = Homeloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "PersonalLoan":
            try:
                loan = Personalloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "VechileLoan":
            try:
                loan = Vechileloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "BussinessLoan":
            try:
                loan = Bussinessloan.objects.get(email=email)
            except:
                loan = None
        else:
            loan = None

        def emi1(p, r, t):
            t = t / 12
            emi = (p * t * r) / 100

            return emi


        date = datetime.now()

        salary = request.POST['salary']
        amount = request.POST['amount']
        timeperiod = request.POST['timeperiod']

        if loantype and date and salary and amount and timeperiod :
            salary = int(salary)
            amount = int(amount)
            timeperiod = int(timeperiod)
        else:
            return render(request, 'loans.html', {'message': "Enter All Fields"})

        if loan != None:
            return render(request, 'loans.html', {'message': "Only one Loan type Can Taken"})

        def emi1(p, r, t):
            t = t / 12
            emi = (p * t * r) / 100

            return emi

        try:
            banks = BankList.objects.filter(loantype=loantype)
        except:
            return render(request, 'loans.html', {'message': "Contact Admin"})

        list = []
        print(amount)

        for bank in banks:
            if (emi1(amount,bank.intrest,timeperiod) + amount < ((salary / 100) * 40)):
                list.append(bank)
                print(bank.bankname)
        print(list)
        if (list):

            return render(request, 'loans.html', {'list': list})
        else:
            return render(request, 'loans.html', {'message': "No Bank Found"})



    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')
        return render(request, "loans.html")




def myaccount_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    try:
        user = Registration.objects.get(email=email)
    except Registration.DoesNotExist:
        user = None

    try:
        studyloan = Studyloan.objects.get(email=email)
    except Studyloan.DoesNotExist:
        studyloan = None

    try:
        homeloan = Homeloan.objects.get(email=email)
    except Homeloan.DoesNotExist:
        homeloan = None

    try:
        personalloan = Personalloan.objects.get(email=email)
    except Personalloan.DoesNotExist:
        personalloan = None

    try:
        vechileloan = Vechileloan.objects.get(email=email)
    except Vechileloan.DoesNotExist:
        vechileloan = None

    try:
        businessloan = Bussinessloan.objects.get(email=email)
    except Bussinessloan.DoesNotExist:
        businessloan = None

    loan = [studyloan, businessloan, homeloan, vechileloan, personalloan]
    return render(request, 'myaccount.html', {'user': user})


def newuser_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        panno = request.POST['panno']
        adharno = request.POST['adharno']
        dob = request.POST['dob']
        phnnum = request.POST['phnnum']
        branch = request.POST['branch']
        city = request.POST['city']
        try:
            gender = request.POST['gender']
        except:
            return render(request, 'newuser.html', {'message': "Enter All Fields"})

        gender = request.POST['gender']
        if name and email and panno and adharno and dob and phnnum and branch and city and gender:
            try:
                Newuser.objects.get(email=email)
                return render(request, 'newuser.html', {'message': "Already Applied"})
            except:
                None

            try:
                Registration.objects.get(email=email)
                Registration.objects.get(adharno=adharno)
                Registration.objects.get(panno=panno)
                return render(request, 'newuser.html', {'message': "Already a USER"})
            except:
                None

            newuser = Newuser()
            newuser.name = name
            newuser.email = email
            newuser.panno = panno
            newuser.adharno = adharno
            newuser.dob = dob
            newuser.phnnum = phnnum
            newuser.branch = branch
            newuser.city = city
            newuser.gender = gender
            newuser.save()
            return render(request, 'newuser.html', {'message': "Sucessfully Applied"})
        else:
            return render(request, 'newuser.html', {'message': "Enter All Fields"})
    else:
        return render(request, 'newuser.html')


def aboutus_view(request):
    return (request,'aboutus.html')

def payloan_view(request):
    if 'user_email' in request.session:
        None
    else:
        return redirect('login')

    if request.method == 'POST':
        loantype = request.POST['submit']

        request.session['loan_type'] = loantype
        return redirect('loanpayment')
    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')
        print(email)
        loan = []
        try:
            studyloan = Studyloan.objects.get(email=email)
            loan.append(studyloan)
        except Studyloan.DoesNotExist:
            studyloan = None


        try:
            personalloan = Personalloan.objects.get(email=email)
            loan.append(personalloan)

        except Personalloan.DoesNotExist:
            personalloan = None

        try:
            homeloan = Homeloan.objects.get(email=email)
            loan.append(homeloan)
        except Homeloan.DoesNotExist:
            homeloan = None

        try:
            vechileloan = Vechileloan.objects.get(email=email)
            loan.append(vechileloan)



        except Vechileloan.DoesNotExist:
            vechileloan = None

        try:
            businessloan = Bussinessloan.objects.get(email=email)
            loan.append(businessloan)

        except Bussinessloan.DoesNotExist:
            businessloan = None

        return render(request, 'payloan.html', {'loans': loan});


def loanpayment_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')
        print(email)

        loantype = request.session['loan_type']

        if loantype == "StudyLoan":
            loan = Studyloan.objects.get(email=email)
        elif loantype == "HomeLoan":
            loan = Homeloan.objects.get(email=email)
        elif loantype == "PersonalLoan":
            loan = Personalloan.objects.get(email=email)
        elif loantype == "VechileLoan":
            loan = Vechileloan.objects.get(email=email)
        elif loantype == "BussinessLoan":
            loan = Bussinessloan.objects.get(email=email)
        else:
            None

        user = Registration.objects.get(email=email)

        amount = request.POST['amount']
        if amount:
            amount = int(amount)

        else:
            return render(request, 'loanpayment.html', {'message': "EnterAmount"})

        if amount > loan.amounthavetopay:
            return render(request, 'loanpayment.html', {'message': "Amount Exceed Than pay Amount"})

        if (user.balance > amount):
            loan.amountpayed = loan.amountpayed + amount
            loan.amounthavetopay = loan.amounttaken - loan.amountpayed + loan.emi
            user.balance = user.balance - amount

            trac = Transactions()
            trac.Email_Id = email
            trac.Account_Number = user.actno
            trac.Type_Of_Transaction = "Loan Payment"
            trac.Date = datetime.now()
            trac.Status = "Debited"
            trac.Amount = amount
            trac.save()

            loan.save()
            user.save()
        else:
            return render(request, 'loanpayment.html', {'message': "Amount Insufficient"})
        return render(request, 'loanpayment.html', {'message': "Amount successfully Paied"})

    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')

        return render(request, 'loanpayment.html')


def logut_view(request):
    del request.session['user_email']
    return redirect('login')


def transcation_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    try:
        data = Transactions.objects.filter(Email_Id=email)
        print(data)
        chartdata = []
        m = len(Transactions.objects.filter(Type_Of_Transaction='Recharge', Email_Id=email))
        chartdata.append(m)
        cb = len(Transactions.objects.filter(Type_Of_Transaction='Loan Payment', Email_Id=email))
        chartdata.append(cb)
        crb = len(Transactions.objects.filter(Type_Of_Transaction='CreditCard Bill', Email_Id=email))
        chartdata.append(crb)

        crb1 = len(Transactions.objects.filter(Type_Of_Transaction='Payment Transfer', Email_Id=email))
        chartdata.append(crb1)

        print(chartdata)
        message1 = 'Transcations'
        labels = ['mobile recharge', 'loan payment', 'creditcard bill', 'payment transfer']
        context = {
            'dataset': data,
            'message': email,
            'labels': labels,
            'data': chartdata,
            'message1': message1
        }
        return render(request, "transactions.html", context)
    except:
        return render(request, "transactions.html", {'message': "NO Transactions"})

    return render(request, "transactions.html", dataset)


def amountsaclist_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')
    user = Registration.objects.get(email=email)
    try:
        data = Amounttaken.objects.filter(actno=user.actno)
        print(data)
        context = {
            'dataset': data
        }
        return render(request, 'loansaclist.html', context)
    except:
        return render(request, 'loansaclist.html', {'message': "No amount Approved"})

    return render(request, 'loansaclist.html', context)


def emi():
    list = Amounttaken.objects.all()
    date1 = datetime.now(timezone.utc)
    loan = None
    for l in list:
        if l.loantype == "StudyLoan":
            try:
                loan = Studyloan.objects.get(loanactno=l.loanactno)
            except:
                loan = None
        elif l.loantype == "HomeLoan":
            try:
                loan = Homeloan.objects.get(loanactno=l.loanactno)
            except:
                loan = None
        elif l.loantype == "PersonalLoan":
            try:
                loan = Personalloan.objects.get(loanactno=l.loanactno)
            except:
                loan = None
        elif l.loantype == "VechileLoan":
            try:
                loan = Vechileloan.objects.get(loanactno=l.loanactno)
            except:
                loan = None
        elif l.loantype == "BussinessLoan":
            try:
                loan = Bussinessloan.objects.get(loanactno=l.loanactno)
            except:
                loan = None
        else:
            loan = None
        t = (date1 - l.date).days / (12 * 12)
        pt = l.amount
        try:
            ampt = loan.amountpayed
        except:
            ampt=0

        if pt - ampt > 0:
            ampt = ampt - pt
            continue
        else:
            pt = pt - ampt
            ampt = 0

        r = loan.interest
        l.amountemi = (pt * r * t) / 100
        loan.emi = loan.emi + l.amountemi
        l.save()
        loan.amounthavetopay = loan.amounttaken - loan.amountpayed + loan.emi

        loan.save()


def landingpage_view(request):
    return (request,'landingpage.html')


def pivot_data(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method=='POST':
        # session will be used here
        labels = ['amount balance', 'amount taken', 'amount have to pay', 'amountpayed']
        loantype = request.POST['loantype']
        print(loantype)
        dataset = []
        if (loantype == 'StudyLoan'):
            try:
                s = Studyloan.objects.get(email=email)
                amb = s.amountbalance
                dataset.append(amb)
                amt = s.amounttaken
                dataset.append(amt)
                ampay = s.amounthavetopay
                dataset.append(ampay)
                amp = s.amountpayed
                dataset.append(amp)
            except:
                return render(request, 'piechart.html', {'message': "you have not taken studyloan"})
        elif (loantype == 'HomeLoan'):
            try:
                s = Homeloan.objects.get(email=email)

                amb = s.amountbalance
                dataset.append(amb)
                amt = s.amounttaken
                dataset.append(amt)
                ampay = s.amounthavetopay
                dataset.append(ampay)
                amp = s.amountpayed
                dataset.append(amp)
            except:
                return render(request, 'piechart.html', {'message': "you have not taken homeloan"})


        elif (loantype == 'PersonalLoan'):
            try:
                s = Personalloan.objects.get(email=email)
                amb = s.amountbalance
                dataset.append(amb)
                amt = s.amounttaken
                dataset.append(amt)
                ampay = s.amounthavetopay
                dataset.append(ampay)
                amp = s.amountpayed
                dataset.append(amp)
            except:
                return render(request, 'piechart.html', {'message': "you have not taken personal loan"})

        elif (loantype == 'VechileLoan'):
            try:
                s = Vechileloan.objects.get(email=email)
                amb = s.amountbalance
                dataset.append(amb)
                amt = s.amounttaken
                dataset.append(amt)
                ampay = s.amounthavetopay
                dataset.append(ampay)
                amp = s.amountpayed
                dataset.append(amp)
            except:
                return render(request, 'piechart.html', {'message': "you have not taken vehicle loan"})

        elif (loantype == 'BussinessLoan'):
            try:
                s = Bussinessloan.objects.get(email=email)
                amb = s.amountbalance
                dataset.append(amb)
                amt = s.amounttaken
                dataset.append(amt)
                ampay = s.amounthavetopay
                dataset.append(ampay)
                amp = s.amountpayed
                dataset.append(amp)
            except:
                return render(request, 'piechart.html', {'message': "you have not taken bussiness loan"})

        else:
            return render(request, 'piechart.html', {'message': "select loan type"})

        print(dataset)
        message = 'loanDetails'
        return render(request, 'piechart.html', {
            'labels': labels,
            'message': message,
            'data': dataset,
        })
    else:
        return render(request,'piechart.html')

def about_us(request):
    return render(request,'aboutus.html')
def loancalculator(request):
    return render(request,'caluculator.html')







def applyloanuser_view(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':

        def emi1(p, r, t):
            t = t / 12
            emi = (p * t * r) / 100

            return emi

        loantype = request.POST['loantype']
        print(email)

        if loantype == "StudyLoan":
            try:
                loan = Studyloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "HomeLoan":
            try:
                loan = Homeloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "PersonalLoan":
            try:
                loan = Personalloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "VechileLoan":
            try:
                loan = Vechileloan.objects.get(email=email)
            except:
                loan = None
        elif loantype == "BussinessLoan":
            try:
                loan = Bussinessloan.objects.get(email=email)
            except:
                loan = None
        else:
            loan = None

        date = datetime.now()

        salary = request.POST['salary']
        amount = request.POST['amount']
        timeperiod = request.POST['timeperiod']
        bankname=request.POST['bankname']

        if loantype and date and salary and amount and timeperiod and bankname:
            salary = int(salary)
            amount = int(amount)
            timeperiod = int(timeperiod)
        else:
            return render(request, 'applyloanuser.html', {'message': "Enter All Fields"})

        if loan != None:
            return render(request, 'applyloanuser.html', {'message': "Only one Loan type Can Taken"})

        bank = BankList.objects.get(loantype=loantype,bankname=bankname)
        interest=bank.intrest
        emi1 = emi1(amount, interest, timeperiod)
        print(emi1)

        if emi1:
            if (amount + emi1) < ((salary / 100) * 40):
                loan = Loans()
                user = Registration.objects.get(email=email)
                loan.email = user.email
                loan.actno = user.actno
                loan.loantype = loantype

                loan.interest = interest
                loan.date = date
                loan.salary = salary
                loan.timeperiod = timeperiod
                loan.amount = amount
                loan.emi = int(emi1)
                loan.bankname=bankname
                loan.save()
                return render(request, 'applyloanuser.html', {'message': "LoanRequest Send"})
            else:
                return render(request, 'applyloanuser.html', {'message': "Loan Cannot be Applied Contact Admin"})

        else:
            return render(request, 'applyloanuser.html', {'message': "Error"})

    else:
        if 'user_email' in request.session:
            email = request.session['user_email']
        else:
            return redirect('login')
        return render(request, "applyloanuser.html")

def sendmessage(request):
    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')

    if request.method == 'POST':
        message=request.POST['message']
        if message and email:
            send = Adminmessages()
            send.message = message
            send.email = email
            send.save()
            return render(request, 'customerservice.html', {'message': "Send request"})
        else:
            return render(request, 'customerservice.html', {'message': "Enter all Fields"})
    else:
        return render(request, 'customerservice.html')


def usermessages(request):

    if 'user_email' in request.session:
        email = request.session['user_email']
    else:
        return redirect('login')
    message=[]
    try:
        message=Usermessages.objects.filter(email=email)
        return render(request,'usermessages.html',{'message':message})
    except:
        message=None
        return render(request, 'usermessages.html', {'message1': "No messages"})
