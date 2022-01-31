
from django.db import models
from django.db.models import options


class Registration(models.Model):
    name = models.CharField(max_length=50)
    panno = models.CharField(max_length=100, unique='True')
    adharno = models.CharField(max_length=100, unique='True')
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    actcif = models.CharField(max_length=100, unique='True')
    actifsc = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default="")
    balance = models.IntegerField(default=0)
    branch = models.CharField(max_length=10)
    phnnum = models.CharField(max_length=13)
    city = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    propertyamount = models.IntegerField(default=0)
class Transactions(models.Model):
    Email_Id=models.CharField(max_length=100,unique=True)
    Account_Number=models.CharField(max_length=50)
    Type_Of_Transaction=models.CharField(max_length=50)
    Date=models.CharField(max_length=10)
    Amount=models.IntegerField()
    class Meta:
        db_table="transcations"







class Loans(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100)
    loantype = models.CharField(max_length=50)
    interest = models.IntegerField(default=0)
    date = models.DateTimeField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    amount = models.IntegerField()
    timeperiod = models.IntegerField()
    bankname=models.CharField(max_length=50,default=None)

    class Meta:
        db_table = "loans"


class Studyloan(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    loanactno = models.CharField(max_length=100, unique='True')
    loantype = models.CharField(max_length=50, default="")
    interest = models.IntegerField()
    date = models.DateTimeField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    amounthavetopay=models.IntegerField()
    timeperiod = models.IntegerField()
    amount = models.IntegerField()
    amounttaken = models.IntegerField()
    amountbalance = models.IntegerField()
    amountpayed = models.IntegerField(default=0)
    bankname = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "studyloan"


class Homeloan(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    loanactno = models.CharField(max_length=100, unique='True')
    loantype = models.CharField(max_length=50, default="")
    interest = models.IntegerField()
    date = models.DateTimeField()
    amounthavetopay = models.IntegerField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    timeperiod = models.IntegerField()
    amount = models.IntegerField()
    amounttaken = models.IntegerField()
    amountbalance = models.IntegerField()
    amountpayed = models.IntegerField(default=0)
    bankname = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "homeloan"


class Personalloan(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    loanactno = models.CharField(max_length=100, unique='True')
    loantype = models.CharField(max_length=50, default="")
    interest = models.IntegerField()
    amounthavetopay = models.IntegerField()
    date = models.DateTimeField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    timeperiod = models.IntegerField()
    amount = models.IntegerField()
    amounttaken = models.IntegerField()
    amountbalance = models.IntegerField()
    amountpayed = models.IntegerField(default=0)
    bankname = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "personalloan"


class Vechileloan(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    loanactno = models.CharField(max_length=100, unique='True')
    loantype = models.CharField(max_length=50, default="")
    interest = models.IntegerField()
    amounthavetopay = models.IntegerField()
    date = models.DateTimeField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    timeperiod = models.IntegerField()
    amount = models.IntegerField()
    amounttaken = models.IntegerField()
    amountbalance = models.IntegerField()
    amountpayed = models.IntegerField(default=0)
    bankname = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "vechileloan"


class Bussinessloan(models.Model):
    email = models.CharField(max_length=100, primary_key="True")
    actno = models.CharField(max_length=100, unique='True')
    loanactno = models.CharField(max_length=100, unique='True')
    loantype = models.CharField(max_length=50, default="")
    interest = models.IntegerField()
    date = models.DateTimeField()
    amounthavetopay = models.IntegerField()
    salary = models.IntegerField(default=0)
    emi = models.IntegerField()
    timeperiod = models.IntegerField()
    amount = models.IntegerField()
    amounttaken = models.IntegerField()
    amountbalance = models.IntegerField()
    amountpayed = models.IntegerField(default=0)
    bankname = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = "businessloan"


class Newuser(models.Model):
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, primary_key="True")
    panno =  models.CharField(max_length=100, unique='True')
    adharno =  models.CharField(max_length=100, unique='True')
    dob = models.CharField(max_length=10)
    phnnum = models.CharField(max_length=30)
    branch = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)

    class Meta:
        db_table = "newuser"


class Amounttaken(models.Model):
    loanactno=models.CharField(max_length=50)
    actno=models.CharField(max_length=50)
    loantype=models.CharField(max_length=50)
    date=models.DateTimeField()
    amount=models.IntegerField()
    amountemi=models.IntegerField(default=0)
    emi=models.IntegerField(default=0)
    class Meta:
        db_table="loanamtsac"

class Transactions(models.Model):
    Email_Id=models.CharField(max_length=100)
    Account_Number=models.CharField(max_length=50)
    Type_Of_Transaction=models.CharField(max_length=50)
    Date=models.DateTimeField()
    Status=models.CharField(max_length=20)
    Amount=models.IntegerField()
    class Meta:
        db_table="transcations"



class BankList(models.Model):
    id = models.AutoField(primary_key=True)
    bankname=models.CharField(max_length=50)
    loantype=models.CharField(max_length=50)
    intrest=models.IntegerField()
    description=models.CharField(max_length=1024)
    class Meta:
        db_table="banklist"



class Usermessages(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=1024)
    email = models.CharField(max_length=50)

    class Meta:
        db_table = "usermessage"


