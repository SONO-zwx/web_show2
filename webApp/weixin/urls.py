from django.urls import path
from webApp.weixin import views

app_name = 'wechat'

urlpatterns = [
    path('wechat/', views.wechat, name='wechat'),


]
