import datetime
import time
import warnings
from operator import itemgetter

from decimal import Decimal
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from webApp.certificate.models import Account, Gongaccount, Shopname, Receipts, Dealproject, CertificateImg, \
    UserRight, Users, Newcategory, Waicaidealinfo, Waicaiinfo, Carinfoimg, Vinimg, Kindsimg, Commentreturn, \
    CommentreturnDealproject, CommentreturnImg, WechatMessage
from django.core.paginator import Paginator


# 日常账号显示
class m_account(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        accountpage = int(request.GET.get('accountpage', 1))
        ShopNames = Shopname.objects.filter(superior=superior)
        if nowshopname == '总部':
            account = Account.objects.filter(shopname__in=ShopNames.all().values_list('shopname')).all().order_by(
                'id').all()
        else:
            account = Account.objects.filter(shopname=nowshopname).all().order_by('id').all()
        accountpaginator = Paginator(account, 10)
        account = accountpaginator.page(accountpage)

        return render(request, 'certificate/../../templates/account/m_account.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'account': account, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


# 供货商账号显示
class m_gongaccount(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        gongaccountpage = int(request.GET.get('gongaccountpage', 1))
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().order_by('id').all()
        gongaccountpaginator = Paginator(gongaccount, 10)
        gongaccount = gongaccountpaginator.page(gongaccountpage)
        return render(request, 'certificate/../../templates/account/m_gongaccount.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


# 添加日常账号
class add_account(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        id = request.GET.get('id')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if id:
            info = Account.objects.filter(id=id).all().values()[0]
        else:
            info = '无'
        return render(request, 'account/add_account.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        datainfo = request.POST
        id = datainfo.get('id')
        if id:
            info = Account.objects.filter(id=id)
            info.update(
                account=datainfo.get('account'),
                name=datainfo.get('name'),
                shopname=datainfo.get('shopname'),
                types=datainfo.get('types'),
                isuse=datainfo.get('isuse')
            )
        else:
            info = Account(
                account=datainfo.get('account'),
                name=datainfo.get('name'),
                shopname=datainfo.get('shopname'),
                types=datainfo.get('types'),
                isuse=datainfo.get('isuse')
            )
            info.save()

        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        accountpage = int(request.GET.get('accountpage', 1))
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        account = Account.objects.filter(shopname=nowshopname).all().order_by('id')
        accountpaginator = Paginator(account, 10)
        account = accountpaginator.page(accountpage)

        return render(request, 'certificate/../../templates/account/m_account.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'account': account, 'limits': request.session.get('limits')})


# 添加供货商账号
class add_gongaccount(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        id = request.GET.get('id')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if id:
            info = Gongaccount.objects.filter(id=id).all().values()[0]
        else:
            info = '无'
        return render(request, 'certificate/../../templates/account/add_gongaccount.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': info, 'superior': superior, 'limits': request.session.get('limits')})

    def post(self, request):
        datainfo = request.POST
        id = datainfo.get('id')
        usernameid = datainfo.get('usernameid')
        username = datainfo.get('username')
        password = datainfo.get('password')
        if id:
            info = Users.objects.filter(id=usernameid)
            info.update(
                username=username,
                password=password
            )
            info = Gongaccount.objects.filter(id=id)
            info.update(
                account=datainfo.get('gongaccount'),
                name=datainfo.get('gongname'),
                shopname=datainfo.get('gongshopname'),
                effect=datainfo.get('gongeffect'),
                types=datainfo.get('gongtypes'),
                isuse=datainfo.get('isuse')
            )
        else:
            info = Users(
                username=username,
                name=datainfo.get('gongname'),
                password=password,
                isuse=1,
                shopname='供应商',
                superior=datainfo.get('gongeffect'),
                limits=''
            )
            info.save()
            info = Gongaccount(
                account=datainfo.get('gongaccount'),
                name=datainfo.get('gongname'),
                shopname=datainfo.get('gongshopname'),
                effect=datainfo.get('gongeffect'),
                types=datainfo.get('gongtypes'),
                isuse=datainfo.get('isuse'),
                usernameid=info.id
            )
            info.save()

        return redirect(reverse('certificate:m_gongaccount'))


# 获取账号信息
def get_m_account(request):
    account = request.POST.get('accountid', '无')
    gongaccount = request.POST.get('gongaccountid', '无')
    if account != '无':
        account = Account.objects.filter(id=account).all().values()[0]
        gongaccount = '无'
    elif gongaccount != '无':
        gongaccount = Gongaccount.objects.filter(id=gongaccount).all().values()[0]
        userinfo = Users.objects.filter(id=gongaccount['usernameid']).all().values()[0]
        gongaccount['username'] = userinfo['username']
        gongaccount['password'] = userinfo['password']
        account = '无'
    return JsonResponse({'account': account, 'gongaccount': gongaccount})


def isuse_m_account(request):
    account = request.POST.get('accountid', '无')
    gongaccount = request.POST.get('gongaccountid', '无')
    isuse = request.POST.get('isuse')
    if account != '无':
        account = Account.objects.filter(id=account)
        account.update(isuse=isuse)
        gongaccount = '无'
    elif gongaccount != '无':
        gongaccount = Gongaccount.objects.filter(id=gongaccount)
        gongaccount.update(isuse=isuse)
        account = '无'
    return JsonResponse({'account': account, 'gongaccount': gongaccount})


def amendlimit(request):
    userid = request.POST.get('userid')
    nowstatus = request.POST.get('nowstatus')
    values = request.POST.get('values')
    field = request.POST.get('field')
    if nowstatus != 'selected':
        if field == 'submit':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['submit']
            userinfo = userinfo.split('；')
            userinfo.append(values)
            info.update(submit="；".join(userinfo))
        elif field == 'oneapprover':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['oneapprover']
            userinfo = userinfo.split('；')
            userinfo.append(values)
            info.update(oneapprover="；".join(userinfo))
        elif field == 'twoapprover':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['twoapprover']
            userinfo = userinfo.split('；')
            userinfo.append(values)
            info.update(twoapprover="；".join(userinfo))
    else:
        if field == 'submit':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['submit']
            userinfo = userinfo.split('；')
            userinfo.remove(values)
            info.update(submit="；".join(userinfo))
        elif field == 'oneapprover':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['oneapprover']
            userinfo = userinfo.split('；')
            userinfo.remove(values)
            info.update(oneapprover="；".join(userinfo))
        elif field == 'twoapprover':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['twoapprover']
            userinfo = userinfo.split('；')
            userinfo.remove(values)
            info.update(twoapprover="；".join(userinfo))

    return JsonResponse({})


def twolimit(request):
    types = request.POST.get('types')
    id = request.session.get('id')
    limits = Users.objects.filter(id=id).all().values()[0]
    limits['submit'] = limits['submit'].split('；')
    info = Newcategory.objects.filter(one=types).all().values()
    limitsinfo = set([i['two'] for i in info])
    twosubmit = list(limitsinfo.intersection(set(limits['submit'])))

    return JsonResponse({'twosubmit': twosubmit})


# 单据流转
class addreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        limits = Users.objects.filter(id=id).all().values()[0]
        limits['submit'] = limits['submit'].split('；')
        onesubmit = []
        for i in limits['submit']:
            info = Newcategory.objects.filter(superior=superior).filter(two=i).all().values()
            notinfo = Newcategory.objects.filter(superior=superior).filter(two=i).filter(
                one__startswith='外采').all().values()

            for x in info:
                if x['one'] in onesubmit or x in notinfo:
                    continue
                else:
                    onesubmit.append(x['one'])
        limits['onesubmit'] = onesubmit
        account = Account.objects.filter(isuse=1).filter(shopname=nowshopname).filter(types='收款').all().values()
        return render(request, 'certificate/addreceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'limits': limits, 'account': account, 'limits': request.session.get('limits')})

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
        if iszi == 'false':
            iszi = '0'
        else:
            iszi = '1'
        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas]
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

        for i in datas[:-1]:
            dealproject = Dealproject(
                projectname=i[1],
                remark=i[2],
                price=i[3],
                issure=0,
                receiptsid=info.id,
                types=i[0],
            )
            dealproject.save()
        return JsonResponse({'id': info.id})


class onereceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='待审批').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(
                paymenttyoe='待审批').order_by('-dates').all().values())
        oneapprover = Users.objects.filter(id=id).all().values()[0]['oneapprover']
        oneapprover = oneapprover.split('；')
        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            dealprojectinfos = [i['types'] for i in dealprojectinfo if i['types'] in oneapprover]
            if len(dealprojectinfos) == 0:
                continue
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)
        onereceiptspage = request.GET.get('onereceiptspage', 1)

        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(onereceiptspage)
        onereceiptsid = request.GET.get('onereceiptsid', None)
        if onereceiptsid:

            receipts = Receipts.objects.filter(id=onereceiptsid).all().values()[0]
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/onereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/onereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        receiptsid = info.get('receiptsid')
        generalmanager = info.get('generalmanager')
        paymenttyoe = info.get('paymenttyoe')
        remarks = info.get('remarks')

        info = Receipts.objects.filter(id=receiptsid)
        if paymenttyoe == '驳回':
            info.update(generalmanager=generalmanager, paymenttyoe=paymenttyoe, remarks=remarks)

        if paymenttyoe == '通过审批':
            ertwo = Dealproject.objects.filter(receiptsid=info.all().values()[0]['id']).all().values()[0]['types']
            isapprover = \
                Newcategory.objects.filter(one=info.all().values()[0]['types']).filter(two=ertwo).all().values()[0][
                    'isapprover']
            if isapprover == '1':
                paymenttyoe = '待确认'
            else:
                paymenttyoe = '待打款'
            info.update(generalmanager=generalmanager, paymenttyoe=paymenttyoe, remarks=remarks)
        return redirect(reverse("certificate:onereceipts"))


class tworeceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='待确认').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(
                paymenttyoe='待确认').order_by('-dates').all().values())
        twoapprover = Users.objects.filter(id=id).all().values()[0]['twoapprover']
        twoapprover = twoapprover.split('；')
        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()
            dealprojectinfos = [i['types'] for i in dealprojectinfo if i['types'] in twoapprover]
            if len(dealprojectinfos) == 0:
                continue
            i['ertwo'] = ';'.join(list(set([i['types'] for i in dealprojectinfo])))
            nowinfo.append(i)
        tworeceiptspage = request.GET.get('tworeceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(tworeceiptspage)
        tworeceiptsid = request.GET.get('tworeceiptsid', None)
        if tworeceiptsid:

            receipts = Receipts.objects.filter(id=tworeceiptsid).all().values()[0]
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/tworeceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/tworeceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        receiptsid = info.get('receiptsid')
        ergeneralmanager = info.get('ergeneralmanager')
        paymenttyoe = info.get('paymenttyoe')
        erremarks = info.get('erremarks')
        infos = Receipts.objects.filter(id=receiptsid)
        if paymenttyoe == '驳回':
            infos.update(ergeneralmanager=ergeneralmanager, paymenttyoe=paymenttyoe, erremarks=erremarks)

        if paymenttyoe == '通过审批':
            paymenttyoe = '待打款'
            infos.update(ergeneralmanager=ergeneralmanager, paymenttyoe=paymenttyoe, erremarks=erremarks)
        return redirect(reverse("certificate:tworeceipts"))


class receiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        info = list(Receipts.objects.order_by('-id').all().values())
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
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/receiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/receiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class onereceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='驳回').order_by('-id').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(
                paymenttyoe='驳回').order_by('-dates').all().values())
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
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/onereceiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/onereceiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class tworeceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        info = list(Receipts.objects.filter(dates=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by(
            '-id').all().values())
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
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/tworeceiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/tworeceiptshistory.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class threereceipts(APIView):

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
            info = list(Receipts.objects.filter(
                paymenttyoe='待打款').order_by('-dates').all().values())
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
            receipts['paymentaccout'] = Account.objects.filter(id=receipts['paymentaccout']).all().values()[0]
            try:
                receipts['zhichupaymentaccout'] = \
                    Account.objects.filter(id=receipts['zhichupaymentaccout']).all().values()[0]
            except:
                receipts['zhichupaymentaccout'] = ''
            receipts['dealproject'] = Dealproject.objects.filter(receiptsid=receipts['id']).all().values()
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/threereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'zhiaccount': zhiaccount,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/threereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'zhiaccount': zhiaccount, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        finance = info.get('finance')
        receiptsid = info.get('receiptsid')
        paymenttyoe = info.get('paymenttyoe')
        zhidates = info.get('zhidates')
        zhichupaymentaccout = info.get('zhichupaymentaccout')
        infos = Receipts.objects.filter(id=receiptsid)
        if str(infos.all().values()[0]['iszi']) != '1':
            infos.update(finance=finance, paymenttyoe='已完成', zhidates=zhidates, zhichupaymentaccout=zhichupaymentaccout)
        else:
            infos.update(finance=finance, paymenttyoe=paymenttyoe, zhidates=zhidates,
                         zhichupaymentaccout=zhichupaymentaccout)
        return redirect(reverse("certificate:threereceipts"))


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
            info = list(Receipts.objects.filter(shopname=nowshopname).filter(paymenttyoe='已打款').order_by(
                '-dates').all().values())
        else:
            info = list(Receipts.objects.filter(
                paymenttyoe='已打款').order_by('-dates').all().values())
        nowinfo = []
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
            receipts['photos'] = CertificateImg.objects.filter(for_id=receipts['id']).all()
            return render(request, 'certificate/fourreceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/fourreceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        receiptsimg = request.FILES.getlist('receiptsimg', None)
        if receiptsimg:
            for imgs in receiptsimg:
                img = CertificateImg(img_url=imgs, for_id=request.POST.get('for_id'))
                img.save()

        receiptsid = request.POST.get('receiptsid')
        infos = Receipts.objects.filter(id=receiptsid)
        infos.update(paymenttyoe='资料审批')

        return redirect(reverse("certificate:fourreceipts"))


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
            info = list(Receipts.objects.filter(
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
            return render(request, 'certificate/fivereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo,
                           'receipts': receipts, 'userinfo': userinfo, 'limits': request.session.get('limits')})
        else:
            return render(request, 'certificate/fivereceipts.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        paymenttyoe = request.POST.get('paymenttyoe')
        receiptsid = request.POST.get('receiptsid')
        infos = Receipts.objects.filter(id=receiptsid)
        if paymenttyoe == '资料审批通过':
            paymenttyoe = '已完成'
        infos.update(paymenttyoe=paymenttyoe)

        return redirect(reverse("certificate:fivereceipts"))


class offshorereceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")))
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.order_by('-id').filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")))
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by('-id')

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status=offshoreinfo['status']).all().values()
        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/offshoreindex.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class gongoffshorereceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()

        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")))
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.order_by('-id').filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")))
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(
                tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d"))).order_by('-id')
        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).all().values()
        else:
            offshoreinfo = None
        offshores = offshores.all().values()
        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/gongoffshoreindex.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class oneoffshorereceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)

        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid)
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).order_by('-id')

        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        shopname = request.GET.get('shopname', '')
        gongaccount = request.GET.get('gongaccount', '')

        if starttime != '' and endtime != '':
            offshores = offshores.filter(tijiaodata__range=(starttime, endtime))

        if shopname != '' and shopname != '请选择门店':
            offshores = offshores.filter(shopname=shopname)

        if gongaccount != '' and gongaccount != '请选择公司':
            offshores = offshores.filter(gongaccount=gongaccount)

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).all().values()
        else:
            offshoreinfo = None
        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname, 'gongaccount': gongaccount}
        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        gongaccount = list(Gongaccount.objects.filter().all().values())
        gongaccounts = []
        for i in gongaccount:
            i['id'] = str(i['id'])
            gongaccounts.append(i)
        gongaccount = gongaccounts
        return render(request, 'certificate/oneoffshoreindex.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'search_info': search_info, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


def cncurrency(value, capital=True, prefix=False, classical=None):
    '''
    参数:
    capital:    True   大写汉字金额
                False  一般汉字金额
    classical:  True   元
                False  圆
    prefix:     True   以'人民币'开头
                False, 无开头
    '''
    if not isinstance(value, (Decimal, str, int)):
        msg = '''
        由于浮点数精度问题，请考虑使用字符串，或者 decimal.Decimal 类。
        因使用浮点数造成误差而带来的可能风险和损失作者概不负责。
        '''
        warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False

    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币'
    else:
        prefix = ''

    # 汉字金额字符定义
    dunit = ('角', '分')
    if capital:
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        iunit = [None, '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    else:
        num = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        iunit = [None, '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千', '万', '十', '百', '千']
    if classical:
        iunit[0] = '元' if classical else '圆'
    # 转换为Decimal，并截断多余小数

    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))

    # 处理负数
    if value < 0:
        prefix += '负'  # 输出前缀，加负
        value = - value  # 取正数部分，无须过多考虑正负数舍入
        # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')  # 小数部分和整数部分分别处理
    istr = istr[::-1]  # 翻转整数部分字符串
    so = []  # 用于记录转换结果

    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False  # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”

    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('整')  # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        # so.append(num[0])  # 无角有分，添加“零”
        # haszero = True  # 标记加过零了
        pass

    # 无整数部分
    if istr == '0':
        if haszero:  # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)  # 加前缀
        so.reverse()  # 翻转
        return ''.join(so)

    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:  # 亿和万之间全部为零的情况
                so.pop()  # 去掉万
            so.append(iunit[i])
            if n == 0:  # 处理这些位上为零的情况
                # if not haszero:  # 如果以前没有加过零
                    # so.insert(-1, num[0])  # 则在单位后面加零
                    # haszero = True  # 标记加过零了
                pass
            else:  # 处理不为零的情况
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
            else:  # 处理为零的情况
                if not haszero:  # 如果以前没有加过零
                    # so.append(num[0])
                    # haszero = True
                    pass

    # 最终结果
    so.append(prefix)
    so.reverse()
    return ''.join(so)

class gongoneoffshorereceiptshistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)

        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid)
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).order_by('-id')


        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        shopname = request.GET.get('shopname', '请选择门店')
        gongaccount = request.GET.get('gongaccount', '请选择公司')
        if starttime != '' and endtime != '':
            offshores = offshores.filter(tijiaodata__range=(starttime, endtime))
        if shopname != '请选择门店':
            offshores = offshores.filter(shopname=shopname)
        if gongaccount != '请选择公司':
            offshores = offshores.filter(gongaccount=gongaccount)

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo['types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).all().values()
        else:
            offshoreinfo = None
        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname, 'gongaccount': gongaccount}
        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        gongaccount = list(Gongaccount.objects.filter().all().values())
        gongaccounts = []
        for i in gongaccount:
            i['id'] = str(i['id'])
            gongaccounts.append(i)
        gongaccount = gongaccounts
        return render(request, 'certificate/gongoneoffshoreindex.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'search_info': search_info, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class No_right(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        nowinfo = []
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']

            info = Waicaiinfo.objects.filter(gongaccount=str(gongid)).filter(status__in=['已完成', '待安装']).filter(jiesuan_status__in=['门店已对账', '供货商已对账', ''])
        else:
            info = Waicaiinfo.objects.filter(status__in=['已完成', '待安装']).filter(jiesuan_status__in=['门店已对账', '供货商已对账', ''])
        shopname = request.GET.get('shopname', '请选择门店')
        if shopname != '请选择门店':
            info = info.filter(shopname=shopname)

        starttime = request.GET.get('starttime')
        endtime = request.GET.get('endtime')
        if starttime and endtime:
            if starttime != 'None' and endtime != 'None':
                info = info.filter(tijiaodata__range=(starttime, endtime))

        for i in list(info.all().values()):

            dealprojectinfo = Waicaidealinfo.objects.filter(forid=i['id']).filter(status__in=['待安装', '已完成']).all().values()
            for dealinfo in dealprojectinfo:
                if i['status'] in ['已完成', '待安装', '退货运费已完成'] and i['jiesuan_status'] in ['门店已对账', '供货商已对账', '']:
                    dealinfo['ertwo'] = dealinfo['productname']
                    dealinfo['dates'] = i['tijiaodata']
                    dealinfo['price'] = dealinfo['manay']
                    if dealinfo['jiesuan_status'] == '':
                        dealinfo['status'] = '待月结'
                    else:
                        dealinfo['status'] = dealinfo['jiesuan_status']
                    dealinfo['types'] = '门店外采'
                    dealinfo['companyinfo'] = Gongaccount.objects.filter(id=i['gongaccount']).all().values()[0][
                        'effect']
                    dealinfo['dealprojectid'] = dealinfo['id']
                    dealinfo['dealprojectstatus'] = '外采'
                    dealinfo['id'] = i['id']
                    dealinfo['shopname'] = i['shopname']
                    dealinfo['ordernumber'] = i['ordernumber']
                    nowinfo.append(dealinfo)
        fivereceiptspage = request.GET.get('fourreceiptspage', 1)
        nowinfo = sorted(nowinfo, key=itemgetter('dates'), reverse=True)
        allnowinfo = nowinfo
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(fivereceiptspage)
        search_info = {'starttime': starttime, 'endtime': endtime, 'shopname': shopname}
        return render(request, 'certificate/no_right.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'allnowinfo': allnowinfo,
                       'info': nowinfo, 'limits': request.session.get('limits'),
                       'search_info': search_info, })

    def post(self, request):
        orderid = request.POST.get('orderid')
        dealid = request.POST.get('dealid')

        if Waicaidealinfo.objects.filter(id=dealid).all().values()[0]['status'] in ['已完成', '待安装'] and Waicaidealinfo.objects.filter(id=dealid).all().values()[0]['jiesuan_status'] in ['供货商已对账', '']:
            Waicaidealinfo.objects.filter(id=dealid).update(jiesuan_status='供货商已对账')
        else:
            Waicaidealinfo.objects.filter(id=dealid).update(jiesuan_status='已对账')

        info = len(Waicaidealinfo.objects.filter(forid=orderid).filter(status__in=['待安装', '已完成']).filter(
            jiesuan_status__in=['供货商已对账', '门店已对账', '']).all())
        if info == 0:
            print(datetime.date.today().strftime("%Y-%m-%d"))
            Waicaiinfo.objects.filter(id=orderid).update(jiesuan_status='已对账',
                                                         zhidates=str(datetime.date.today().strftime("%Y-%m-%d")))
        return redirect(reverse('financial_management:no_right'))


class offshoreaddreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)
        number = request.GET.get('number')

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(status='待确认')
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(
                    status='待确认').order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status='待确认').order_by('-id')


        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = list(Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status__in=['待确认', '待发货']).all().values())

        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)


        return render(request, 'certificate/offshorereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'number': number, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        if info.get('number') != '':
            Waicaiinfo.objects.filter(id=info.get('id')).update(status='待发货', number=info.get('number'), sansong=0)
        else:
            Waicaiinfo.objects.filter(id=info.get('id')).update(status='待发货', sansong=0)

        waicaiinfo = Waicaiinfo.objects.filter(id=info.get('id')).all().values()[0]
        userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(info.get('id')),
            send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单待发货，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return redirect(reverse("certificate:offshoreaddreceipts"))


class shouoffshoreaddreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)
        ordernumber = request.GET.get('sansong')
        sansong = request.GET.get('sansong')
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '总部' or nowshopname == '供应商':
            offshores = Waicaiinfo.objects.filter(status='待安装')
        else:
            offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status='待安装')

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status__in=['待安装', '待退货', '已完成']).all().values()

        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/shouoffshorereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'sansong': sansong, 'ordernumber': ordernumber, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        if info.get('sansong') == '':
            sansong = 0
        else:
            sansong = info.get('sansong')
        tuiinfo = Waicaidealinfo.objects.filter(forid=request.POST.get('id')).filter(status='待退货').all().values()
        lentuiinfo = len(tuiinfo)
        waicaiinfo = Waicaiinfo.objects.filter(id=info.get('id')).all().values()[0]
        userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']

        if lentuiinfo == 1:
            tuiid = '外采订单:' + str(tuiinfo[0]['id'])
            tuiinfo = CommentreturnDealproject.objects.filter(order_num=tuiid).all().values()[0]['for_id']
            Commentreturn.objects.filter(id=tuiinfo).update(status='待审批')
            Waicaiinfo.objects.filter(id=info.get('id')).update(status='待退货', sansong=sansong, jiesuan_status='',
                                                            ordernumber=info.get('ordernumber'))
            tishi = WechatMessage(
                source_table='waicaiinfo',
                source_id=str(info.get('id')),
                send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单已发起退货',
                status='0',
                wechatid=wechatid
            )
            tishi.save()
        else:
            Waicaiinfo.objects.filter(id=info.get('id')).update(status='已完成', sansong=sansong, jiesuan_status='',
                                                            ordernumber=info.get('ordernumber'))
            tishi = WechatMessage(
                source_table='waicaiinfo',
                source_id=str(info.get('id')),
                send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单已施工完成',
                status='0',
                wechatid=wechatid
            )
            tishi.save()

        return redirect(reverse("certificate:shouoffshoreaddreceipts"))


class faoffshoreaddreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)
        yunfei = request.GET.get('yunfei')
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(status='待发货')
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(
                    status='待发货').order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status='待发货').order_by('-id')

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status__in=['待安装', '待发货']).all().values()
        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/faoffshoreonereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'yunfei': yunfei, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST


        if info.get('yunfei') == '':
            yunfei = 0
        else:
            if info.get('yunfei') is None:
                yunfei = 0
            else:
                yunfei = info.get('yunfei')
        price = Waicaidealinfo.objects.filter(forid=info.get('id')).filter(status='待安装').all().values()
        pricesinfo = 0
        for i in price:
            pricesinfo += i['manay']

        Waicaiinfo.objects.filter(id=info.get('id')).update(yunfei=yunfei, status='待安装')
        price = Waicaiinfo.objects.filter(id=info.get('id')).all().values()[0]

        pricesinfo = pricesinfo + price['yunfei'] + price['sansong']
        Waicaiinfo.objects.filter(id=info.get('id')).update(allprice=pricesinfo)
        waicaiinfo = Waicaiinfo.objects.filter(id=info.get('id')).all().values()[0]
        gongaccount = waicaiinfo['gongaccount']
        userid = waicaiinfo['userid']
        brand = waicaiinfo['brand']
        gongaccountname = Gongaccount.objects.filter(id=gongaccount).all().values()[0]['effect']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(info.get('id')),
            send_message=gongaccountname + brand +'的货品已经发货，请准备收货，施工',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return redirect(reverse("certificate:faoffshoreaddreceipts"))


class tuifaoffshoreaddreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior)
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)

        commentreturninfo = [i['id'] for i in Commentreturn.objects.filter(order_type='外采退货').filter(
            status__in=['待退货', '已完成', '待审批']).all().values()]
        orderid = []
        for i in commentreturninfo:
            order = CommentreturnDealproject.objects.filter(for_id=i).all().values()[0]['order_num'].replace('外采订单:', '')
            orderid.append(order)
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        orderid = Waicaidealinfo.objects.filter(id__in=orderid).values_list('forid')
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(id__in=orderid)
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(id__in=orderid).order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(id__in=orderid).order_by('-id')
        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status__in=['待退货', '已退货']).all().values()
        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/tuifaoffshoreonereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        if info.get('yunfei') == '':
            yunfei = 0
        else:
            yunfei = info.get('yunfei')
        Waicaiinfo.objects.filter(id=info.get('id')).update(yunfei=yunfei, status='待安装')
        return redirect(reverse("certificate:faoffshoreaddreceipts"))


class tuishoreonereceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior)
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)
        commentreturninfo = [i['id'] for i in Commentreturn.objects.filter(order_type='外采退货').filter(
            status__in=['待退货', '已完成', '待审批']).all().values()]
        orderid = []
        for i in commentreturninfo:
            order = CommentreturnDealproject.objects.filter(for_id=i).all().values()[0]['order_num'].replace('外采订单:','')
            orderid.append(order)
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        offshores = Waicaidealinfo.objects.filter(id__in=orderid).values_list('forid')
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(id__in=offshores)
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(id__in=offshores).order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(id__in=offshores).order_by('-id')

        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
                status__in=['待退货', '已退货']).all().values()
        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/tuishoreonereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        if info.get('yunfei') == '':
            yunfei = 0
        else:
            yunfei = info.get('yunfei')
        Waicaiinfo.objects.filter(id=info.get('id')).update(yunfei=yunfei, status='待安装')
        return redirect(reverse("certificate:faoffshoreaddreceipts"))

def cuidan(request):
    info = request.POST
    waicaiinfo = Waicaiinfo.objects.filter(id=info.get('id')).all().values()[0]
    userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
    wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
    timeinfo = WechatMessage.objects.filter(source_id=str(info.get('id'))).filter(source_table='waicaiinfo').filter(wechatid=wechatid).filter(status=1).all().values('send_datatime')
    timeinfo = [i['send_datatime'] for i in timeinfo]
    if len(timeinfo) != 0:
        timeinfo = max(timeinfo)
        timeinfo = abs((datetime.datetime.now() - datetime.datetime.strptime(str(timeinfo).split('+')[0],'%Y-%m-%d %H:%M:%S')).total_seconds()/ 60)
        if timeinfo>3:
            msg = 'ok'
        else:
            msg = 'no'

    else:
        msg = 'no'

    if msg == 'ok':
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(info.get('id')),
            send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo[
                'brand'] + '的外采订单还未处理，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()

    return JsonResponse({'msg': msg})

def chakan(request):
    offshoreid = request.GET.get('offshoreid', None)

    offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
    gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
    offshoreinfo['gongaccountdizhi'] = gonginfo['effect']
    offshoreinfo['gongaccountname'] = gonginfo['name']
    offshoreinfo['taitou'] = gonginfo['taitou']
    offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
    offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
    offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
        status__in=['已完成', '已退货', '待退货', '待发货', '结算已完成', '供货商已对账', '门店已对账', '待安装']).all().values()
    offshoreinfo['danhao'] = str(offshoreinfo['tijiaodata'].strftime("%Y-%m-%d")).replace('-', '') + str(offshoreinfo['id'])
    offshoreinfo['daxiemanay'] = cncurrency(offshoreinfo['allprice'])
    return render(request, 'certificate/chakan.html', {'offshoreinfo': offshoreinfo})


def chakanan(request):
    offshoreid = request.GET.get('offshoreid', None)

    offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
    gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
    offshoreinfo['gongaccountdizhi'] = gonginfo['effect']
    offshoreinfo['gongaccountname'] = gonginfo['name']
    offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
    offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(
        status__in=['已完成', '已退货', '待退货', '待发货', '结算已完成', '供货商已对账', '门店已对账']).all().values()
    offshoreinfo['danhao'] = str(offshoreinfo['tijiaodata'].strftime("%Y-%m-%d")).replace('-', '') + str(offshoreinfo['id'])
    offshoreinfo['daxiemanay'] = cncurrency(offshoreinfo['allprice'])
    return render(request, 'certificate/chakanan.html', {'offshoreinfo': offshoreinfo})


class addoffshoreaddreceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()

        return render(request, 'certificate/addoffshorereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        shopname = info.get('shopname')
        status = info.get('status')
        gongaccount = info.get('gongaccount')
        brand = info.get('brand')
        motorcycle = info.get('motorcycle')
        model = info.get('model')
        forid = info.get('forid')
        waicaiinfo = Waicaiinfo(
            shopname=shopname,
            status=status,
            gongaccount=gongaccount,
            brand=brand,
            motorcycle=motorcycle,
            forid=forid,
            userid=request.session.get('id'),
            jiesuan_status='',
            tijiaodata=str(datetime.date.today().strftime("%Y-%m-%d")),
            model=model
        )
        waicaiinfo.save()

        Carinfoimgs = request.FILES.getlist('carinfoimg', None)
        if Carinfoimg:
            for imgs in Carinfoimgs:
                img = Carinfoimg(img_url=imgs, for_id=waicaiinfo.id)
                img.save()

        Vinimgs = request.FILES.getlist('vinimg', None)
        if Vinimg:
            for imgs in Vinimgs:
                img = Vinimg(img_url=imgs, for_id=waicaiinfo.id)
                img.save()

        Kindsimgs = request.FILES.getlist('kindsimg', None)
        if Kindsimg:
            for imgs in Kindsimgs:
                img = Kindsimg(img_url=imgs, for_id=waicaiinfo.id)
                img.save()

        userid = Gongaccount.objects.filter(id=gongaccount).all().values()[0]['usernameid']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(waicaiinfo.id),
            send_message='您收到来自途虎养车（' + shopname + '）关于' + brand + '的外采订单，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return redirect(reverse("certificate:offshoreaddreceipts"))


class offshoreonereceipts(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        offshorepage = request.GET.get('offshorepage', 1)
        offshoreid = request.GET.get('offshoreid', None)
        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()

        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(status='申请中')
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(
                    status='申请中').order_by('-id')
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(status='申请中').order_by('-id')

        starttime = request.GET.get('starttime', None)
        endtime = request.GET.get('endtime', None)
        if starttime and endtime:
            offshores = offshores.filter(tijiaodata__range=(starttime, endtime))
            searchinfo = {'starttime': starttime, 'endtime': endtime}
        else:
            searchinfo = None
        if offshoreid:
            offshoreinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
            gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]
            offshoreinfo['gongaccount'] = gonginfo['effect'] + ' ---  ' + gonginfo['name'] + ' ---  ' + gonginfo[
                'types']
            offshoreinfo['baojiaxishu'] = gonginfo['baojiaxishu']
            offshoreinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
            offshoreinfo['dealinfo'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).all().values()
            offshoreinfo['Carinfoimg'] = Carinfoimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Vinimg'] = Vinimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['Kindsimg'] = Kindsimg.objects.filter(for_id=offshoreinfo['id']).all()
            offshoreinfo['offshoredealproject'] = Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).all().values()
            offshoreinfo['numbersss'] = len(
                Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(status__isnull=True).all().values())
        else:
            offshoreinfo = None

        offshores = Paginator(offshores, 10)
        offshores = offshores.page(offshorepage)
        return render(request, 'certificate/offshoreonereceipts.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'gongaccount': gongaccount, 'offshores': offshores, 'offshoreinfo': offshoreinfo,
                       'searchinfo': searchinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST.get('datas')
        forid = request.POST.get('forid')
        info = info.split('**--**')
        infos = []
        waicaiinfo = Waicaiinfo.objects.filter(id=forid).all().values()[0]
        gongaccount = waicaiinfo['gongaccount']
        gongaccount = Gongaccount.objects.filter(id=gongaccount).all().values()
        baojiaxishu = gongaccount[0]['baojiaxishu']
        for i in info:
            infos.append(i.split('**-**'))
        for i in infos:
            if len(i) != 1:
                waicaidealinfo = Waicaidealinfo(
                    brand=i[0],
                    productname=i[1],
                    model=i[2],
                    number=i[3],
                    unit=i[4],
                    status=i[6],
                    manay=float(i[4]) * float(i[3]) * baojiaxishu,
                    forid=forid,
                    jiesuan_status='',
                )
                waicaidealinfo.save()
        Waicaiinfo.objects.filter(id=forid).update(status='待确认')

        waicaiinfo = Waicaiinfo.objects.filter(id=forid).all().values()[0]
        gongaccount = waicaiinfo['gongaccount']
        userid = waicaiinfo['userid']
        brand = waicaiinfo['brand']
        gongaccountname = Gongaccount.objects.filter(id=gongaccount).all().values()[0]['effect']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(forid),
            send_message=gongaccountname + '，已经添加' + brand +'的货品待您确认货品，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return JsonResponse({'msg': 200})


def addreceiptsimg(request):
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
    return render(request, 'certificate/addreceipts.html',
                  {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                   'receipts': receipts,
                   'limitinfo': limits, 'account': account, 'limits': request.session.get('limits')})


def querenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='待发货')
    if request.POST.get('number') != '':
        forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
        Waicaiinfo.objects.filter(id=forid).update(number=request.POST.get('number'))
    return JsonResponse({'msg': 200})


def notquerenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='待确认')
    if request.POST.get('number') != '':
        forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
        Waicaiinfo.objects.filter(id=forid).update(number=request.POST.get('number'))
    return JsonResponse({'msg': 200})


def farenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='待安装')
    forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
    if request.POST.get('yunfei')=='':
        yunfei = 0
    else:
        yunfei = request.POST.get('yunfei')
    Waicaiinfo.objects.filter(id=forid).update(yunfei=yunfei)
    return JsonResponse({'msg': 200})


def notfarenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='待发货')
    forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
    if request.POST.get('yunfei')=='':
        yunfei = 0
    else:
        yunfei = request.POST.get('yunfei')
    Waicaiinfo.objects.filter(id=forid).update(yunfei=yunfei)
    return JsonResponse({'msg': 200})


def getaccount(request):
    info = Account.objects.filter(shopname=request.POST.get('shopname')).filter(isuse=1).all().values()
    return JsonResponse({'account': [[i['id'], i['account'] + '---' + i['name']] for i in info]})


def wufarenokdealinfo(request):
    Waicaiinfo.objects.filter(id=request.POST.get('id')).update(status='无货')

    waicaiinfo = Waicaiinfo.objects.filter(id=request.POST.get('id')).all().values()[0]
    gongaccount = waicaiinfo['gongaccount']
    userid = waicaiinfo['userid']
    gongaccountname = Gongaccount.objects.filter(id=gongaccount).all().values()[0]['effect']
    wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
    tishi = WechatMessage(
        source_table='waicaiinfo',
        source_id=str(request.POST.get('id')),
        send_message=gongaccountname + '，已确认无货，请前往查看（OA地址：http://www.sonoams.com/）',
        status='0',
        wechatid=wechatid
    )
    tishi.save()
    return JsonResponse({'msg': 200})


def qudealinfo(request):
    Waicaiinfo.objects.filter(id=request.POST.get('id')).update(status='订单取消')
    waicaiinfo = Waicaiinfo.objects.filter(id=request.POST.get('id')).all().values()[0]
    userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
    wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
    tishi = WechatMessage(
        source_table='waicaiinfo',
        source_id=str(request.POST.get('id')),
        send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo[
            'brand'] + '的外采订单已取消',
        status='0',
        wechatid=wechatid
    )
    tishi.save()
    return JsonResponse({'msg': 200})


def wudealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='无货')
    return JsonResponse({'msg': 200})


def okdealinfo(request):
    brand = request.POST.get('brand')
    productname = request.POST.get('productname')
    model = request.POST.get('model')
    number = request.POST.get('number')
    unit = request.POST.get('unit')
    forid = request.POST.get('forid')
    info = Waicaidealinfo.objects.filter(id=forid)
    info.update(
        brand=brand,
        productname=productname,
        model=model,
        number=number,
        unit=unit,
        status='待确认',
        manay=int(number) * int(unit)
    )
    return JsonResponse({'msg': 200})


def chafarenokdealinfo(request):
    info = len(Waicaidealinfo.objects.filter(forid=request.POST.get('id')).filter(status='待发货').all().values())

    return JsonResponse({'msg': info})


def someokdealinfo(request):
    info = len(Waicaidealinfo.objects.filter(forid=request.POST.get('id')).filter(status='待发货').all().values())
    return JsonResponse({'msg': info})


def chashourenokdealinfo(request):
    info = len(Waicaidealinfo.objects.filter(forid=request.POST.get('id')).filter(status='待安装').all().values())
    tuiinfo = len(Waicaidealinfo.objects.filter(forid=request.POST.get('id')).filter(status='待退货').all().values())

    return JsonResponse({'msg': info, 'tuimsg': tuiinfo})



def shoufarenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='已完成')
    forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
    if request.POST.get('sansong') == '':
        Waicaiinfo.objects.filter(id=forid).update(ordernumber=request.POST.get('ordernumber'))
    else:
        Waicaiinfo.objects.filter(id=forid).update(ordernumber=request.POST.get('ordernumber'),sansong=request.POST.get('sansong'))
    return JsonResponse({'msg': 200})


def notshoufarenokdealinfo(request):
    Waicaidealinfo.objects.filter(id=request.POST.get('id')).update(status='待安装')
    forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
    if request.POST.get('sansong') == '':
        Waicaiinfo.objects.filter(id=forid).update(ordernumber=request.POST.get('ordernumber'))
    else:
        Waicaiinfo.objects.filter(id=forid).update(ordernumber=request.POST.get('ordernumber'),sansong=request.POST.get('sansong'))
    return JsonResponse({'msg': 200})


def tuihuofarenokdealinfo(request):
    dealinfo = Waicaidealinfo.objects.filter(id=request.POST.get('id'))
    allprice = dealinfo.all().values()[0]['manay']
    for_id = dealinfo.all().values()[0]['forid']
    allpriceinfo = Waicaiinfo.objects.filter(id=for_id).all().values()[0]['allprice']
    allpriceinfo = allpriceinfo - allprice
    Waicaiinfo.objects.filter(id=for_id).update(allprice=allpriceinfo)
    dealinfo.update(status='待退货')
    dealinfo = Waicaidealinfo.objects.filter(id=request.POST.get('id'))
    forid = Waicaidealinfo.objects.filter(id=request.POST.get('id')).all().values()[0]['forid']
    info = Waicaiinfo.objects.filter(id=forid).all().values()[0]
    tuihuoinfo = Commentreturn(
        shopname=info['shopname'],
        consignee=Gongaccount.objects.filter(id=info['gongaccount']).all().values()[0]['effect'],
        operator=request.session.get('name'),
        company='',
        people='',
        license_plate='',
        dates=str(datetime.date.today().strftime("%Y-%m-%d")),
        submitremark='运营外采退货:' + dealinfo.all().values()[0]['productname'],
        allprice=dealinfo.all().values()[0]['manay'],
        status='填写未完成',
        order_type='外采退货'
    )
    tuihuoinfo.save()

    tuihuodealinfo = CommentreturnDealproject(
        order_num='外采订单:' + str(dealinfo.all().values()[0]['id']),
        product_name=dealinfo.all().values()[0]['productname'],
        count=dealinfo.all().values()[0]['number'],
        amount=dealinfo.all().values()[0]['manay'],
        reason='外采退货',
        for_id=tuihuoinfo.id,
        order_type='退货管理'
    )
    tuihuodealinfo.save()

    return JsonResponse({'msg': 200})


class receiptlimits(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        userid = request.GET.get('userid', None)
        userpage = request.GET.get('userpage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        userinfo = Users.objects.filter(superior=superior).all().values().order_by('id').all()
        userinfopaginator = Paginator(userinfo, 10)
        userinfo = userinfopaginator.page(userpage)
        receiptlimits = Newcategory.objects.filter(superior=superior).all().values()
        receiptlimit = {}
        for limit in receiptlimits:
            if limit['one'] not in receiptlimit.keys():
                receiptlimit[limit['one']] = [limit['two']]
            else:
                if limit['two'] not in receiptlimit[limit['one']]:
                    receiptlimit[limit['one']].append(limit['two'])

        if userid:
            oneuserinfo = Users.objects.filter(id=userid).all().values()[0]
            oneuserinfo['submit'] = oneuserinfo['submit'].split('；')
            oneuserinfo['oneapprover'] = oneuserinfo['oneapprover'].split('；')
            oneuserinfo['twoapprover'] = oneuserinfo['twoapprover'].split('；')
        else:
            oneuserinfo = None

        return render(request, 'certificate/receiptlimits.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'userinfo': userinfo,
                       'oneuserinfo': oneuserinfo, 'receiptlimit': receiptlimit,
                       'limits': request.session.get('limits')})

    def post(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        userid = request.GET.get('userid', None)
        userpage = request.GET.get('userpage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        userinfo = Users.objects.filter(superior=superior).all().values().order_by('id').all()
        userinfopaginator = Paginator(userinfo, 10)
        userinfo = userinfopaginator.page(userpage)
        receiptlimits = Newcategory.objects.filter(superior=superior).all().values()
        receiptlimit = {}
        for limit in receiptlimits:
            if limit['one'] not in receiptlimit.keys():
                receiptlimit[limit['one']] = [limit['two']]
            else:
                if limit['two'] not in receiptlimit[limit['one']]:
                    receiptlimit[limit['one']].append(limit['two'])

        if userid:
            oneuserinfo = Users.objects.filter(id=userid).all().values()[0]
        else:
            oneuserinfo = None

        return render(request, 'certificate/receiptlimits.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'userinfo': userinfo,
                       'oneuserinfo': oneuserinfo, 'receiptlimit': receiptlimit,
                       'limits': request.session.get('limits')})


class receiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receiptlimits = Newcategory.objects.filter(superior=superior).all().values().order_by('id').all()
        receiptlimits = Paginator(receiptlimits, 10)
        receiptlimits = receiptlimits.page(receiptlimitspage)
        if receiptlimitid:
            receiptlimitinfo = Newcategory.objects.filter(id=receiptlimitid).all().values()[0]
            limitinfo = UserRight.objects.filter(proinfo=receiptlimitinfo['id']).filter(
                tablename='Newcategory').order_by('id').all().values()
            num = 1
            limitinfos = []
            for i in limitinfo:
                a = {'id': i['id'], 'number': num,
                     'project': Users.objects.filter(id=i['conductor']).all().values()[0]['name']}
                num += 1
                limitinfos.append(a)
            receiptlimitinfo['limitinfo'] = limitinfos
        else:
            receiptlimitinfo = None

        return render(request, 'certificate/receiptclass.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'receiptlimits': receiptlimits, 'receiptlimitinfo': receiptlimitinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class addreceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        return render(request, 'certificate/receiptclass.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'superior': superior, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class updatereceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receiptlimits = Newcategory.objects.filter(superior=superior).all().values().order_by('id').all()
        receiptlimits = Paginator(receiptlimits, 10)
        receiptlimits = receiptlimits.page(receiptlimitspage)
        if receiptlimitid:
            receiptlimitinfo = Newcategory.objects.filter(id=receiptlimitid).all().values()[0]
            limitinfo = UserRight.objects.filter(proinfo=receiptlimitinfo['id']).filter(
                tablename='Newcategory').order_by('id').all().values()
            num = 1
            limitinfos = []
            for i in limitinfo:
                a = {'id': i['id'], 'number': num,
                     'project': Users.objects.filter(id=i['conductor']).all().values()[0]['name']}
                num += 1
                limitinfos.append(a)
            receiptlimitinfo['limitinfo'] = limitinfos
            userinfo = Users.objects.filter(superior=superior).all().values()
        else:
            receiptlimitinfo = None
            userinfo = None

        return render(request, 'certificate/updatereceiptclass.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'receiptlimits': receiptlimits, 'receiptlimitinfo': receiptlimitinfo, 'userinfo': userinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        id = request.POST.get('id')
        userinfo = request.POST.get('userinfo')
        try:
            info = \
                UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
                    'lastuser_right']
        except:
            info = 0
        userright = UserRight(
            proinfo=id,
            tablename='Newcategory',
            conductor=userinfo,
            lastuser_right=info
        )
        userright.save()
        return JsonResponse({'msg': 200})


def shanchureceiptclass(request):
    id = request.POST.get('id')
    try:
        info = UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
            'id']
    except:
        info = 0
    if info != 0:
        UserRight.objects.filter(id=info).delete()
    return JsonResponse({'msg': 200})


def xiugaireceiptclass(request):
    id = request.POST.get('id')
    one = request.POST.get('one')
    two = request.POST.get('two')
    isapprover = request.POST.get('isapprover')
    Newcategory.objects.filter(id=id).update(
        one=one,
        two=two,
        isapprover=isapprover
    )
    return JsonResponse({'msg': 200})
