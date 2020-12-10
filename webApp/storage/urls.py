from django.urls import path
from . import views
app_name = 'storage'

urlpatterns = [
    path('stock_apply', views.Stock_apply.as_view(), name='stock_apply'),
    path('out_apply', views.Out_apply.as_view(), name='out_apply'),
    path('stock_lists', views.Stock_lists.as_view(), name='stock_lists'),
    path('inventory', views.Inventory.as_view(), name='inventory'),
]
