from django.urls import path
from webApp.approval_administration import views

app_name = 'approval_administration'

urlpatterns = [
    path('receiptclass/', views.receiptclass.as_view(), name='receiptclass'),
    path('addreceiptclass/', views.addreceiptclass.as_view(), name='addreceiptclass'),
    path('updatereceiptclass/', views.updatereceiptclass.as_view(), name='updatereceiptclass'),
    path('shanchureceiptclass/', views.shanchureceiptclass, name='shanchureceiptclass'),
    path('xiugaireceiptclass/', views.xiugaireceiptclass, name='xiugaireceiptclass'),
    path('shourureceiptclass/', views.shourureceiptclass.as_view(), name='shourureceiptclass'),
    path('shouruaddreceiptclass/', views.shouruaddreceiptclass.as_view(), name='shouruaddreceiptclass'),
    path('shouruupdatereceiptclass/', views.shouruupdatereceiptclass.as_view(), name='shouruupdatereceiptclass'),
    path('shourushanchureceiptclass/', views.shourushanchureceiptclass, name='shourushanchureceiptclass'),
    path('shouruxiugaireceiptclass/', views.shouruxiugaireceiptclass, name='shouruxiugaireceiptclass'),
    path('tuihuoreceiptclass/', views.tuihuoreceiptclass.as_view(), name='tuihuoreceiptclass'),
    path('tuihuoaddreceiptclass/', views.tuihuoaddreceiptclass.as_view(), name='tuihuoaddreceiptclass'),
    path('tuihuoupdatereceiptclass/', views.tuihuoupdatereceiptclass.as_view(), name='tuihuoupdatereceiptclass'),
    path('tuihuoshanchureceiptclass/', views.tuihuoshanchureceiptclass, name='tuihuoshanchureceiptclass'),
    path('tuihuoxiugaireceiptclass/', views.tuihuoxiugaireceiptclass, name='tuihuoxiugaireceiptclass'),
    path('expenditure/', views.Expenditure.as_view(), name='expenditure'),
    path('back_goods/', views.Back_goods.as_view(), name='back_goods'),
    path('collection_voucher/', views.Collection_voucher.as_view(), name='collection_voucher'),
]
