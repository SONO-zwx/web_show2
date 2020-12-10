import base64
import json
import time
from operator import itemgetter

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
import datetime

# Create your views here.
from webApp.expenditure_management.models import CertificateImg, Shopname, Receipts, Account, Dealproject, Users, \
    Newcategory, Commentreturn, CommentreturnDealproject, CommentreturnImg, Invoice, InvoiceDealproject, InvoiceImg, \
    Income, IncomeDealproject, IncomeImg, Xiaoxi, UserRight


class Stock_up(APIView):
    def get(self, request):
        receiptsimg = request.FILES.getlist('receiptsimg', None)

        if receiptsimg:
            for imgs in receiptsimg:
                img = CertificateImg(img_url=imgs, for_id=request.POST.get('for_id'))
                img.save()
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receipts = Receipts.objects.filter(id=549).all().values()[0]
        receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
        receipts['zhichupaymentaccout'] = Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
        receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
        receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()

        limits = Users.objects.filter(id=id).all().values()[0]
        limits['submit'] = limits['submit'].split('；')
        onesubmit = []
        for i in limits['submit']:
            info = Newcategory.objects.filter(superior=superior).filter(two=i).all().values()
            for x in info:
                if x['one'] in onesubmit:
                    continue
                else:
                    onesubmit.append(x['one'])
        limits['onesubmit'] = onesubmit
        account = Account.objects.filter(isuse=1).filter(shopname=nowshopname).filter(types='收款').all().values()
        return render(request, 'expenditure_management/stock_up.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'receipts': receipts,
                       'limitinfo': limits, 'account': account, 'limits': request.session.get('limits')})

    def post(self, request):
        return render(request, 'expenditure_management/stock_up.html')


class Back_goods(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        if ShopName == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
        else:
            ShopNames = Shopname.objects.filter(superior=superior).filter(shopname=ShopName).all().values()

        today = datetime.date.today().strftime("%Y-%m-%d")
        return render(request, 'expenditure_management/back_goods.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'today': today, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.session.get('id')
        datas = request.POST.get('datas')
        shopname = request.POST.get('shopname')
        consignee = request.POST.get('consignee')
        operator = request.POST.get('operator')
        company = request.POST.get('company')
        people = request.POST.get('people')
        license_plate = request.POST.get('license_plate')
        dates = request.POST.get('dates')
        submitremark = request.POST.get('submitremark')
        allprice = request.POST.get('allprice')
        order_type = request.POST.get('order_type')
        receiptsimg = eval(request.POST.get('myImg'))

        info = Commentreturn(
            shopname=shopname,
            consignee=consignee,
            operator=operator,
            company=company,
            people=people,
            license_plate=license_plate,
            dates=dates,
            submitremark=submitremark,
            allprice=allprice,
            status='待审批',
            order_type=order_type
        )
        info.save()

        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas if i != '']

        for i in datas:
            dealinfo = CommentreturnDealproject(
                order_num=i[0],
                product_name=i[1],
                count=i[2],
                amount=i[3],
                reason=i[4],
                for_id=info.id,
                order_type='退货管理'
            )
            dealinfo.save()
        category = Newcategory.objects.filter(one=order_type,two=order_type, classname='退货管理', superior='北京索诺汽车服务有限公司').all().values()[0]['id']
        chuliren = UserRight.objects.filter(tablename='Newcategory', proinfo=category, lastuser_right=0).all().values()[0]
        try:
            nextchuliren = UserRight.objects.filter(lastuser_right=chuliren['lastuser_right']).all().values()[0]
        except:
            category = Newcategory.objects.filter(one='退货', two='退货', classname='财务处理', superior='北京索诺汽车服务有限公司').all().values()[0]['id']
            nextchuliren = UserRight.objects.filter(tablename='Newcategory', proinfo=category, lastuser_right=0).all().values()[0]

        xiaoxi = Xiaoxi(
            biaoming='commentreturn',
            tableid=info.id,
            chuliren=chuliren['conductor'],
            nextchuliren=nextchuliren['conductor'],
            isok=0,
            ischaoshi=0
        )
        xiaoxi.save()
        for i in receiptsimg:
            imginfo = base64_to_jpg(i, 'CommentreturnImg/' + str(id))
            img = CommentreturnImg(img_url=imginfo, for_id=info.id)
            img.save()

        return JsonResponse({'id': info.id})


def Back_goodsimg(request):
    receiptsimg = request.FILES.getlist('receiptsimg', None)
    if receiptsimg:
        for imgs in receiptsimg:
            img = CommentreturnImg(img_url=imgs, for_id=request.POST.get('for_id'))
            img.save()
    return redirect(reverse("expenditure_management:back_goods"))


class Invoice_apply(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        if ShopName == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
        else:
            ShopNames = Shopname.objects.filter(superior=superior).filter(shopname=ShopName).all().values()

        today = datetime.date.today().strftime("%Y-%m-%d")
        return render(request, 'expenditure_management/invioce_apply.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'today': today, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.session.get('id')
        datas = request.POST.get('datas')
        dates = request.POST.get('dates')
        shopname = request.POST.get('shopname')
        agent = request.POST.get('agent')
        collection_method = request.POST.get('collection_method')
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        remark = request.POST.get('remark')
        receiptsimg = eval(request.POST.get('myImg'))

        info = Invoice(
            dates=dates,
            shopname=shopname,
            agent=agent,
            collection_method=collection_method,
            customer_name=customer_name,
            phone=phone,
            remark=remark,
            status='待处理',
            order_type='发票申请'
        )
        info.save()
        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas if i != '']
        for i in datas:
            infodeal = InvoiceDealproject(
                company_name=i[0],
                duty_paragraph=i[1],
                invoice_type=i[2],
                invoice_amount=i[3],
                site=i[4],
                for_id=info.id,
                order_type='发票申请'
            )
            infodeal.save()
        category = Newcategory.objects.filter(one='财务',two='财务', classname='财务处理', superior='北京索诺汽车服务有限公司').all().values()[0]['id']
        chuliren = UserRight.objects.filter(tablename='Newcategory', proinfo=category, lastuser_right=0).all().values()[0]
        xiaoxi = Xiaoxi(
            biaoming='invoice',
            tableid=info.id,
            chuliren=chuliren['conductor'],
            isok=0,
            ischaoshi=0
        )
        xiaoxi.save()
        for i in receiptsimg:
            imginfo = base64_to_jpg(i, 'InvoiceImg/' + str(id))
            img = InvoiceImg(img_url=imginfo, for_id=info.id)
            img.save()
        return JsonResponse({'id': info.id})


def Invoice_applyimg(request):
    receiptsimg = request.FILES.getlist('receiptsimg', None)
    if receiptsimg:
        for imgs in receiptsimg:
            img = InvoiceImg(img_url=imgs, for_id=request.POST.get('for_id'))
            img.save()
    return redirect(reverse("expenditure_management:invoice_apply"))


class Collection_voucher(APIView):
    def get(self, request):
        receiptsimg = request.FILES.getlist('receiptsimg', None)

        if receiptsimg:
            for imgs in receiptsimg:
                img = CertificateImg(img_url=imgs, for_id=request.POST.get('for_id'))
                img.save()
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        if ShopName == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
        else:
            ShopNames = Shopname.objects.filter(superior=superior).filter(shopname=ShopName).all().values()

        account = Account.objects.filter(isuse=1).filter(types='收款').all().values()
        info = Account.objects.filter(isuse=1).all().values()
        return render(request, 'expenditure_management/collection_voucher.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'account': account, 'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.session.get('id')
        datas = request.POST.get('datas')
        dates = request.POST.get('dates')
        shopname = request.POST.get('shopname')
        payment_account = request.POST.get('payment_account')
        payment_term = request.POST.get('payment_term')
        allprice = request.POST.get('allprice')
        submitremark = request.POST.get('submitremark')
        receiptsimg = eval(request.POST.get('myImg'))
        info = Income.objects.create(dates=dates, shopname=shopname, payment_account=payment_account,
                                     payment_term=payment_term, allprice=allprice, submitremark=submitremark,
                                     status='待审批', order_type='收入凭证')
        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas if i != '']
        for i in datas:
            IncomeDealproject.objects.create(project_name=i[0], explains=i[1], amount=i[2], for_id=info.id,
                                             order_type='收入凭证')

        for i in receiptsimg:
            imginfo = base64_to_jpg(i, 'IncomeImg/' + str(id))
            img = IncomeImg(img_url=imginfo, for_id=info.id)
            img.save()
        return JsonResponse({'data': info.id})


def Collection_voucher_img(request):
    for_id = request.POST.get('for_id')
    file = request.FILES.getlist('receiptsimg')
    for i in file:
        IncomeImg.objects.create(img_url=i, for_id=for_id)
    return redirect('expenditure_management:collection_voucher')


def deleteimg(request):
    id = request.POST.get('id')
    CertificateImg.objects.filter(id=id).delete()
    return redirect('expenditure_management:fourreceipts')


class fourreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(userid=request.session.get('id'))
                        .filter(paymenttyoe='资料补充').order_by('dates').all().values())
        else:
            info = list(Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='资料补充').filter(userid=request.session.get('id')).order_by('dates').all().values())
        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='资料审批驳回').order_by(
                'dates').all().values())
        else:
            info = list(Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='资料审批驳回').order_by('dates').all().values())
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)

        fourreceiptspage = request.GET.get('fourreceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)
        fourreceiptsid = request.GET.get('fourreceiptsid', None)

        if fourreceiptsid:

            receipts = Receipts.objects.filter(id=fourreceiptsid).all().values()[0]
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).filter(onloadinfo=1).all()
            receipts['new_photos'] = CertificateImg.objects.filter(for_id=receipts['id']).filter(onloadinfo=2).all()
            if receipts['remarks']:
                receipts['remarks'] = [
                    {'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for i in
                    receipts['remarks'].split('**--**')]
            else:
                receipts['remarks'] = []

            return render(request, 'expenditure_management/fourreceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'expenditure_management/fourreceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        receiptsimg = eval(request.POST.get('myImg'))
        receiptsid = request.POST.get('receiptsid')
        id = request.session.get('id')

        for i in receiptsimg:
            imginfo = base64_to_jpg(i, 'photos/' + str(id))
            img = CertificateImg(img_url=imginfo, for_id=receiptsid, onloadinfo=2)
            img.save()

        infos = Receipts.objects.filter(id=receiptsid)
        infos.update(paymenttyoe='资料审批')

        return redirect(reverse("expenditure_management:fourreceipts"))


class Bill_list(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        one_types = request.GET.get('one_types', '')
        status = request.GET.get('status', '')
        types = request.GET.get('types', '')
        shopname = request.GET.get('shopname', '')
        search = request.GET.get('search_form', '')
        nowinfo = []

        if types == '支出' or types == '':

            if nowshopname != '总部':
                info = Receipts.objects.filter(shopname=nowshopname).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by('-id').order_by(
                    'dates').all().values()
            else:
                info = Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by('dates').all().values()
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(types=one_types)
            if status != '':
                info = info.filter(paymenttyoe=status)
            result = []
            if search != '':
                for i in info.filter(types__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remark__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(responsibleperson__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remarks__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            projectname__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            remark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            types__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            new_info = []
            for i in result:
                if i['types'] == '外采' or i['types'] == '外采退换货':
                    continue
                new_info.append(i)
            info = new_info

            for i in info:
                dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
                i['dates'] = i['dates'].strftime("%Y-%m-%d")
                i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['projectname'] for i in dealprojectinfo]))
                i['type'] = '支出'
                nowinfo.append(i)

        if types == '收入' or types == '':

            if nowshopname == '总部':
                info = Income.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by(
                    '-id').all().values()
            else:
                info = Income.objects.filter(shopname=nowshopname).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by(
                    '-id').all().values()
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Income.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Income.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            explains__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = IncomeDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['project_name'] for i in dealprojectinfo]))
                i['type'] = '收入'
                nowinfo.append(i)

        if types == '退货' or types == '':

            if nowshopname == '总部':
                info = Commentreturn.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by(
                    '-id').all().values()
            else:
                info = Commentreturn.objects.filter(shopname=nowshopname).filter(
                    dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by(
                    '-id').all().values()
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            reason__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = CommentreturnDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['product_name'] for i in dealprojectinfo]))
                i['type'] = '退货'
                nowinfo.append(i)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        fourreceiptspage = request.GET.get('fourreceiptspage', 1)
        allinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)
        if types == '支出' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True)))
            statusinfo = list(
                set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True)))
        elif types == '收入' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True)))
            statusinfo = list(set(Income.objects.values_list('status', flat=True)))
        else:
            one_typesinfo = []
            statusinfo = []

        searchinfo = {
            'one_types': one_types,
            'one_typesinfo': one_typesinfo,
            'status': status,
            'statusinfo': statusinfo,
            'types': types,
            'shopname': shopname,
            'search': search,
        }
        return render(request, 'expenditure_management/bill_list.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'searchinfo': searchinfo,
                       'allinfo': allinfo,
                       'nowshopname': nowshopname, 'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        types = request.POST.get('types')
        one_types = ''
        status = ''
        if types == '支出' or types == '':
            one_types = set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True))
            status = set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True))
        elif types == '收入' or types == '':
            one_types = set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True))
            status = set(Income.objects.values_list('status', flat=True))
        return JsonResponse({'one_types': list(one_types), 'status': list(status)}, safe=True)


def datassplit(StartTime, EndTime):
    dt = datetime.datetime.strptime(StartTime, "%Y-%m-%d")
    end_dt = datetime.datetime.strptime(EndTime, "%Y-%m-%d")

    dates = []

    while dt <= end_dt:
        dates.append(dt.strftime("%Y-%m-%d"))
        if dt == end_dt:
            return dates
        dt = dt + datetime.timedelta(days=1)


class Receiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        zhistarttime = request.GET.get('zhistarttime', '')
        zhiendtime = request.GET.get('zhiendtime', '')
        one_types = request.GET.get('one_types', '')
        status = request.GET.get('status', '')
        types = request.GET.get('types', '')
        shopname = request.GET.get('shopname', '')
        search = request.GET.get('search_form', '')
        nowinfo = []
        if types == '支出' or types == '':
            if nowshopname != '总部':
                info = Receipts.objects.filter(shopname=nowshopname).order_by('-id').order_by('dates').all().values()
            else:
                info = Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).order_by(
                    'dates').all().values()
            if starttime != '' and endtime != '':
                info = info.filter(dates__range=(starttime, endtime))
            if zhistarttime != '' and zhiendtime != '':
                info = info.filter(zhidates__range=(zhistarttime, zhiendtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(types=one_types)
            if status != '':
                info = info.filter(paymenttyoe=status)
            result = []
            if search != '':
                for i in info.filter(types__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remark__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(responsibleperson__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remarks__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            projectname__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            remark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            types__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info

            new_info = []
            for i in result:
                if i['types'] == '外采' or i['types'] == '外采退换货':
                    continue
                new_info.append(i)
            info = new_info
            for i in info:
                dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
                i['dates'] = i['dates'].strftime("%Y-%m-%d")
                if i['zhidates']:
                    i['zhidates'] = i['zhidates'].strftime("%Y-%m-%d")
                else:
                    i['zhidates'] = ''
                i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['projectname'] for i in dealprojectinfo]))
                i['type'] = '支出'
                nowinfo.append(i)

        if types == '收入' or types == '':
            info = Income.objects.order_by(
                '-id').all().values()
            if starttime != '' and endtime != '':
                info = info.filter(dates__in=datassplit(starttime, endtime))
            if zhistarttime != '' and zhiendtime != '':
                info = info.filter(zhidates__in=datassplit(zhistarttime, zhiendtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Income.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Income.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            explains__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = IncomeDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                if i['zhidates']:
                    i['zhidates'] = i['zhidates']
                else:
                    i['zhidates'] = ''
                i['erproject'] = ';'.join(list([i['project_name'] for i in dealprojectinfo]))
                i['type'] = '收入'
                nowinfo.append(i)

        if types == '退货' or types == '':
            info = Commentreturn.objects.order_by('-id').all().values()
            if starttime != '' and endtime != '':
                info = info.filter(dates__in=datassplit(starttime, endtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            reason__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = CommentreturnDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['product_name'] for i in dealprojectinfo]))
                i['type'] = '退货'
                nowinfo.append(i)

        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)

        allinfo = nowinfo
        fourreceiptspage = request.GET.get('fourreceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)

        if types == '支出' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True)))
            statusinfo = list(
                set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True)))
        elif types == '收入' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True)))
            statusinfo = list(set(Income.objects.values_list('status', flat=True)))
        else:
            one_typesinfo = []
            statusinfo = []

        searchinfo = {
            'one_types': one_types,
            'one_typesinfo': one_typesinfo,
            'status': status,
            'starttime': starttime,
            'endtime': endtime,
            'statusinfo': statusinfo,
            'types': types,
            'shopname': shopname,
            'search': search,
            'zhiendtime': zhiendtime,
            'zhistarttime': zhistarttime,
        }

        return render(request, 'expenditure_management/receiptshistory.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': nowinfo, 'searchinfo': searchinfo, 'allinfo': allinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        types = request.POST.get('types')
        one_types = ''
        status = ''
        if types == '支出' or types == '':
            one_types = set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True))
            status = set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True))
        elif types == '收入' or types == '':
            one_types = set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True))
            status = set(Income.objects.values_list('status', flat=True))
        return JsonResponse({'one_types': list(one_types), 'status': list(status)}, safe=True)


class Onereceiptshistory(APIView):

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
        one_types = request.GET.get('one_types', '')
        status = request.GET.get('status', '')
        types = request.GET.get('types', '')
        shopname = request.GET.get('shopname', '')
        search = request.GET.get('search_form', '')
        nowinfo = []
        if types == '支出' or types == '':
            if nowshopname != '总部':
                info = Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='驳回').order_by('-id').order_by(
                    'dates').all().values()
            else:
                info = Receipts.objects.filter(paymenttyoe='驳回').filter(
                    paymenttyoe='驳回').order_by('dates').all().values()

            if starttime != '' and endtime != '':
                info = info.filter(dates__range=(starttime, endtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(types=one_types)
            if status != '':
                info = info.filter(paymenttyoe=status)
            result = []
            if search != '':
                for i in info.filter(types__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remark__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(responsibleperson__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.filter(remarks__contains=search).all().values():
                    if i in result:
                        continue
                    else:
                        result.append(i)
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            projectname__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            remark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Dealproject.objects.filter(receiptsid=i['id']).filter(
                            types__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            new_info = []
            for i in result:
                if i['types'] == '外采' or i['types'] == '外采退换货':
                    continue
                new_info.append(i)
            info = new_info

            for i in info:
                dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
                i['dates'] = i['dates'].strftime("%Y-%m-%d")
                i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['projectname'] for i in dealprojectinfo]))
                i['type'] = '支出'
                nowinfo.append(i)

        if types == '收入' or types == '':
            info = Income.objects.filter(status='驳回').order_by(
                '-id').all().values()

            if starttime != '' and endtime != '':
                info = info.filter(dates__in=datassplit(starttime, endtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Income.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Income.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(IncomeDealproject.objects.filter(for_id=i['id']).filter(
                            explains__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = IncomeDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['project_name'] for i in dealprojectinfo]))
                i['type'] = '收入'
                nowinfo.append(i)

        if types == '退货' or types == '':
            info = Commentreturn.objects.filter(status='驳回').order_by(
                '-id').all().values()
            if starttime != '' and endtime != '':
                info = info.filter(dates__in=datassplit(starttime, endtime))
            if shopname != '':
                info = info.filter(shopname=shopname)
            if one_types != '':
                info = info.filter(order_type=one_types)
            if status != '':
                info = info.filter(status=status)
            result = []
            if search != '':
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(submitremark__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(Commentreturn.objects.filter(approverinfo__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            project_name__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
                for i in info.all().values():
                    if len(CommentreturnDealproject.objects.filter(for_id=i['id']).filter(
                            reason__contains=search).all().values()) != 0:
                        result.append(i)
                    else:
                        continue
            else:
                result = info
            for i in result:
                dealprojectinfo = CommentreturnDealproject.objects.filter(for_id=i['id']).all().values()
                i['ertwo'] = ';'.join(list(set([i['order_type'] for i in dealprojectinfo])))
                i['erproject'] = ';'.join(list([i['product_name'] for i in dealprojectinfo]))
                i['type'] = '退货'
                nowinfo.append(i)

        fourreceiptspage = request.GET.get('fourreceiptspage', 1)

        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        # nowinfo = sorted(nowinfo, key=lambda e: [i['dates'] for i in e.values()][0], reverse=True)
        allinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fourreceiptspage)
        if types == '支出' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True)))
            statusinfo = list(
                set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True)))
        elif types == '收入' or types == '':
            one_typesinfo = list(set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True)))
            statusinfo = list(set(Income.objects.values_list('status', flat=True)))
        else:
            one_typesinfo = []
            statusinfo = []

        searchinfo = {
            'one_types': one_types,
            'one_typesinfo': one_typesinfo,
            'status': status,
            'starttime': starttime,
            'endtime': endtime,
            'statusinfo': statusinfo,
            'types': types,
            'shopname': shopname,
            'search': search,
        }
        return render(request, 'expenditure_management/onereceiptshistory.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'allinfo': allinfo,
                       'info': nowinfo, 'searchinfo': searchinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        types = request.POST.get('types')
        one_types = ''
        status = ''
        if types == '支出' or types == '':
            one_types = set(Newcategory.objects.filter(classname='支出单据').values_list('one', flat=True))
            status = set(Receipts.objects.exclude(types__startswith='外').values_list('paymenttyoe', flat=True))
        elif types == '收入' or types == '':
            one_types = set(Newcategory.objects.filter(classname='收入单据').values_list('one', flat=True))
            status = set(Income.objects.values_list('status', flat=True))
        return JsonResponse({'one_types': list(one_types), 'status': list(status)}, safe=True)


class Bill_detail(APIView):

    def get(self, request):
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        id = request.GET.get('fourreceiptsid')
        types = request.GET.get('types')
        fourreceiptspage = request.GET.get('fourreceiptspage')
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        urls = str(request.GET.get('url')).replace('\'', '')

        if types == '支出' or types == '':
            receipts = Receipts.objects.filter(id=id).all().values()[0]
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
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
            return render(request, 'expenditure_management/bill_detail.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits'),
                           'urls': urls})
        if types == '收入':
            receipts = Income.objects.filter(id=id).all().values()[0]
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
            return render(request, 'expenditure_management/bill_detail.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'zhireceipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits'),
                           'url': urls})
        if types == '退货' or types == '':
            receipts = Commentreturn.objects.filter(id=id).all().values()[0]
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
            return render(request, 'expenditure_management/bill_detail.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'tuizhireceipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits'),
                           'url': urls})

    def post(self, request):
        return render(request, 'expenditure_management/bill_detail.html')


class addreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        if ShopName == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
        else:
            ShopNames = Shopname.objects.filter(superior=superior).filter(shopname=ShopName).all().values()
        limits = Users.objects.filter(id=id).all().values()[0]
        onesubmit = []
        info = Newcategory.objects.filter(superior=superior).filter(classname='支出单据').all().values()
        notinfo = Newcategory.objects.filter(superior=superior).filter(classname='支出单据').filter(
            one__startswith='外采').all().values()

        for x in info:
            if x['one'] in onesubmit or x in notinfo:
                continue
            else:
                onesubmit.append(x['one'])
        limits['onesubmit'] = onesubmit
        account = Account.objects.filter(isuse=1).filter(types='收款').all().values()
        today = datetime.date.today().strftime("%Y-%m-%d")

        return render(request, 'expenditure_management/addreceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'limitinfo': limits, 'account': account, 'today': today,
                       'limits': request.session.get('limits')})

    def post(self, request):
        id = request.session.get('id')
        date = request.POST
        datas = date.get('datas')
        shopname = date.get('shopname')
        types = date.get('types')
        yuzhi = date.get('yuzhi')
        iszi = date.get('iszi')
        responsibleperson = date.get('responsibleperson')
        dates = date.get('dates')
        paymentaccout = date.get('paymentaccout')
        remark = date.get('remark')
        allpriceinfo = date.get('allpriceinfo')
        receiptsimg = eval(date.get('myImg'))
        receiptsimg1 = eval(date.get('myImg1'))

        if iszi == 'false':
            iszi = '0'
        else:
            iszi = '1'
        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas if i != '']
        info = Receipts(
            shopname=shopname,
            types=types,
            yuzhi=yuzhi,
            paymenttyoe='待审批',
            responsibleperson=responsibleperson,
            dates=dates,
            iszi=iszi,
            paymentaccout=paymentaccout,
            remark=remark,
            allprice=allpriceinfo,
            userid=id
        )
        info.save()

        for i in datas:
            dealproject = Dealproject(
                projectname=i[1],
                remark=i[2],
                price=i[3],
                issure=0,
                receiptsid=info.id,
                types=i[0],
                status=''
            )
            dealproject.save()
        for i in receiptsimg:
            imginfo = base64_to_jpg(i, 'photos/' + str(id))
            img = CertificateImg(img_url=imginfo, for_id=info.id, onloadinfo=1)
            img.save()

        category = Newcategory.objects.filter(one=types,two=datas[0][0], classname='支出单据', superior='北京索诺汽车服务有限公司').all().values()[0]['id']
        chuliren = UserRight.objects.filter(tablename='Newcategory', proinfo=category, lastuser_right=0).all().values()[0]
        try:
            nextchuliren = UserRight.objects.filter(lastuser_right=chuliren['lastuser_right']).all().values()[0]
        except:
            category = Newcategory.objects.filter(one='财务', two='财务', classname='财务处理', superior='北京索诺汽车服务有限公司').all().values()[0]['id']
            nextchuliren = UserRight.objects.filter(tablename='Newcategory', proinfo=category, lastuser_right=0).all().values()[0]

        xiaoxi = Xiaoxi(
            biaoming='receipts',
            tableid=info.id,
            chuliren=chuliren['conductor'],
            nextchuliren=nextchuliren['conductor'],
            isok=0,
            ischaoshi=0
        )
        xiaoxi.save()

        isfa = 0
        for i in receiptsimg1:
            isfa = 1
            imginfo = base64_to_jpg(i, 'photos/' + str(id))
            img = CertificateImg(img_url=imginfo, for_id=info.id, onloadinfo=5)
            img.save()
        if isfa == 1:
            info = Invoice(
                dates=dates,
                shopname=shopname,
                agent=responsibleperson,
                collection_method='自取',
                customer_name=responsibleperson,
                phone='手机号',
                remark='支出单据应收发票',
                status='待处理',
                order_type='发票申请'
            )
            info.save()

            infodeal = InvoiceDealproject(
                company_name='发票单位',
                duty_paragraph='税号',
                invoice_type='应收',
                invoice_amount=allpriceinfo,
                site='地址',
                for_id=info.id,
                order_type='发票申请'
            )
            infodeal.save()
            for i in receiptsimg1:
                imginfo = base64_to_jpg(i, 'InvoiceImg/' + str(id))
                img = InvoiceImg(img_url=imginfo, for_id=info.id)
                img.save()

        return JsonResponse({'id': info.id})


def twolimit(request):
    types = request.POST.get('types')
    id = request.session.get('id')
    superior = request.session.get('superior')
    info = Newcategory.objects.filter(one=types).filter(superior=superior).filter(classname='支出单据').all().values()
    twosubmit = list(set([i['two'] for i in info]))

    return JsonResponse({'twosubmit': twosubmit})


def getaccount(request):
    info = Account.objects.filter(shopname=request.POST.get('shopname')).filter(isuse=1).all().values()
    return JsonResponse({'account': [[i['id'], i['account'] + '---' + i['name']] for i in info]})


def base64_to_jpg(bs64, nameinfo):
    imgname = '/home/zwx/code/web_show2/media/' + str(nameinfo) + str(time.time()).replace('.', '') + '.jpg'
    if ',' in bs64:
        imgData = base64.b64decode(bs64.split(',')[-1])
        leniyimg = open(imgname, 'wb')
        leniyimg.write(imgData)
        leniyimg.close()
    else:
        imgData = base64.b64decode(bs64)
        leniyimg = open(imgname, 'wb')
        leniyimg.write(imgData)
        leniyimg.close()
    imgname = imgname.replace('/home/zwx/code/web_show2/media/', '')
    return imgname
