from django.urls import path
from webApp.mirror import views

app_name = 'mirror'

urlpatterns = [
    path('index/', views.index, name='index'),
]
