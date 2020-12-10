from django.urls import path
from webApp.collect import views

app_name = 'collect'

urlpatterns = [
    path('week_collect/', views.week_collect.as_view(), name='week_collect'),
    path('day_collect/', views.day_collect.as_view(), name='day_collect'),
    path('month_collect/', views.month_collect.as_view(), name='month_collect'),
    path('xiangqing/', views.xiangqing, name='xiangqing'),
    path('fenxiangqing/', views.fenxiangqing, name='fenxiangqing'),
    path('get_staffs/', views.get_staffs, name='get_staffs'),
    path('year_collect/', views.year_collect.as_view(), name='year_collect'),
    path('fenyear_collect/', views.fenyear_collect.as_view(), name='fenyear_collect'),
    path('fenmonth_collect/', views.fenmonth_collect.as_view(), name='fenmonth_collect'),
    path('technician_data/', views.Technician_data.as_view(), name='technician_data'),
    path('product_data/', views.Product_data.as_view(), name='product_data'),
]
