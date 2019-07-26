from django.db import models
import time

# Create your models here.
class user(models.Model):
    id = models.AutoField(primary_key=True)
    loginname = models.TextField(max_length=50)
    password = models.TextField(max_length=50)
#updatetime = models.DateTimeField()
#lastchapter = models.CharField(max_length=100)


class user_info(models.Model):
    name = models.TextField(max_length=50)
    tel = models.IntegerField(null=True)
    cer = models.IntegerField(null=True)
    uid = models.OneToOneField(user, on_delete=models.CASCADE)

def upload_to(instance, filename):
    stt = time.strftime("%Y%m%d",time.localtime())
    return '/'.join(['cjdj',stt,filename])


class Cjdj_info(models.Model):
    id = models.AutoField(primary_key = True)
    dizhi = models.TextField(max_length = 500)
    lx = models.TextField(max_length = 500)
    mianji = models.FloatField()
    zongjia = models.FloatField()
    dj = models.FloatField()
    cjdate = models.DateTimeField()
    down = models.FileField(upload_to=upload_to)


def __str__(self):
    return self.text