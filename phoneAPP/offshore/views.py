import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from rest_framework.views import APIView
from webApp.certificate.models import Account, Gongaccount, Shopname, Receipts, Dealproject, CertificateImg, \
    UserRight, Users, Newcategory, Waicaidealinfo, Waicaiinfo, Carinfoimg, Vinimg, Kindsimg, Commentreturn, \
    CommentreturnDealproject, CommentreturnImg, WechatMessage

class offshore_index(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        userid = request.session.get('userid')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        nowshopname = request.session.get('nowshopname')

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(status__in=['申请中', '待发货']).all().values()
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(status__in=['待确认', '待安装']).order_by('-id').all().values()
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(userid=userid).filter(status__in=['待确认', '待安装']).order_by('-id').all().values()

        for i in offshores:
            i['username'] = Users.objects.filter(id=i['userid']).all().values()[0]['name']

        return render(request, 'app/offshore/offshore.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'offshores': offshores})

    def post(self, request):
        pass


class add_offshore(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        return render(request, 'app/offshore/add_offshore.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'gongaccount': gongaccount,})

    def post(self, request):
        info = request.POST
        shopname = info.get('shopname')
        status = info.get('status', '申请中')
        gongaccount = info.get('gongaccount')
        brand = info.get('brand')
        motorcycle = info.get('motorcycle')
        model = info.get('model')
        forid = info.get('forid')
        isok = info.get('isok')
        if isok == '0':
            name = request.session.get('name')
            username = request.session.get('username')
            ShopName = request.session.get('ShopName')
            limits = request.session.get('limits')
            superior = request.session.get('superior')
            ShopName = request.session.get('nowshopname')

            gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
            return render(request, 'app/offshore/add_offshore.html',
                          {'ShopName': ShopName, 'limits': limits, 'name': name,
                           'nowshopname': ShopName, 'gongaccount': gongaccount, })
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
        return redirect(reverse("offshore:gongzuotai"))


class gongzuotai(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/offshore/gongzuotai.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass


class offshore_one(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        userid = request.session.get('userid')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        nowshopname = request.session.get('nowshopname')

        gongaccount = Gongaccount.objects.filter(shopname=superior).all().values()
        if nowshopname == '供应商':
            gongid = Gongaccount.objects.filter(usernameid=id).all().values()[0]['id']
            offshores = Waicaiinfo.objects.filter(gongaccount=gongid).filter(status__in=['申请中', '待发货']).all().values()
        else:
            if nowshopname == '总部':
                offshores = Waicaiinfo.objects.filter(status__in=['待确认', '待安装']).order_by('-id').all().values()
            else:
                offshores = Waicaiinfo.objects.filter(shopname=nowshopname).filter(userid=userid).filter(status__in=['待确认', '待安装']).order_by('-id').all().values()

        for i in offshores:
            i['username'] = Users.objects.filter(id=i['userid']).all().values()[0]['name']

        return render(request, 'app/offshore/offshore_one.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'offshores': offshores})

    def post(self, request):
        pass


class offshore_two(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        offshoreid = request.GET.get('offshoreid')

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
        offshoreinfo['username'] = Users.objects.filter(id=offshoreinfo['userid']).all().values()[0]['name']
        offshoreinfo['numbersss'] = len(
            Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(status__isnull=True).all().values())

        return render(request, 'app/offshore/offshore_two.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'offshoreinfo': offshoreinfo})

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
            send_message=gongaccountname + '，已经添加' + brand + '的货品待您确认货品，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return JsonResponse({'msg': 200})


class offshore_three(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/offshore/offshore_three.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,'nowshopname': ShopName, })

    def post(self, request):
        pass


class offshore_four(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/offshore/offshore_four.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass


class offshore_five(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        offshoreid = request.GET.get('offshoreid')

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
        offshoreinfo['username'] = Users.objects.filter(id=offshoreinfo['userid']).all().values()[0]['name']
        offshoreinfo['numbersss'] = len(
            Waicaidealinfo.objects.filter(forid=offshoreinfo['id']).filter(status__isnull=True).all().values())

        return render(request, 'app/offshore/offshore_five.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'offshoreinfo': offshoreinfo})


    def post(self, request):
        info = request.POST

        if info.get('number') != '':
            Waicaiinfo.objects.filter(id=info.get('offshoreid')).update(status='待发货', number=info.get('number'), sansong=0)
        else:
            Waicaiinfo.objects.filter(id=info.get('offshoreid')).update(status='待发货', sansong=0)

        Waicaidealinfo.objects.filter(id=request.POST.get('isid')).update(status='待发货')
        waicaiinfo = Waicaiinfo.objects.filter(id=info.get('offshoreid')).all().values()[0]
        userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']
        tishi = WechatMessage(
            source_table='waicaiinfo',
            source_id=str(info.get('offshoreid')),
            send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单待发货，请前往处理（OA地址：http://www.sonoams.com/）',
            status='0',
            wechatid=wechatid
        )
        tishi.save()
        return redirect(reverse("certificate:offshoreaddreceipts"))


class quxiaodingdan(APIView):

    def post(self, request):
        offshoreid = request.POST.get('offshoreid')
        Waicaiinfo.objects.filter(id=offshoreid).update(status='订单取消')

        waicaiinfo = Waicaiinfo.objects.filter(id=offshoreid).all().values()[0]
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


class offshore_six(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        dealid = request.GET.get('dealid')
        dealinfo = Waicaidealinfo.objects.filter(id=dealid).all().values()[0]
        offshoreinfo = Waicaiinfo.objects.filter(id=dealinfo['forid']).all().values()[0]
        gonginfo = Gongaccount.objects.filter(id=offshoreinfo['gongaccount']).all().values()[0]

        dealinfo['baojiaxishu'] = gonginfo['baojiaxishu']
        dealinfo['xiaoshouxishu'] = gonginfo['xiaoshouxishu']
        return render(request, 'app/offshore/offshore_six.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, 'dealinfo': dealinfo})

    def post(self, request):
        pass


class offshore_seven(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/offshore/offshore_seven.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass


class offshore_eight(APIView):
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


        return render(request, 'app/offshore/offshore_eight.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname, 'offshoreinfo': offshoreinfo,
                       'sansong': sansong, 'ordernumber': ordernumber, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        if info.get('sansong') == '':
            sansong = 0
        else:
            sansong = info.get('sansong')

        dealid = Waicaidealinfo.objects.filter(forid=info.get('offshoreid')).filter(status='待安装').all().values()[0]['id']

        if info.get('status') == '1':
            Waicaidealinfo.objects.filter(id=dealid).update(status='已完成')
        else:
            dealinfo = Waicaidealinfo.objects.filter(id=dealid)
            allprice = dealinfo.all().values()[0]['manay']
            for_id = dealinfo.all().values()[0]['forid']
            allpriceinfo = Waicaiinfo.objects.filter(id=for_id).all().values()[0]['allprice']
            allpriceinfo = allpriceinfo - allprice
            Waicaiinfo.objects.filter(id=for_id).update(allprice=allpriceinfo)
            dealinfo.update(status='待退货')
            dealinfo = Waicaidealinfo.objects.filter(id=dealid)
            forid = Waicaidealinfo.objects.filter(id=dealid).all().values()[0]['forid']
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

        tuiinfo = Waicaidealinfo.objects.filter(forid=request.POST.get('offshoreid')).filter(status='待退货').all().values()
        lentuiinfo = len(tuiinfo)
        waicaiinfo = Waicaiinfo.objects.filter(id=request.POST.get('offshoreid')).all().values()[0]
        userid = Gongaccount.objects.filter(id=waicaiinfo['gongaccount']).all().values()[0]['usernameid']
        wechatid = Users.objects.filter(id=userid).all().values()[0]['oneapprover']

        if lentuiinfo == 1:
            tuiid = '外采订单:' + str(tuiinfo[0]['id'])
            tuiinfo = CommentreturnDealproject.objects.filter(order_num=tuiid).all().values()[0]['for_id']
            Commentreturn.objects.filter(id=tuiinfo).update(status='待审批')
            Waicaiinfo.objects.filter(id=request.POST.get('offshoreid')).update(status='待退货', sansong=sansong, jiesuan_status='',
                                                            ordernumber=info.get('ordernumber'))
            tishi = WechatMessage(
                source_table='waicaiinfo',
                source_id=str(info.get('offshoreid')),
                send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单已发起退货',
                status='0',
                wechatid=wechatid
            )
            tishi.save()
        else:
            Waicaiinfo.objects.filter(id=request.POST.get('offshoreid')).update(status='已完成', sansong=sansong, jiesuan_status='',
                                                            ordernumber=info.get('ordernumber'))
            tishi = WechatMessage(
                source_table='waicaiinfo',
                source_id=str(info.get('offshoreid')),
                send_message='途虎养车（' + waicaiinfo['shopname'] + '）' + waicaiinfo['brand'] + '的外采订单已施工完成',
                status='0',
                wechatid=wechatid
            )
            tishi.save()

        return redirect(reverse("offshore:offshore_index"))


class offshore_nine(APIView):
    def get(self, request):
        name = request.session.get('name')
        username = request.session.get('username')
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        superior = request.session.get('superior')
        ShopName = request.session.get('nowshopname')
        return render(request, 'app/offshore/offshore_nine.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name,
                       'nowshopname': ShopName, })

    def post(self, request):
        pass