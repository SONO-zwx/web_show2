from django.urls import path
from webApp.login import views

app_name = 'index'

urlpatterns = [
    path('', views.log),
    path('log_in/', views.log_in, name='log_in'),
    path('nowshopname/', views.nowshopname, name='nowshopname'),
    path('exit_log/', views.exit_log, name='exit_log'),
    path('update_pwd/', views.update_pwd, name='update_pwd'),
]
