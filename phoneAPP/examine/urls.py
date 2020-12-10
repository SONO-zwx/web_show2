from django.urls import path
from phoneAPP.examine import views

app_name = 'examine'

urlpatterns = [
    path('examine_index/', views.examine_index.as_view(), name='examine_index'),
    path('examine_two/', views.examine_two.as_view(), name='examine_two'),
    path('examine_three/', views.examine_three.as_view(), name='examine_three'),
    path('examine_four/', views.examine_four.as_view(), name='examine_four'),
    path('examine_five/', views.examine_five.as_view(), name='examine_five'),
    path('examine_six/', views.examine_six.as_view(), name='examine_six'),
    path('examine_seven/', views.examine_seven.as_view(), name='examine_seven'),

]
