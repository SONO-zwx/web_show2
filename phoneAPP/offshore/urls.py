from django.urls import path
from phoneAPP.offshore import views

app_name = 'offshore'

urlpatterns = [
    path('offshore_index/', views.offshore_index.as_view(), name='offshore_index'),
    path('add_offshore/', views.add_offshore.as_view(), name='add_offshore'),
    path('gongzuotai/', views.gongzuotai.as_view(), name='gongzuotai'),
    path('offshore_one/', views.offshore_one.as_view(), name='offshore_one'),
    path('offshore_two/', views.offshore_two.as_view(), name='offshore_two'),
    path('offshore_three/', views.offshore_three.as_view(), name='offshore_three'),
    path('offshore_four/', views.offshore_four.as_view(), name='offshore_four'),
    path('offshore_five/', views.offshore_five.as_view(), name='offshore_five'),
    path('quxiaodingdan/', views.quxiaodingdan.as_view(), name='quxiaodingdan'),
    path('offshore_six/', views.offshore_six.as_view(), name='offshore_six'),
    path('offshore_seven/', views.offshore_seven.as_view(), name='offshore_seven'),
    path('offshore_eight/', views.offshore_eight.as_view(), name='offshore_eight'),
    path('offshore_nine/', views.offshore_nine.as_view(), name='offshore_nine'),
]
