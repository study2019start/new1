from django.shortcuts import render
from django.contrib import messages
from django import forms
from myappweb.models import user,Cjdj_info
from django.forms import widgets
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


class UserForm(forms.Form):   # 必须继承forms.Form
    name = forms.CharField(label="用户名  ", required=True, error_messages={"required": "不能为空"},
                           widget=widgets.TextInput())
    pwd = forms.CharField(label="密    码  ", required=True, error_messages={"required": "不能为空"},
                          widget=widgets.PasswordInput())


class TestForm(forms.Form):
    photo = forms.FileField(label='your photo')


def login(request):
    form = UserForm() 
    if request.method == "POST":
        form1 = UserForm(request.POST)
        if form1.is_valid():
            data1 = form1.clean()
            result = user.objects.filter(loginname=data1["name"], password=data1["pwd"],)
            print(data1["name"])
            if result.exists():
                return render(request, 'myappweb/index.html', {'name': data1["name"]})
            else:
                messages.success(request, "错误")
                return render(request, 'myappweb/login.html')
        else:
            
            errors = form1.errors
            return render(request, 'myappweb/login.html', {"form":form, "errors":errors})
    else:
        return render(request, 'myappweb/login.html', {"form": form})


def index(request):
    return render(request, 'myappweb/index.html')


@csrf_exempt
def test(request):
    if request.method == 'POST':
        
        form1 = TestForm(request.POST, request.FILES)
       
        if  False :#form1.is_valid():
            dz = "中华路"
            lx = "1600"
            mj = 100
            zj = 600
            dj = 6.05
            down = form1.cleaned_data['photo']
            print(down)
            cjdd = Cjdj_info.objects.create(dizhi=dz, lx=lx, mianji=mj, zongjia=zj, dj=dj, cjdate='2018-05-01', down = down)
            cjdd.save()
            ff = TestForm()
            return render(request,"myappweb/test.html",{"form1" : ff})
        else:
            rq = request.FILES.get("upload")
            fiel_path = os.path.join("cjdj",rq.name)
            with open(fiel_path,'wb')as f:
                for chunk in rq.chunks():
                    f.write(chunk)
                f.close()
            ff = TestForm()
            da={}
            da['aa']="成功"
            da['name']=rq.name
            print(da)        
            return HttpResponse(json.dumps(da,ensure_ascii=False),content_type="application/json,charset=utf-8")
            return render(request,"myappweb/test.html",{"form1" : ff})

    else:
        
        form1 = TestForm()
        return render(request,"myappweb/test.html",{"form1" : form1})
# Create your views here.





