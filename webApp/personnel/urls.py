from django.urls import path
from webApp.personnel import views

app_name = 'personnel'

urlpatterns = [

    path('personnel/', views.personnel.as_view(), name='personnel'),
    path('performance/', views.performance.as_view(), name='performance'),
    path('withhold/', views.withhold.as_view(), name='withhold'),
    path('shenwithhold/', views.shenwithhold.as_view(), name='shenwithhold'),
    path('shenwithholdtong/', views.shenwithholdtong, name='shenwithholdtong'),
    path('shenwithholdbo/', views.shenwithholdbo, name='shenwithholdbo'),
    path('addpersonnel/', views.addpersonnel.as_view(), name='addpersonnel'),
    path('addperformance/', views.addperformance.as_view(), name='addperformance'),
    path('addwithhold/', views.addwithhold.as_view(), name='addwithhold'),
    path('seestaffs/', views.seestaffs, name='seestaffs'),
    path('seejixiao/', views.seejixiao, name='seejixiao'),
    path('seeparticulars/', views.seeparticulars, name='seeparticulars'),
]
