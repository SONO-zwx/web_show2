from django.urls import path
from webApp.testsinfo import views

app_name = 'testsinfo'

urlpatterns = [
    path('testinfo/', views.testinfo.as_view(), name='testinfo'),
]
