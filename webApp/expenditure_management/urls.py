from django.urls import path
from . import views

app_name = 'expenditure_management'
urlpatterns = [
    path('addreceipts/', views.addreceipts.as_view(), name='addreceipts'),
    path('getaccount/', views.getaccount, name='getaccount'),
    path('twolimit/', views.twolimit, name='twolimit'),
    path('Back_goodsimg/', views.Back_goodsimg, name='Back_goodsimg'),
    path('Invoice_applyimg/', views.Invoice_applyimg, name='Invoice_applyimg'),
    path('stock_up/', views.Stock_up.as_view(), name='stock_up'),
    path('back_goods/', views.Back_goods.as_view(), name='back_goods'),
    path('invoice_apply/', views.Invoice_apply.as_view(), name='invoice_apply'),
    path('collection_voucher/', views.Collection_voucher.as_view(), name='collection_voucher'),
    path('bill_list/', views.Bill_list.as_view(), name='bill_list'),
    path('receiptshistory/', views.Receiptshistory.as_view(), name='receiptshistory'),
    path('onereceiptshistory/', views.Onereceiptshistory.as_view(), name='onereceiptshistory'),
    path('fourreceipts/', views.fourreceipts.as_view(), name='fourreceipts'),
    path('deleteimg/', views.deleteimg, name='deleteimg'),
    path('bill_detail/', views.Bill_detail.as_view(), name='bill_detail'),
    path('Collection_voucher_img/', views.Collection_voucher_img, name='collection_voucher_img'),
]
