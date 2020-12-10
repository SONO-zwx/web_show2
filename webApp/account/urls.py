from django.urls import path
from webApp.account import views

app_name = 'account'

urlpatterns = [
    path('addaccount/', views.addaccount.as_view(), name='addaccount'),
    path('accountlimits/', views.accountlimits.as_view(), name='accountlimits'),
    path('isaccount/', views.isaccount, name='isaccount'),
    path('delaccount/', views.delaccount, name='delaccount'),
    path('alertaccountlimit/', views.alertaccountlimit, name='alertaccountlimit'),
]