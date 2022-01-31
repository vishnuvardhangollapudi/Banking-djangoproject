from django.db import models


class Adminmessages(models.Model):
    id = models.AutoField(primary_key=True)
    message=models.CharField(max_length=1024)
    email=models.CharField(max_length=50)
    class Meta:
        db_table="adminnmessage"
