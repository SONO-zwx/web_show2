from django.urls import path
from webApp.monitor import views

app_name = 'monitor'

urlpatterns = [
    path('monitor_list/', views.Monitor_list.as_view(), name='monitor_list'),
    path('monitor_history/', views.monitor_history.as_view(), name='monitor_history'),
    path('monitor_detail/', views.Monitor_detail.as_view(), name='monitor_detail'),
    path('handle_pic/', views.Handle_pic.as_view(), name='handle_pic'),
    path('seeperformance/', views.seeperformance, name='seeperformance'),
    path('seefen/', views.seefen, name='seefen'),
]