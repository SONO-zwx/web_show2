import base64
import datetime
import time
from operator import itemgetter

from django.http import JsonResponse
from django.urls import reverse

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from webApp.financial_management.models import CertificateImg, Shopname, Receipts, Account, Dealproject, Users, \
    Newcategory, Commentreturn, CommentreturnDealproject, CommentreturnImg, Invoice, InvoiceDealproject, InvoiceImg, \
    Income, IncomeDealproject, IncomeImg, Waicaidealinfo, Waicaiinfo, Vinimg, Gongaccount, Kindsimg, Carinfoimg


# Create your views here.


class No_right(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='待月结').filter(
                jietype='月结').order_by(
                '-dates')
        else:
            info = Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='待月结').filter(
                jietype='月结').order_by('-dates')

        starttime = request.GET.get('starttime')
        endtime = request.GET.get('endtime')
        if starttime and endtime:
            if starttime != '':
                info = info.filter(dates__range=(starttime, endtime))

        shopname = request.GET.get('shopname', '请选择门店')
        if shopname != '请选择门店' and shopname != '':
            info = info.filter(shopname=shopname)

        types = request.GET.get('types', '请选择类型')
        if types != '请选择类型' and types != '':
            info = info.filter(types=types)

        project_name = request.GET.get('project_name')
        nowinfo = []

        for i in list(info.all().values()):
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()

            for dealinfo in dealprojectinfo:
                if dealinfo['status'] == '':
                    if not project_name:
                        dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                        dealinfo['price'] = dealinfo['price']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['status'] = i['paymenttyoe']
                        dealinfo['dates'] = i['dates']
                        if dealinfo['types'] in ['会员代付', '大客户代付']:
                            dealinfo['typeinfos'] = '应收'
                        else:
                            dealinfo['typeinfos'] = '支出'

                        dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0]['name']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '月结'

                        nowinfo.append(dealinfo)
                    else:
                        if dealinfo['types'] == project_name:
                            dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                            dealinfo['price'] = dealinfo['price']
                            dealinfo['shopname'] = i['shopname']
                            if dealinfo['types'] in ['会员代付', '大客户代付']:
                                dealinfo['typeinfos'] = '应收'
                            else:
                                dealinfo['typeinfos'] = '支出'

                            dealinfo['status'] = i['paymenttyoe']
                            dealinfo['dates'] = i['dates']
                            dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0]['name']
                            dealinfo['dealprojectid'] = dealinfo['id']
                            dealinfo['dealprojectstatus'] = '月结'

                            nowinfo.append(dealinfo)
                        else:
                            continue

        if types == '门店外采' or types == '请选择类型':
            if nowshopname != '总部':
                info = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status__in=['已完成', '待安装', '退货运费已完成']).filter(jiesuan_status__in=['供货商已对账', '门店已对账', ''])
            else:
                info = Waicaiinfo.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    status__in=['已完成', '待安装', '退货运费已完成']).filter(jiesuan_status__in=['供货商已对账', '门店已对账', ''])

            shopname = request.GET.get('shopname', '请选择门店')
            if shopname != '请选择门店':
                info = info.filter(shopname=shopname)

            starttime = request.GET.get('starttime')
            endtime = request.GET.get('endtime')
            if starttime and endtime:
                info = info.filter(tijiaodata__range=(starttime, endtime))

            for i in list(info.all().values()):
                dealprojectinfo = Waicaidealinfo.objects.filter(forid=i['id']).filter(status__in=['待安装', '已完成']).all().values()

                for dealinfo in dealprojectinfo:
                    if dealinfo['status'] in ['已完成', '待安装', '退货运费已完成'] or dealinfo['jiesuan_status'] in ['供货商已对账', '门店已对账', '']:

                        dealinfo['ertwo'] = dealinfo['productname']
                        dealinfo['dates'] = i['tijiaodata']
                        dealinfo['typeinfos'] = '支出'
                        dealinfo['price'] = dealinfo['manay']
                        if dealinfo['jiesuan_status'] == '':
                            dealinfo['status'] = '待月结'
                        else:
                            dealinfo['status'] = dealinfo['jiesuan_status']
                        dealinfo['zhidates'] = i['zhidates']
                        dealinfo['types'] = '门店外采'
                        dealinfo['companyinfo'] = Gongaccount.objects.filter(id=i['gongaccount']).all().values()[0][
                            'effect']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '外采'
                        dealinfo['id'] = i['id']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['ordernumber'] = i['ordernumber']
                        nowinfo.append(dealinfo)

        fourreceiptspage = request.GET.get('fourreceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        allnowinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)
        if types != '请选择类型':
            project_name = list(Newcategory.objects.filter(classname='支出单据').filter(one=types).all().values())
        else:
            project_name = None
        types = list(set([i['one'] for i in list(Newcategory.objects.filter(classname='支出单据').all().values())]))
        types.append('门店外采')
        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname,
                       'types': request.GET.get('types'), 'project_name': request.GET.get('project_name')}
        return render(request, 'financial_management/no_right.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'allnowinfo': allnowinfo,
                       'info': nowinfo, 'limits': request.session.get('limits'), 'types': types,
                       'project_name': project_name,
                       'search_info': search_info, })

    def post(self, request):
        orderid = request.POST.get('orderid')
        dealid = request.POST.get('dealid')
        status = request.POST.get('status')
        if status == '月结':
            Dealproject.objects.filter(id=dealid).update(status='已对账')
            info = len(Dealproject.objects.filter(receiptsid=orderid).filter(status='').all())
            if info == 0:
                Receipts.objects.filter(id=orderid).update(paymenttyoe='已对账',
                                                           zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))
        if status == '外采':
            if Waicaidealinfo.objects.filter(id=dealid).all().values()[0]['jiesuan_status'] in ['门店已对账', '']:
                Waicaidealinfo.objects.filter(id=dealid).update(jiesuan_status='门店已对账')
            else:
                Waicaidealinfo.objects.filter(id=dealid).update(jiesuan_status='已对账')

            info = len(Waicaidealinfo.objects.filter(forid=orderid).filter(status__in=['待安装', '已完成']).filter(jiesuan_status__in=['供货商已对账', '门店已对账', '']).all())
            if info == 0:
                Waicaiinfo.objects.filter(id=orderid).update(jiesuan_status='已对账',
                                                             zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))
        return redirect(reverse('financial_management:no_right'))


class To_be_invoiced(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Invoice.objects.filter(shopname=nowshopname).filter(status='已开').order_by(
                '-dates')
        else:
            info = Invoice.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='已开').order_by('-dates')
        shopname = request.GET.get('shopname', '')
        if shopname != '' and shopname != '请选择门店':
            info = info.filter(shopname=shopname)
        endtime = request.GET.get('endtime', '')
        types = request.GET.get('types', '')
        starttime = request.GET.get('starttime', '')
        if starttime != '' and endtime != '':
            info = info.filter(dates__in=datassplit(starttime, endtime))
        info = info.all().values()
        nowinfo = []
        for i in info:
            dealprojectinfo = InvoiceDealproject.objects.filter(for_id=i['id']).all().values()
            if types == '':
                i['ertwo'] = dealprojectinfo
                nowinfo.append(i)
            else:
                if dealprojectinfo[0]['invoice_type'] == types:
                    i['ertwo'] = dealprojectinfo
                    nowinfo.append(i)
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        search_info = {
            'starttime': starttime,
            'endtime': endtime,
            'types': types,
            'shopname': shopname
        }
        return render(request, 'financial_management/to_be_invoiced.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': nowinfo, 'limits': request.session.get('limits'), 'search_info': search_info})

    def post(self, request):
        return render(request, 'financial_management/to_be_invoiced.html')


class bohui_invoiced(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Invoice.objects.filter(shopname=nowshopname).filter(status='驳回').order_by(
                '-dates')
        else:
            info = Invoice.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='驳回').order_by('-dates')

        shopname = request.GET.get('shopname', '')
        if shopname != '' and shopname != '请选择门店':
            info = info.filter(shopname=shopname)
        endtime = request.GET.get('endtime', '')
        types = request.GET.get('types', '')
        starttime = request.GET.get('starttime', '')
        if starttime != '' and endtime != '':
            info = info.filter(dates__in=datassplit(starttime, endtime))
        info = info.all().values()

        nowinfo = []

        for i in info:
            dealprojectinfo = InvoiceDealproject.objects.filter(for_id=i['id']).all().values()
            if types == '':
                i['ertwo'] = dealprojectinfo
                nowinfo.append(i)
            else:
                if dealprojectinfo[0]['invoice_type'] == types:
                    i['ertwo'] = dealprojectinfo
                    nowinfo.append(i)
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        search_info = {
            'starttime': starttime,
            'endtime': endtime,
            'types': types,
            'shopname': shopname
        }
        return render(request, 'financial_management/bohui_invoiced.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': nowinfo, 'limits': request.session.get('limits'), 'search_info': search_info})


class Already_inoviced(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Invoice.objects.filter(shopname=nowshopname).filter(status='待处理').order_by(
                '-dates').all().values())
        else:
            info = list(Invoice.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待处理').order_by('-dates').all().values())

        nowinfo = []
        for i in info:
            dealprojectinfo = InvoiceDealproject.objects.filter(for_id=i['id']).all().values()
            i['ertwo'] = ' '.join(list(set([i['invoice_type'] for i in dealprojectinfo])))
            nowinfo.append(i)

        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)

        if threereceiptsid:

            receipts = Invoice.objects.filter(id=threereceiptsid).all().values()[0]
            receipts['dealproject'] = InvoiceDealproject.objects.filter(for_id=receipts['id']).all().values()
            receipts['photos'] = InvoiceImg.objects.filter(for_id=receipts['id']).all()

            return render(request, 'financial_management/already_invoiced.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/already_invoiced.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        status = info.get('status')
        remarks = info.get('remarks')
        infos = Invoice.objects.filter(id=receiptsid)
        if status == '已开发票':
            infos.update(finance=finance, status='已完成', approverinfo=remarks,
                         zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))
        else:
            infos.update(finance=finance, status=status, approverinfo=remarks,
                         zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))

        return redirect(reverse("financial_management:already_inoviced"))


class Already_right(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='已对账').filter(
                jietype='月结').order_by(
                '-dates')
        else:
            info = Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='已对账').filter(
                jietype='月结').order_by('-dates')

        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        if starttime != '' and endtime != '':
            info = info.filter(dates__range=(starttime, endtime))

        shopname = request.GET.get('shopname', '请选择门店')
        if shopname != '请选择门店':
            info = info.filter(shopname=shopname)
        types = request.GET.get('types', '请选择类型')
        if types != '请选择类型':
            info = info.filter(types=types)

        project_name = request.GET.get('project_name')
        nowinfo = []
        for i in list(info.all().values()):
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            for dealinfo in dealprojectinfo:
                if dealinfo['status'] == '已对账':
                    if not project_name:
                        dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                        dealinfo['price'] = dealinfo['price']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['status'] = i['paymenttyoe']
                        if dealinfo['types'] in ['会员代付', '大客户代付']:
                            dealinfo['typeinfos'] = '应收'
                        else:
                            dealinfo['typeinfos'] = '支出'
                        dealinfo['dates'] = i['dates']
                        dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0][
                            'name']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '月结'

                        nowinfo.append(dealinfo)
                    else:
                        if dealinfo['types'] == project_name:
                            dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                            dealinfo['price'] = dealinfo['price']
                            dealinfo['shopname'] = i['shopname']
                            dealinfo['status'] = i['paymenttyoe']
                            dealinfo['dates'] = i['dates']
                            if dealinfo['types'] in ['会员代付', '大客户代付']:
                                dealinfo['typeinfos'] = '应收'
                            else:
                                dealinfo['typeinfos'] = '支出'
                            dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0]['name']
                            dealinfo['dealprojectid'] = dealinfo['id']
                            dealinfo['dealprojectstatus'] = '月结'

                            nowinfo.append(dealinfo)
                        else:
                            continue

        if types == '门店外采' or types == '请选择类型':
            if nowshopname != '总部':
                info = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status__in=['已完成', '待安装']).filter(jiesuan_status='已对账')
            else:
                info = Waicaiinfo.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    status__in=['已完成', '待安装']).filter(jiesuan_status='已对账')

            shopname = request.GET.get('shopname', '请选择门店')
            if shopname != '请选择门店':
                info = info.filter(shopname=shopname)

            starttime = request.GET.get('starttime')
            endtime = request.GET.get('endtime')
            if starttime and endtime:
                info = info.filter(tijiaodata__range=(starttime, endtime))

            for i in list(info.all().values()):
                dealprojectinfo = Waicaidealinfo.objects.filter(forid=i['id']).all().values()
                for dealinfo in dealprojectinfo:
                    if dealinfo['jiesuan_status'] in ['已对账', '已打款']:
                        dealinfo['ertwo'] = dealinfo['productname']
                        dealinfo['dates'] = i['tijiaodata']
                        dealinfo['status'] = i['jiesuan_status']
                        dealinfo['price'] = dealinfo['manay']
                        dealinfo['zhidates'] = i['zhidates']
                        dealinfo['types'] = '门店外采'
                        dealinfo['companyinfo'] = Gongaccount.objects.filter(id=i['gongaccount']).all().values()[0][
                            'effect']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '外采'
                        dealinfo['id'] = i['id']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['ordernumber'] = i['ordernumber']
                        nowinfo.append(dealinfo)
        fourreceiptspage = request.GET.get('fourreceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        allnowinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)
        if types != '请选择类型':
            project_name = list(Newcategory.objects.filter(classname='支出单据').filter(one=types).all().values())
        else:
            project_name = None
        types = list(set([i['one'] for i in list(Newcategory.objects.filter(classname='支出单据').all().values())]))

        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname,
                       'types': request.GET.get('types'), 'project_name': request.GET.get('project_name')}
        return render(request, 'financial_management/already_right.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'allnowinfo': allnowinfo,
                       'info': nowinfo, 'limits': request.session.get('limits'), 'types': types,
                       'project_name': project_name,
                       'search_info': search_info, })

    def post(self, request):
        orderid = request.POST.get('orderid')
        dealid = request.POST.get('dealid')
        status = request.POST.get('status')
        if status == '月结':
            Dealproject.objects.filter(id=dealid).update(status='已完成')
            info = len(Dealproject.objects.filter(receiptsid=orderid).filter(status__in=['已对账', '']).all())
            if info == 0:
                Receipts.objects.filter(id=orderid).update(paymenttyoe='已完成',
                                                           zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))

        if status == '外采':
            Waicaidealinfo.objects.filter(id=dealid).update(jiesuan_status='结算已完成')
            info = len(Waicaidealinfo.objects.filter(forid=orderid).filter(status__in=['待安装', '已完成']).filter(jiesuan_status__in=['已对账']).all())
            if info == 0:
                Waicaiinfo.objects.filter(id=orderid).update(jiesuan_status='结算已完成',
                                                             zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))
        return redirect(reverse('financial_management:already_right'))


class Already_pay(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='已完成').filter(
                jietype='月结').order_by(
                '-dates')
        else:
            info = Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='已完成').filter(
                jietype='月结').order_by('-dates')

        starttime = request.GET.get('starttime')
        endtime = request.GET.get('endtime')
        if starttime and endtime:
            info = info.filter(dates__range=(starttime, endtime))

        shopname = request.GET.get('shopname', '请选择门店')
        if shopname != '请选择门店':
            info = info.filter(shopname=shopname)
        types = request.GET.get('types', '请选择类型')
        if types != '请选择类型':
            info = info.filter(types=types)

        project_name = request.GET.get('project_name')
        nowinfo = []
        for i in list(info.all().values()):
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            for dealinfo in dealprojectinfo:
                if dealinfo['status'] == '已完成':
                    if not project_name:
                        dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                        dealinfo['price'] = dealinfo['price']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['status'] = i['paymenttyoe']
                        dealinfo['dates'] = i['dates']
                        if dealinfo['types'] in ['会员代付', '大客户代付']:
                            dealinfo['typeinfos'] = '应收'
                        else:
                            dealinfo['typeinfos'] = '支出'
                        dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0]['name']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '月结'
                        dealinfo['zhistatus'] = '应付'
                        nowinfo.append(dealinfo)
                    else:
                        if dealinfo['types'] == project_name:
                            dealinfo['ertwo'] = dealinfo['types'] + ':' + dealinfo['projectname']
                            dealinfo['price'] = dealinfo['price']
                            dealinfo['shopname'] = i['shopname']
                            dealinfo['status'] = i['paymenttyoe']
                            dealinfo['dates'] = i['dates']
                            if dealinfo['types'] in ['会员代付', '大客户代付']:
                                dealinfo['typeinfos'] = '应收'
                            else:
                                dealinfo['typeinfos'] = '支出'
                            dealinfo['dealprojectstatus'] = '月结'
                            dealinfo['companyinfo'] = Account.objects.filter(id=i['paymentaccout']).all().values()[0]['name']
                            dealinfo['dealprojectid'] = dealinfo['id']
                            dealinfo['zhistatus'] = '应付'
                            nowinfo.append(dealinfo)
                        else:
                            continue

        if types == '门店外采' or types == '请选择类型':
            if nowshopname != '总部':
                info = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status__in=['待安装', '已完成']).filter(jiesuan_status='结算已完成')
            else:
                info = Waicaiinfo.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    status__in=['待安装', '已完成']).filter(jiesuan_status='结算已完成')

            shopname = request.GET.get('shopname', '请选择门店')
            if shopname != '请选择门店':
                info = info.filter(shopname=shopname)

            starttime = request.GET.get('starttime')
            endtime = request.GET.get('endtime')
            if starttime and endtime:
                info = info.filter(tijiaodata__range=(starttime, endtime))

            for i in list(info.all().values()):
                dealprojectinfo = Waicaidealinfo.objects.filter(forid=i['id']).all().values()
                for dealinfo in dealprojectinfo:
                    if dealinfo['jiesuan_status'] == '结算已完成':
                        dealinfo['ertwo'] = dealinfo['productname']
                        dealinfo['dates'] = i['tijiaodata']
                        dealinfo['price'] = dealinfo['manay']
                        if dealinfo['jiesuan_status'] == '':
                            dealinfo['status'] = '待月结'
                        else:
                            dealinfo['status'] = dealinfo['jiesuan_status']
                        dealinfo['zhidates'] = i['zhidates']
                        dealinfo['types'] = '门店外采'
                        dealinfo['companyinfo'] = Gongaccount.objects.filter(id=i['gongaccount']).all().values()[0]['effect']
                        dealinfo['dealprojectid'] = dealinfo['id']
                        dealinfo['dealprojectstatus'] = '外采'
                        dealinfo['id'] = i['id']
                        dealinfo['shopname'] = i['shopname']
                        dealinfo['ordernumber'] = i['ordernumber']
                        dealinfo['zhistatus'] = '应付'

                        nowinfo.append(dealinfo)
        fivereceiptspage = request.GET.get('fivereceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        allnowinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fivereceiptspage)
        if types != '请选择类型':
            project_name = list(Newcategory.objects.filter(classname='支出单据').filter(one=types).all().values())
        else:
            project_name = None
        types = list(set([i['one'] for i in list(Newcategory.objects.filter(classname='支出单据').all().values())]))

        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname,
                       'types': request.GET.get('types'), 'project_name': request.GET.get('project_name')}
        return render(request, 'financial_management/already_pay.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'allnowinfo': allnowinfo,
                       'info': nowinfo, 'limits': request.session.get('limits'), 'types': types,
                       'project_name': project_name,
                       'search_info': search_info, })

    def post(self, request):
        return render(request, 'financial_management/already_pay.html')


class expenditure(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='待打款').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='待打款').order_by('-dates').all().values())

        new_info = []
        for i in info:
            if i['types'] == '外采' or i['types'] == '外采退换货':
                continue
            new_info.append(i)
        info = new_info

        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)
        zhiaccount = Account.objects.filter(isuse=1).filter(types='支出').all().values()

        if threereceiptsid:

            receipts = Receipts.objects.filter(id=threereceiptsid).all().values()[0]
            try:
                receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            except:
                receipts['paymentaccout'] = ''
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            if receipts['remarks']:
                try:
                    receipts['remarks'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2],
                                            'limits': i.split('**-**')[3]} for i in receipts['remarks'].split('**--**')]
                except:
                    receipts['remarks'] = []
            else:
                receipts['remarks'] = []
            nowtime = str(datetime.date.today().strftime("%Y-%m-%d"))
            return render(request, 'financial_management/caiwuexpenditure.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'nowtime': nowtime,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo, 'zhiaccount': zhiaccount,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/caiwuexpenditure.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'zhiaccount': zhiaccount, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        jietype = info.get('jietype')
        receiptsid = info.get('receiptsid')
        paymenttyoe = info.get('paymenttyoe')
        zhidates = info.get('zhidates')
        myImg = eval(info.get('myImg'))
        zhichupaymentaccout = info.get('zhichupaymentaccout')
        infos = Receipts.objects.filter(id=receiptsid)
        if paymenttyoe == '已打款':
            if str(infos.all().values()[0]['iszi']) == '1':
                infos.update(finance=finance, jietype=jietype, paymenttyoe='资料补充', zhidates=zhidates,
                             zhichupaymentaccout=zhichupaymentaccout)
            else:
                infos.update(finance=finance, jietype=jietype, paymenttyoe='已完成', zhidates=zhidates,
                             zhichupaymentaccout=zhichupaymentaccout)
        else:
            infos.update(finance=finance, jietype=jietype, paymenttyoe=paymenttyoe, zhidates=zhidates,
                         zhichupaymentaccout=zhichupaymentaccout)
        for i in myImg:
            imginfo = base64_to_jpg(i, 'photos/' + str(request.session.get('id')))

            img = CertificateImg(img_url=imginfo, for_id=receiptsid, onloadinfo=3)
            img.save()
        return redirect(reverse("financial_management:expenditure"))


def base64_to_jpg(bs64, nameinfo):
    imgname = '/home/zwx/code/web_show2/media/' + str(nameinfo) + str(time.time()).replace('.', '') + '.jpg'
    if ',' in bs64:
        imgData = base64.b64decode(bs64.split(',')[-1])
        leniyimg = open(imgname, 'wb')
        leniyimg.write(imgData)
        leniyimg.close()
    else:
        print(bs64)
        imgData = base64.b64decode(bs64)
        leniyimg = open(imgname, 'wb')
        leniyimg.write(imgData)
        leniyimg.close()
    imgname = imgname.replace('/home/zwx/code/web_show2/media/', '')
    return imgname


class fivereceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='资料审批').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='资料审批').order_by('-dates').all().values())
        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)
        fivereceiptspage = request.GET.get('fivereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fivereceiptspage)
        fivereceiptsid = request.GET.get('fivereceiptsid', None)

        if fivereceiptsid:

            receipts = Receipts.objects.filter(id=fivereceiptsid).all().values()[0]
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            if receipts['remarks']:
                receipts['remarks'] = [
                    {'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for i in
                    receipts['remarks'].split('**--**')]
            else:
                receipts['remarks'] = []
            return render(request, 'financial_management/fivereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/fivereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        paymenttyoe = request.POST.get('paymenttyoe')
        receiptsid = request.POST.get('receiptsid')
        erremarks = request.POST.get('erremarks')
        infos = Receipts.objects.filter(id=receiptsid)
        if paymenttyoe == '资料审批通过':
            paymenttyoe = '已完成'
        infos.update(paymenttyoe=paymenttyoe, erremarks=erremarks)

        return redirect(reverse("financial_management:fivereceipts"))


class collection_voucher(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Income.objects.filter(shopname=nowshopname).filter(status='待核实').order_by(
                '-dates').all().values())
        else:
            info = list(Income.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待核实').order_by('-dates').all().values())

        nowinfo = []
        for i in info:
            dealprojectinfo = IncomeDealproject.objects.filter(for_id=i['id']).all().values()
            account = Account.objects.filter(id=i['payment_account']).all().values()[0]
            i['payment_account'] = account['name'] + '---' + account['account']
            i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
            nowinfo.append(i)
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)

        if threereceiptsid:

            receipts = Income.objects.filter(id=threereceiptsid).all().values()[0]
            receipts['dealproject'] = IncomeDealproject.objects.filter(for_id=receipts['id']).all().values()
            receipts['photos'] = IncomeImg.objects.filter(for_id=receipts['id']).all()
            account = Account.objects.filter(id=receipts['payment_account']).all().values()[0]
            receipts['payment_account'] = account['name'] + '---' + account['account']
            if receipts['approverinfo']:
                try:
                    receipts['approverinfo'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2],
                                                 'limits': i.split('**-**')[3]} for i in
                                                receipts['approverinfo'].split('**--**')]
                except:
                    receipts['approverinfo'] = []
            else:
                receipts['approverinfo'] = []
            return render(request, 'financial_management/caiwucollection_voucher.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/caiwucollection_voucher.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        status = info.get('status')
        zhidates = info.get('zhidates')
        infos = Income.objects.filter(id=receiptsid)
        if status == '通过审核':
            infos.update(finance=finance, status='已完成', zhidates=zhidates)
        else:
            infos.update(finance=finance, status=status, zhidates=zhidates)

        return redirect(reverse("financial_management:collection_voucher"))


class back_goods(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        if nowshopname != '总部':
            info = Commentreturn.objects.filter(shopname=nowshopname).filter(status='待退货').filter(
                order_type__in=['途虎退货', '运营退货']).order_by('-dates')
        else:
            info = Commentreturn.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                order_type__in=['途虎退货', '运营退货']).filter(status='待退货').order_by('-dates')

        if starttime != '' and endtime != '':
            info.filter(dates__in=datassplit(starttime, endtime))
        info = list(info.all().values())
        nowinfo = info
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)

        if threereceiptsid:

            receipts = Commentreturn.objects.filter(id=threereceiptsid).all().values()[0]
            receipts['dealproject'] = CommentreturnDealproject.objects.filter(for_id=receipts['id']).all().values()

            receipts['photos'] = CommentreturnImg.objects.filter(for_id=receipts['id']).all()
            if receipts['approverinfo']:
                try:
                    receipts['approverinfo'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2],
                                                 'limits': i.split('**-**')[3]} for i in
                                                receipts['approverinfo'].split('**--**')]
                except:
                    receipts['approverinfo'] = []
            else:
                receipts['approverinfo'] = []
            return render(request, 'financial_management/caiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo,
                           'limits': request.session.get('limits'), 'starttime': starttime, 'endtime': endtime})
        else:
            return render(request, 'financial_management/caiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits'), 'starttime': starttime,
                           'endtime': endtime})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        status = info.get('status')
        remarks = info.get('remarks')
        infos = Commentreturn.objects.filter(id=receiptsid)
        if status == '通过':
            infos.update(finance=finance, status='已完成', remarks=remarks)
        else:
            infos.update(finance=finance, status=status, remarks=remarks)

        return redirect(reverse("financial_management:back_goods"))


def datassplit(StartTime, EndTime):
    dt = datetime.datetime.strptime(StartTime, "%Y-%m-%d")
    end_dt = datetime.datetime.strptime(EndTime, "%Y-%m-%d")

    dates = []

    while dt <= end_dt:
        dates.append(dt.strftime("%Y-%m-%d"))
        if dt == end_dt:
            return dates
        dt = dt + datetime.timedelta(days=1)


class waicaiback_goods(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = Commentreturn.objects.filter(shopname=nowshopname).filter(status='待退货').filter(
                order_type__in=['外采退货']).order_by(
                '-dates')
        else:
            info = Commentreturn.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                order_type__in=['外采退货']).filter(
                status='待退货').order_by('-dates')

        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        if starttime != '' and endtime != '':
            info.filter(dates__in=datassplit(starttime, endtime))
        info = list(info.all().values())
        nowinfo = info
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)

        if threereceiptsid:

            receipts = Commentreturn.objects.filter(id=threereceiptsid).all().values()[0]
            receipts['dealproject'] = CommentreturnDealproject.objects.filter(for_id=receipts['id']).all().values()
            if receipts['approverinfo']:
                try:
                    receipts['approverinfo'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2],
                                                 'limits': i.split('**-**')[3]} for i in
                                                receipts['approverinfo'].split('**--**')]
                except:
                    receipts['approverinfo'] = []
            else:
                receipts['approverinfo'] = []
            if receipts['order_type'] == '外采退货':
                waicaiid = int(receipts['dealproject'][0]['order_num'].replace('外采订单:', ''))
                waicaiid = Waicaidealinfo.objects.filter(id=waicaiid).all().values()[0]['forid']
                offshoreinfo = Waicaiinfo.objects.filter(id=waicaiid).all().values()[0]
                gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
                offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                    'types']
                offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
                offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
                offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
                offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(
                    forid=offshoreinfo['id']).filter(status='待退货').all().values()
                return render(request, 'financial_management/waicaicaiwuback_goods.html',
                              {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                               'info': nowinfo, 'offshoreinfo': offshoreinfo, 'receipts': receipts,
                               'userinfo': userinfo, 'limits': request.session.get('limits')})
            receipts['photos'] = CommentreturnImg.objects.filter(for_id=receipts['id']).all()

            return render(request, 'financial_management/waicaicaiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/waicaicaiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits'), 'endtime': endtime,
                           'starttime': starttime})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        status = info.get('status')
        remarks = info.get('remarks')
        infos = Commentreturn.objects.filter(id=receiptsid)
        if status == '供货商原因退货':
            infos.update(finance=finance, status='已完成', remarks='供货商原因退货:' + str(remarks))
            receipts = int(CommentreturnDealproject.objects.filter(for_id=receiptsid).all().values()[0]['order_num'].replace(
                    '外采订单:', ''))
            info = Waicaidealinfo.objects.filter(id=receipts).all().values()[0]
            Waicaidealinfo.objects.filter(id=receipts).update(status='已退货')
            Waicaiinfo.objects.filter(id=info['forid']).update(status='退货完成')
            maininfo = Waicaiinfo.objects.filter(id=info['forid']).all().values()[0]
            waicaiinfo = Waicaiinfo(
                shopname=maininfo['shopname'],
                gongaccount=maininfo['gongaccount'],
                ordernumber=maininfo['ordernumber'],
                brand=maininfo['brand'],
                motorcycle=maininfo['motorcycle'],
                model=maininfo['model'],
                number=maininfo['number'],
                forid=maininfo['forid'],
                allprice=0 - maininfo['sansong'],
                status='退货运费已完成',
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")),
                jiesuan_status=''
            )
            waicaiinfo.save()
            Waicaidealinfo(
                brand='退货运费',
                motorcycle='退货运费',
                productname='退货运费',
                model='供货商原因：闪送费用 ￥' + str(maininfo['sansong']),
                number=1,
                unit=0 - maininfo['sansong'],
                status='退货运费已完成',
                manay=0 - maininfo['sansong'],
                forid=waicaiinfo.id,
                jiesuan_status=''
            ).save()
        else:
            infos.update(finance=finance, status='已完成', remarks='门店原因退货:' + str(remarks))
            receipts = int(CommentreturnDealproject.objects.filter(for_id=receiptsid).all().values()[0]['order_num'].replace(
                    '外采订单:', ''))
            info = Waicaidealinfo.objects.filter(id=receipts).all().values()[0]
            Waicaidealinfo.objects.filter(id=receipts).update(status='已退货')
            Waicaiinfo.objects.filter(id=info['forid']).update(status='退货完成')
            maininfo = Waicaiinfo.objects.filter(id=info['forid']).all().values()[0]
            waicaiinfo = Waicaiinfo(
                shopname=maininfo['shopname'],
                gongaccount=maininfo['gongaccount'],
                ordernumber=maininfo['ordernumber'],
                brand=maininfo['brand'],
                motorcycle=maininfo['motorcycle'],
                model=maininfo['model'],
                number=maininfo['number'],
                forid=maininfo['forid'],
                allprice=0 + maininfo['yunfei'],
                status='退货运费已完成',
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")),
                jiesuan_status=''
            )
            waicaiinfo.save()
            Waicaidealinfo(
                brand='退货运费',
                motorcycle='退货运费',
                productname='退货运费',
                model='门店原因：垫付运费 ￥' + str(maininfo['yunfei']),
                number=1,
                unit=0 + maininfo['yunfei'],
                status='退货运费已完成',
                manay=0 + maininfo['yunfei'],
                forid=waicaiinfo.id,
                jiesuan_status=''
            ).save()
        return redirect(reverse("financial_management:waicaiback_goods"))


class waicai_goods(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Commentreturn.objects.filter(shopname=nowshopname).filter(status='待退货').order_by(
                '-dates').all().values())
        else:
            info = list(Commentreturn.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待退货').order_by('-dates').all().values())

        nowinfo = info
        threereceiptspage = request.GET.get('threereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(threereceiptspage)
        threereceiptsid = request.GET.get('threereceiptsid', None)

        if threereceiptsid:

            receipts = Commentreturn.objects.filter(id=threereceiptsid).all().values()[0]
            receipts['dealproject'] = CommentreturnDealproject.objects.filter(for_id=receipts['id']).all().values()
            receipts['photos'] = CommentreturnImg.objects.filter(for_id=receipts['id']).all()
            if receipts['approverinfo']:
                try:
                    receipts['approverinfo'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2],
                                                 'limits': i.split('**-**')[3]} for i in
                                                receipts['approverinfo'].split('**--**')]
                except:
                    receipts['approverinfo'] = []
            else:
                receipts['approverinfo'] = []
            return render(request, 'financial_management/caiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'financial_management/caiwuback_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        status = info.get('status')
        remarks = info.get('remarks')
        infos = Commentreturn.objects.filter(id=receiptsid)
        if status == '通过':
            infos.update(finance=finance, status='已完成', remarks=remarks)
        else:
            infos.update(finance=finance, status=status, remarks=remarks)

        return redirect(reverse("financial_management:back_goods"))


def search_erinfo(request):
    info = request.POST.get('types')
    info = list(Newcategory.objects.filter(classname='支出单据').filter(one=info).all().values())
    return JsonResponse({'info': info})
