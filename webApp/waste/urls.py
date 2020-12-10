from django.urls import path
from webApp.waste import views

app_name = 'waste'

urlpatterns = [
    path('wasteinfo/', views.wasteinfo.as_view(), name='wasteinfo'),
    path('wastetradinghistory/', views.wastetradinghistory.as_view(), name='wastetradinghistory'),
    path('wastetradingok/', views.wastetradingok.as_view(), name='wastetradingok'),
    path('searchinfo/', views.searchinfo, name='searchinfo'),
    path('wastetrading/', views.wastetrading.as_view(), name='wastetrading'),
    path('wastecontractor/', views.wastecontractor.as_view(), name='wastecontractor'),
    path('wasteproject/', views.wasteproject.as_view(), name='wasteproject'),
    path('addwastecontractor/', views.addwastecontractor.as_view(), name='addwastecontractor'),
    path('wastecontractorinfo/', views.wastecontractorinfo.as_view(), name='wastecontractorinfo'),
    path('addwasteproject/', views.addwasteproject.as_view(), name='addwasteproject'),
    path('wasteproinfo/', views.wasteproinfo, name='wasteproinfo'),
    path('addreceiptsimg/', views.addreceiptsimg, name='addreceiptsimg'),
    path('wastediff/', views.wastediff.as_view(), name='wastediff'),
    path('searchtime/', views.searchtime, name='searchtime'),

]
