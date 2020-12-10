from django.urls import path
from webApp.exam import views

app_name = 'exam'

urlpatterns = [
    path('add_exam/', views.add_exam.as_view(), name='add_exam'),
    path('show_exam/', views.show_exam.as_view(), name='show_exam'),
    path('open_exam/', views.open_exam.as_view(), name='open_exam'),
    path('open_option/', views.open_option.as_view(), name='open_option'),
    path('add_topic/', views.add_topic.as_view(), name='add_topic'),
    path('show_topic/', views.show_topic.as_view(), name='show_topic'),
]
