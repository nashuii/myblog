from django.conf.urls import url,include
from django.contrib import admin
from api.common import views

urlpatterns = [
    url(r'^common_captcha/$', views.common_captcha,name='common_captcha'),

]