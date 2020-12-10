from django.urls import path
from . import views
app_name = 'financial_management'

urlpatterns = [
    path('no_right/', views.No_right.as_view(), name='no_right'),
    path('expenditure/', views.expenditure.as_view(), name='expenditure'),
    path('fivereceipts/', views.fivereceipts.as_view(), name='fivereceipts'),
    path('back_goods/', views.back_goods.as_view(), name='back_goods'),
    path('waicaiback_goods/', views.waicaiback_goods.as_view(), name='waicaiback_goods'),
    path('search_erinfo/', views.search_erinfo, name='search_erinfo'),
    path('waicai_goods/', views.waicai_goods.as_view(), name='waicai_goods'),
    path('collection_voucher/', views.collection_voucher.as_view(), name='collection_voucher'),
    path('to_be_invoiced/', views.To_be_invoiced.as_view(), name='to_be_invoiced'),
    path('bohui_invoiced/', views.bohui_invoiced.as_view(), name='bohui_invoiced'),
    path('already_inoviced/', views.Already_inoviced.as_view(), name='already_inoviced'),
    path('already_right/', views.Already_right.as_view(), name='already_right'),
    path('already_pay/', views.Already_pay.as_view(), name='already_pay'),
]
