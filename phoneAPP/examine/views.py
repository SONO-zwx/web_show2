from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from rest_framework.views import APIView
from webApp.approval_administration.models import Receipts, Account, CertificateImg, Dealproject, Shopname, UserRight, \
    Users, Newcategory, Commentreturn, CommentreturnImg, CommentreturnDealproject, Income, IncomeDealproject, IncomeImg, \
    InvoiceImg, InvoiceDealproject, Invoice, Waicaiinfo, Waicaidealinfo, Gongaccount, Vinimg, Carinfoimg, Kindsimg

##########################
class examine_index(APIView):
    def get(self, request):
        username = request.session.get('username')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        nowshopname = request.session.get('nowshopname')
        name = request.session.get('name')
        id = request.session.get('id')
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
        if nowshopname != '总部':
            info = list(Income.objects.filter(shopname=nowshopname).filter(status='待审批').order_by(
                '-dates').all().values())
        else:
            info = list(Income.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待审批').order_by('-dates').all().values())

        zhinowinfo = []
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
                            zhinowinfo.append(i)
                        else:
                            for shenpi in remarks:
                                if '审批人id：' + str(id) not in shenpi:
                                    i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                                    i['payment_account'] = \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0][
                                            'name'] + '---' + \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0]['account']

                                    zhinowinfo.append(i)
                    else:
                        i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                        i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'name'] + '---' + \
                                               Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'account']

                        zhinowinfo.append(i)
                else:
                    someinfo = UserRight.objects.filter(id=userright[0]['lastuser_right']).all().values()[0]

                    for foo in remarks:
                        if '审批人id：' + str(someinfo['conductor']) in foo:
                            i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                            i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'name'] + '---' + \
                                                   Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'account']
                            zhinowinfo.append(i)
                            break
                        else:
                            break

        return render(request, 'app/examine/examine.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'nowinfo': nowinfo, 'zhinowinfo': zhinowinfo})

    def post(self, request):
        pass


class examine_two(APIView):
    def get(self, request):
        username = request.session.get('username')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        nowshopname = request.session.get('nowshopname')
        name = request.session.get('name')
        id = request.session.get('id')
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
        if nowshopname != '总部':
            info = list(Income.objects.filter(shopname=nowshopname).filter(status='待审批').order_by(
                '-dates').all().values())
        else:
            info = list(Income.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                status='待审批').order_by('-dates').all().values())

        zhinowinfo = []
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
                            zhinowinfo.append(i)
                        else:
                            for shenpi in remarks:
                                if '审批人id：' + str(id) not in shenpi:
                                    i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                                    i['payment_account'] = \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0][
                                            'name'] + '---' + \
                                        Account.objects.filter(id=i['payment_account']).all().values()[0]['account']

                                    zhinowinfo.append(i)
                    else:
                        i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                        i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'name'] + '---' + \
                                               Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                   'account']

                        zhinowinfo.append(i)
                else:
                    someinfo = UserRight.objects.filter(id=userright[0]['lastuser_right']).all().values()[0]

                    for foo in remarks:
                        if '审批人id：' + str(someinfo['conductor']) in foo:
                            i['product_name'] = [i['project_name'] for i in dealprojectinfo]
                            i['payment_account'] = Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'name'] + '---' + \
                                                   Account.objects.filter(id=i['payment_account']).all().values()[0][
                                                       'account']
                            zhinowinfo.append(i)
                            break
                        else:
                            break

        return render(request, 'app/examine/examine_two.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'nowinfo': nowinfo, 'zhinowinfo': zhinowinfo})

    def post(self, request):
        pass


class examine_three(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        onereceiptsid = request.GET.get('onereceiptsid')
        receipts = Income.objects.filter(id=onereceiptsid).all().values()[0]
        receipts['dealproject'] = IncomeDealproject.objects.filter(for_id=receipts['id']).all().values()
        receipts['photos'] = IncomeImg.objects.filter(for_id=receipts['id']).all()
        receipts['payment_account'] = Account.objects.filter(id=receipts['payment_account']).all().values()[0][
                                          'name'] + '---' + \
                                      Account.objects.filter(id=receipts['payment_account']).all().values()[0][
                                          'account']

        if receipts['approverinfo']:
            receipts['approverinfo'] = [{'name': i.split('**-**')[1], 'status': i.split('**-**')[2], 'limits': i.split('**-**')[3]} for
                i in receipts['approverinfo'].split('**--**')]
        else:
            receipts['approverinfo'] = []
        return render(request, 'app/examine/examine_three.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'receipts': receipts})

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
            Income.objects.filter(id=receiptsid).update(status='驳回', approverinfo=remarks)
        return redirect(reverse('examine:examine_two'))

class examine_four(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')

        onereceiptsid = request.GET.get('id')
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

        return render(request, 'app/examine/examine_four.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'receipts': receipts})

    def post(self, request):
        superior = request.session.get('superior')
        id = request.session.get('id')
        info = request.POST
        generalmanager = info.get('generalmanager', '')
        receiptsid = info.get('receiptsid', '')
        paymenttyoe = info.get('paymenttyoe', '')
        remarks = info.get('remarks', '')
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
                          'remarks'] + '**--**' + '审批人id：' + str(id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks
        else:
            remarks = '审批人id：' + str(id) + '**-**' + generalmanager + '**-**' + paymenttyoe + '**-**' + remarks

        if paymenttyoe == '通过审批':
            if len(userright) == 0:
                Receipts.objects.filter(id=receiptsid).update(remarks=remarks, paymenttyoe='待打款')
            else:
                Receipts.objects.filter(id=receiptsid).update(remarks=remarks)

        else:
            Receipts.objects.filter(id=receiptsid).update(remarks=remarks, paymenttyoe='驳回')
        return redirect(reverse('examine:examine_two'))



class examine_five(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/examine/examine_five.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass


class examine_six(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/examine/examine_six.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass


class examine_seven(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/examine/examine_seven.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass