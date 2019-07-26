from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^index', views.index, name='index'),
   # url(r'^table', views.data, name='table'),
    url(r'^test', views.test, name='test'),

]

app_name = 'myappweb'