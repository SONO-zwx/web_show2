import datetime

from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from webApp.approval_administration.models import Receipts, Account, CertificateImg, Dealproject, Shopname, UserRight, \
    Users, Newcategory, Commentreturn, CommentreturnImg, CommentreturnDealproject, Income, IncomeDealproject, IncomeImg, \
    InvoiceImg, InvoiceDealproject, Invoice, Waicaiinfo, Waicaidealinfo, Gongaccount, Vinimg, Carinfoimg, Kindsimg


# Create your views here.
class receiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receiptlimits = Newcategory.objects.filter(superior=superior).filter(classname='支出单据').all().values().order_by(
            '-id').all()
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

        return render(request, 'approval_administration/zhichureceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
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

        return render(request, 'approval_administration/zhichuaddreceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'superior': superior,
                       'name': name, 'limits': request.session.get('limits')})

    def post(self, request):
        one = request.POST.get('one')
        two = request.POST.get('two')
        superior = request.POST.get('superior')
        isapprover = request.POST.get('isapprover')
        info = Newcategory(
            one=one,
            two=two,
            superior=superior,
            isapprover=isapprover,
            classname='支出单据'
        )
        info.save()
        return JsonResponse({'msg': 200})


class updatereceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

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
            userinfo = Users.objects.filter(superior=superior).filter(isuse=1).all().values()
        else:
            receiptlimitinfo = None
            userinfo = None

        return render(request, 'approval_administration/zhichuupdatereceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
                       'receiptlimitspage': receiptlimitspage, 'receiptlimitinfo': receiptlimitinfo,
                       'userinfo': userinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.POST.get('id')
        userinfo = request.POST.get('userinfo')
        info = UserRight.objects.filter(proinfo=id).filter(conductor=userinfo).all().values()
        if len(info) != 0:
            return JsonResponse({'msg': 300})
        try:
            info = \
                UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
                    'id']
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


class shourureceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receiptlimits = Newcategory.objects.filter(superior=superior).filter(classname='收入单据').all().values().order_by(
            '-id').all()
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

        return render(request, 'approval_administration/shourureceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
                       'receiptlimits': receiptlimits, 'receiptlimitinfo': receiptlimitinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class shouruaddreceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        return render(request, 'approval_administration/shouruaddreceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'superior': superior,
                       'name': name, 'limits': request.session.get('limits')})

    def post(self, request):
        one = request.POST.get('one')
        two = request.POST.get('two')
        superior = request.POST.get('superior')
        isapprover = request.POST.get('isapprover')
        info = Newcategory(
            one=one,
            two=two,
            superior=superior,
            isapprover=isapprover,
            classname='收入单据'
        )
        info.save()
        return JsonResponse({'msg': 200})


class shouruupdatereceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

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
            userinfo = Users.objects.filter(superior=superior).filter(isuse=1).all().values()
        else:
            receiptlimitinfo = None
            userinfo = None

        return render(request, 'approval_administration/shouruupdatereceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
                       'receiptlimitspage': receiptlimitspage, 'receiptlimitinfo': receiptlimitinfo,
                       'userinfo': userinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.POST.get('id')
        userinfo = request.POST.get('userinfo')
        info = UserRight.objects.filter(proinfo=id).filter(conductor=userinfo).all().values()
        if len(info) != 0:
            return JsonResponse({'msg': 300})
        try:
            info = \
                UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
                    'id']
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


def shourushanchureceiptclass(request):
    id = request.POST.get('id')
    try:
        info = UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
            'id']
    except:
        info = 0
    if info != 0:
        UserRight.objects.filter(id=info).delete()
    return JsonResponse({'msg': 200})


def shouruxiugaireceiptclass(request):
    id = request.POST.get('id')
    two = request.POST.get('two')
    isapprover = request.POST.get('isapprover')
    Newcategory.objects.filter(id=id).update(
        one=two,
        two=two,
        isapprover=isapprover
    )
    return JsonResponse({'msg': 200})


class tuihuoreceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        receiptlimits = Newcategory.objects.filter(superior=superior).filter(classname='退货管理').all().values().order_by(
            '-id').all()
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

        return render(request, 'approval_administration/tuihuoreceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
                       'receiptlimits': receiptlimits, 'receiptlimitinfo': receiptlimitinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class tuihuoaddreceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        return render(request, 'approval_administration/tuihuoaddreceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'superior': superior,
                       'name': name, 'limits': request.session.get('limits')})

    def post(self, request):
        one = request.POST.get('one')
        two = request.POST.get('two')
        superior = request.POST.get('superior')
        isapprover = request.POST.get('isapprover')
        info = Newcategory(
            one=one,
            two=two,
            superior=superior,
            isapprover=isapprover,
            classname='退货管理'
        )
        info.save()
        return JsonResponse({'msg': 200})


class tuihuoupdatereceiptclass(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        receiptlimitid = request.GET.get('receiptlimitid', None)
        receiptlimitspage = request.GET.get('receiptlimitspage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

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
            userinfo = Users.objects.filter(superior=superior).filter(isuse=1).all().values()
        else:
            receiptlimitinfo = None
            userinfo = None

        return render(request, 'approval_administration/tuihuoupdatereceiptclass.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'name': name,
                       'receiptlimitspage': receiptlimitspage, 'receiptlimitinfo': receiptlimitinfo,
                       'userinfo': userinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        id = request.POST.get('id')
        userinfo = request.POST.get('userinfo')
        info = UserRight.objects.filter(proinfo=id).filter(conductor=userinfo).all().values()
        if len(info) != 0:
            return JsonResponse({'msg': 300})
        try:
            info = \
                UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
                    'id']
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


def tuihuoshanchureceiptclass(request):
    id = request.POST.get('id')
    try:
        info = UserRight.objects.filter(proinfo=id).filter(tablename='Newcategory').order_by('-id').all().values()[0][
            'id']
    except:
        info = 0
    if info != 0:
        UserRight.objects.filter(id=info).delete()
    return JsonResponse({'msg': 200})


def tuihuoxiugaireceiptclass(request):
    id = request.POST.get('id')
    two = request.POST.get('two')
    isapprover = request.POST.get('isapprover')
    Newcategory.objects.filter(id=id).update(
        one=two,
        two=two,
        isapprover=isapprover
    )
    return JsonResponse({'msg': 200})


class Expenditure(APIView):

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
            info = list(Receipts.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                paymenttyoe='待审批').order_by('-dates').all().values())
        new_info = []
        for i in info:
            if i['types'] == '外采' or i['types'] == '外采退换货':
                continue
            new_info.append(i)
        info = new_info
        nowinfo = []
        for i in info:
            dealprojectinfo = Dealproject.objects.filter(receiptsid=i['id']).all().values()[0]
            if i['remarks']:
                remarks = [i.split('**-**') for i in i['remarks'].split('**--**')]
            else:
                remarks = []
            try:
                category = Newcategory.objects.filter(superior=superior).filter(one=i['types']).filter(
                    two=dealprojectinfo['types']).all().values()[0]
            except:
                continue
            userright = UserRight.objects.filter(proinfo=category['id']).filter(conductor=id).all().order_by(
                'id').values()
            if len(userright) != 0:
                if userright[0]['lastuser_right'] == 0:
                    if len(remarks) == 0:
                        i['ertwo'] = dealprojectinfo['types']
                        nowinfo.append(i)
                    else:
                        for shenpi in remarks:
                            if '审批人id：' + str(id) not in shenpi:
                                i['ertwo'] = dealprojectinfo['types']
                                nowinfo.append(i)

                else:
                    someinfo = UserRight.objects.filter(id=userright[0]['lastuser_right']).all().values()[0]
                    for foo in remarks:
                        if '审批人id：' + str(someinfo['conductor']) in foo:
                            i['ertwo'] = dealprojectinfo['types']
                            nowinfo.append(i)
                            break
                        else:
                            break
        category = Newcategory.objects.filter(superior=superior).filter(classname='支出单据').all()
        havelimit = list(set([i[0] for i in UserRight.objects.filter(tablename='Newcategory').filter(
            proinfo__in=category.values_list('id')).all().values_list('proinfo')]))
        categorys = []
        for info in category.values_list('id', 'one', 'two'):
            if str(info[0]) in havelimit:
                continue
            else:
                categorys.append(info)
        if len(categorys) == 0:
            categorys = None
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
            if receipts['remarks']:
                receipts['remarks'] = [
                    {'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for i in
                    receipts['remarks'].split('**--**')]
            else:
                receipts['remarks'] = []

            return render(request, 'approval_administration/expenditure.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo, 'categorys': categorys,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'approval_administration/expenditure.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'categorys': categorys, 'limits': request.session.get('limits')})

    def post(self, request):
        superior = request.session.get('superior')
        id = request.session.get('id')
        info = request.POST
        generalmanager = info.get('generalmanager', '')
        receiptsid = info.get('receiptsid', '')
        paymenttyoe = info.get('paymenttyoe', '')
        remarks = info.get('remarks', '')
        userid = info.get('userid', '')
        info = Receipts.objects.filter(id=receiptsid).all().values()[0]
        dealinfo = Dealproject.objects.filter(receiptsid=int(receiptsid)).all().values()[0]
        try:
            category = Newcategory.objects.filter(superior=superior).filter(one=info['types']).filter(
                two=dealinfo['types']).all().values()[0]
            userright = UserRight.objects.filter(proinfo=int(category['id'])).filter(conductor=int(id)).all().order_by(
                'id').values()[0]['id']
            userright = list(
                UserRight.objects.filter(lastuser_right=userright).filter(proinfo=int(category['id'])).all().values())
        except:
            userright = []
        if info['remarks']:
            remarks = info[
                          'remarks'] + '**--**' + '审批人id：' + userid + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks
        else:
            remarks = '审批人id：' + userid + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks

        if paymenttyoe == '通过审批':
            if len(userright) == 0:
                Receipts.objects.filter(id=receiptsid).update(remarks=remarks, paymenttyoe='待打款')
            else:
                Receipts.objects.filter(id=receiptsid).update(remarks=remarks)

        else:
            Receipts.objects.filter(id=receiptsid).update(remarks=remarks, paymenttyoe='驳回')
        return redirect(reverse('approval_administration:expenditure'))


class Back_goods(APIView):
    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Commentreturn.objects.filter(shopname=nowshopname).filter(status='待审批').order_by(
                '-dates').all().values())
        else:
            info = list(Commentreturn.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待审批').order_by('-dates').all().values())
        nowinfo = []
        for i in info:
            dealprojectinfo = CommentreturnDealproject.objects.filter(for_id=i['id']).all().values()
            if i['approverinfo']:
                remarks = [i.split('**-**') for i in i['approverinfo'].split('**--**')]
            else:
                remarks = []
            try:
                category = Newcategory.objects.filter(classname='退货管理').filter(superior=superior).filter(
                    one=i['order_type']).filter(
                    two=i['order_type']).all().values()[0]
            except:
                continue
            userright = UserRight.objects.filter(proinfo=category['id']).filter(conductor=id).all().order_by(
                'id').values()

            if len(userright) != 0:
                if int(userright[0]['lastuser_right']) == 0:
                    if len(remarks) == 0:
                        i['product_name'] = [i['product_name'] for i in dealprojectinfo]
                        nowinfo.append(i)
                    else:
                        for shenpi in remarks:
                            if '审批人id：' + str(id) not in shenpi:
                                i['product_name'] = [i['product_name'] for i in dealprojectinfo]
                                nowinfo.append(i)
                else:

                    someinfo = UserRight.objects.filter(id=userright[0]['lastuser_right']).all().values()[0]
                    for foo in remarks:
                        if '审批人id：' + str(someinfo['conductor']) in foo:
                            i['product_name'] = [i['product_name'] for i in dealprojectinfo]
                            nowinfo.append(i)
                            break
                        else:
                            break
        category = Newcategory.objects.filter(superior=superior).filter(classname='退货管理').all()
        havelimit = list(set([i[0] for i in UserRight.objects.filter(tablename='Newcategory').filter(
            proinfo__in=category.values_list('id')).all().values_list('proinfo')]))
        categorys = []
        for info in category.values_list('id', 'one', 'two'):
            if str(info[0]) in havelimit:
                continue
            else:
                categorys.append(info)
        if len(categorys) == 0:
            categorys = None
        onereceiptspage = request.GET.get('onereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(onereceiptspage)
        onereceiptsid = request.GET.get('onereceiptsid', None)
        if onereceiptsid:
            receipts = Commentreturn.objects.filter(id=onereceiptsid).all().values()[0]
            receipts['dealproject'] = CommentreturnDealproject.objects.filter(for_id=receipts['id']).all().values()
            if receipts['approverinfo']:
                receipts['approverinfo'] = [
                    {'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for i in
                    receipts['approverinfo'].split('**--**')]
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
                return render(request, 'approval_administration/back_goods.html',
                              {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                               'info': nowinfo, 'offshoreinfo': offshoreinfo, 'receipts': receipts,
                               'userinfo': userinfo, 'limits': request.session.get('limits')})

            receipts['photos'] = CommentreturnImg.objects.filter(for_id=receipts['id']).all()

            return render(request, 'approval_administration/back_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo, 'categorys': categorys,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'approval_administration/back_goods.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'categorys': categorys, 'limits': request.session.get('limits')})

    def post(self, request):
        superior = request.session.get('superior')
        id = request.session.get('id')
        info = request.POST
        generalmanager = info.get('generalmanager', '')
        receiptsid = info.get('receiptsid', '')
        paymenttyoe = info.get('paymenttyoe', '')
        remarks = info.get('remarks', '')
        userid = info.get('userid', '')
        info = Commentreturn.objects.filter(id=receiptsid).all().values()[0]
        dealinfo = CommentreturnDealproject.objects.filter(for_id=int(receiptsid)).all().values()[0]
        try:
            category = Newcategory.objects.filter(superior=superior).filter(one=info['types']).filter(
                two=dealinfo['types']).all().values()[0]
            userright = UserRight.objects.filter(proinfo=int(category['id'])).filter(conductor=int(id)).all().order_by(
                'id').values()[0]['id']
            userright = list(
                UserRight.objects.filter(lastuser_right=userright).filter(proinfo=int(category['id'])).all().values())
        except:
            userright = []
        if info['approverinfo']:
            remarks = info[
                          'approverinfo'] + '**--**' + '审批人id：' + str(
                id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks
        else:
            remarks = '审批人id：' + str(id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks

        if paymenttyoe == '通过审批':
            if len(userright) == 0:
                Commentreturn.objects.filter(id=receiptsid).update(approverinfo=remarks, status='待退货')
            else:
                Commentreturn.objects.filter(id=receiptsid).update(approverinfo=remarks)
        else:
            Commentreturn.objects.filter(id=receiptsid).update(status='驳回')
        return redirect(reverse('approval_administration:back_goods'))


class Collection_voucher(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        userinfo = Users.objects.filter(id=id).all().values()[0]
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname != '总部':
            info = list(Income.objects.filter(shopname=nowshopname).filter(status='待审批').order_by(
                '-dates').all().values())
        else:
            info = list(Income.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待审批').order_by('-dates').all().values())

        nowinfo = []
        for i in info:
            dealprojectinfo = IncomeDealproject.objects.filter(for_id=i['id']).all().values()
            if i['approverinfo']:
                remarks = [i.split('**-**') for i in i['approverinfo'].split('**--**')]
            else:
                remarks = []
            try:
                category = Newcategory.objects.filter(classname='收入单据').filter(superior=superior).filter(
                    one=i['order_type']).filter(
                    two=i['order_type']).all().values()[0]
            except:
                continue
            userright = UserRight.objects.filter(proinfo=category['id']).filter(conductor=id).all().order_by(
                'id').values()
            if len(userright) != 0:
                if int(userright[0]['lastuser_right']) == 0:
                    if len(remarks) != 0:
                        if len(remarks) == 0:
                            nowinfo.append(i)
                        else:
                            for shenpi in remarks:
                                if '审批人id：' + str(id) not in shenpi:
                                    i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                                    i['payment_account'] = \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0][
                                            'name'] + '---' + \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0]['account']

                                    nowinfo.append(i)
                    else:
                        i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                        i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'name'] + '---' + \
                                               Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'account']

                        nowinfo.append(i)
                else:
                    someinfo = UserRight.objects.filter(id=userright[0]['lastuser_right']).all().values()[0]

                    for foo in remarks:
                        if '审批人id：' + str(someinfo['conductor']) in foo:
                            i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                            i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'name'] + '---' + \
                                                   Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'account']
                            nowinfo.append(i)
                            break
                        else:
                            break
        category = Newcategory.objects.filter(superior=superior).filter(classname='收入单据').all()
        havelimit = list(set([i[0] for i in UserRight.objects.filter(tablename='Newcategory').filter(
            proinfo__in=category.values_list('id')).all().values_list('proinfo')]))
        categorys = []
        for info in category.values_list('id', 'one', 'two'):
            if str(info[0]) in havelimit:
                continue
            else:
                categorys.append(info)
        if len(categorys) == 0:
            categorys = None
        onereceiptspage = request.GET.get('onereceiptspage', 1)
        nowinfo = Paginator(nowinfo, 10)
        nowinfo = nowinfo.page(onereceiptspage)
        onereceiptsid = request.GET.get('onereceiptsid', None)
        if onereceiptsid:
            receipts = Income.objects.filter(id=onereceiptsid).all().values()[0]
            receipts['dealproject'] = IncomeDealproject.objects.filter(for_id=receipts['id']).all().values()
            receipts['photos'] = IncomeImg.objects.filter(for_id=receipts['id']).all()
            receipts['payment_account'] = Account.objects.filter(id=receipts['payment_account']).all().values()[0][
                                              'name'] + '---' + \
                                          Account.objects.filter(id=receipts['payment_account']).all().values()[0][
                                              'account']

            if receipts['approverinfo']:
                receipts['approverinfo'] = [
                    {'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for
                    i in receipts['approverinfo'].split('**--**')]
            else:
                receipts['approverinfo'] = []

            return render(request, 'approval_administration/collection_voucher.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'receipts': receipts, 'userinfo': userinfo, 'categorys': categorys,
                           'limits': request.session.get('limits')})
        else:
            return render(request, 'approval_administration/collection_voucher.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'info': nowinfo, 'categorys': categorys, 'limits': request.session.get('limits')})

    def post(self, request):
        superior = request.session.get('superior')
        id = request.session.get('id')
        info = request.POST
        generalmanager = info.get('generalmanager', '')
        receiptsid = info.get('receiptsid', '')
        paymenttyoe = info.get('paymenttyoe', '')
        remarks = info.get('remarks', '')
        info = Income.objects.filter(id=receiptsid).all().values()[0]

        try:
            category = Newcategory.objects.filter(superior=superior).filter(one=info['order_type']).filter(
                two=info['order_type']).all().values()[0]
            userright = UserRight.objects.filter(proinfo=int(category['id'])).filter(conductor=int(id)).all().order_by(
                'id').values()[0]['id']
            userright = list(
                UserRight.objects.filter(lastuser_right=userright).filter(proinfo=int(category['id'])).all().values())
        except:
            userright = []

        if info['approverinfo']:
            remarks = info[
                          'approverinfo'] + '**--**' + '审批人id：' + str(
                id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks
        else:
            remarks = '审批人id：' + str(id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks

        if paymenttyoe == '通过审批':
            if len(userright) == 0:
                Income.objects.filter(id=receiptsid).update(approverinfo=remarks, status='待核实')
            else:
                Income.objects.filter(id=receiptsid).update(approverinfo=remarks)

        else:
            Income.objects.filter(id=receiptsid).update(status='驳回')
        return redirect(reverse('approval_administration:collection_voucher'))
