import datetime

import numpy
import pandas
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from sqlalchemy import create_engine

from webApp.waste.models import Shopname, Wastesubsidiary, Wastepro, Wasteuser, Wastesdealinfo, WasteImg, \
    Wasteusermanay, Newcategory, UserRight
from django.core.paginator import Paginator


# Create your views here.
class wasteinfo(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        starttime = request.GET.get('starttime',
                                    str((datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")))
        endtime = request.GET.get('endtime', str(datetime.date.today()))
        project = request.GET.get('project')

        infopage = request.GET.get('infopage')
        project_listpage = request.GET.get('project_listpage', 1)
        project_list = comment_list()
        list_info = []
        for i in project_list:
            info = comment_dict(i, nowshopname, starttime, endtime)
            list_info.append({'name': i, 'number': info['commendnumber_sql']})
        project_list = list_info
        if project and project != 'undefined':
            info = comment_dict(project, nowshopname, starttime, endtime)
            commendnumber_sql = {'name': project, 'number': info['commendnumber_sql']}

            info = Paginator(list(info['commendlist_sql'].values()), 15)
            info = info.page(int(infopage))
        else:
            commendnumber_sql = None
            info = None

        project_list = Paginator(project_list, 10)
        project_list = project_list.page(project_listpage)
        return render(request, 'waste/wasteinfo.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': info,
                       'project_list': project_list, 'commendnumber_sql': commendnumber_sql, 'starttime': starttime,
                       'endtime': endtime, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class wastetrading(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        return render(request, 'waste/addwaste.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        datas = info.get('datas')
        shopname = info.get('shopname')
        status = info.get('status')
        wasteprotype = info.get('wasteprotype')
        allpriceinfo = info.get('allpriceinfo')
        responsibleperson = info.get('responsibleperson')
        datatimes = info.get('datatimes')
        wasteuser = info.get('wasteuser')
        remark = info.get('remark')
        datas = datas.split('**--**')
        datas = [i.split('**-**') for i in datas]
        info = Wastesubsidiary(
            shopname=shopname,
            status='待审核',
            wastepro=wasteprotype,
            zhimanay=allpriceinfo,
            responsibleperson=responsibleperson,
            datetimes=datatimes,
            wasteuser=wasteuser,
            remark=remark
        )

        info.save()

        for i in datas:
            if len(i) != 1:
                dealproject = Wastesdealinfo(
                    wastepro=i[0],
                    number=i[1],
                    zhimanay=i[2],
                    forid=info.id
                )
                dealproject.save()
        return JsonResponse({'id': info.id})


class wastetradinghistory(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        infopage = request.GET.get('infopage', 1)
        infoid = request.GET.get('infoid', None)
        shopname = request.GET.get('shopname', '')
        gongaccount = request.GET.get('gongaccount', '')
        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname == '总部':
            info = Wastesubsidiary.objects.filter(shopname__in=[i['shopname'] for i in ShopNames])
        else:
            info = Wastesubsidiary.objects.filter(shopname=nowshopname)

        if shopname != '':
            info = info.filter(shopname=shopname)
        if gongaccount != '':
            info = info.filter(wasteuser=gongaccount)
        if starttime != '' and endtime != '':
            info = info.filter(datetimes__range=(starttime, endtime))
        search_info = {
            'gongaccount': gongaccount,
            'starttime': starttime,
            'endtime': endtime,
            'shopname': shopname,
        }
        info = list(info.all().values())
        info = Paginator(info, 10)
        info = info.page(int(infopage))
        if infoid:
            wasteinfo = Wastesubsidiary.objects.filter(id=infoid).all().values()[0]
            wasteinfo['dealproject'] = Wastesdealinfo.objects.filter(forid=wasteinfo['id']).all().values()
            wasteinfo['photos'] = WasteImg.objects.filter(for_id=wasteinfo['id']).all()
        else:
            wasteinfo = None
        gongaccount = Wasteuser.objects.filter().all().values()
        return render(request, 'waste/wastehistory.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': info, 'wasteinfo': wasteinfo, 'limits': request.session.get('limits'),
                       'gongaccount': gongaccount, 'search_info': search_info})

    def post(self, request):
        pass


class wastetradingok(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        id = request.session.get('id')
        superior = request.session.get('superior')
        infopage = request.GET.get('infopage', 1)
        infoid = request.GET.get('infoid', None)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        quanxian = Newcategory.objects.filter(one__in=['危废交易单', '客户带走单']).all().values_list('id')
        quanxian = UserRight.objects.filter(proinfo__in=quanxian).filter(conductor=id).all().values_list('proinfo')
        if len(quanxian) != 0:
            quanxian = Newcategory.objects.filter(id__in=quanxian).all().values_list('one')
            if nowshopname == '总部':
                info = Wastesubsidiary.objects.filter(shopname__in=[i['shopname'] for i in ShopNames]).filter(
                    wastepro__in=quanxian).filter(
                    status='待审核').all()
            else:
                info = Wastesubsidiary.objects.filter(shopname=nowshopname).filter(wastepro__in=quanxian).filter(
                    status='待审核').all()
            info = Paginator(info, 10)
            info = info.page(int(infopage))
        else:
            info = None
        if infoid:
            wasteinfo = Wastesubsidiary.objects.filter(id=infoid).all().values()[0]
            wasteinfo['dealproject'] = Wastesdealinfo.objects.filter(forid=wasteinfo['id']).all().values()
            wasteinfo['photos'] = WasteImg.objects.filter(for_id=wasteinfo['id']).all()
        else:
            wasteinfo = None

        return render(request, 'waste/wastehistoryok.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'info': info, 'wasteinfo': wasteinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        shenremarks = info.get('shenremarks')
        status = info.get('status')
        id = info.get('id')
        stateinfo = info.get('stateinfo')
        manay = info.get('manay')
        wasteuser = info.get('wasteuser')

        info = Wastesubsidiary.objects.filter(id=id)
        info.update(
            shenremarks=shenremarks,
            status=status
        )
        if stateinfo == '扣款':
            info = Wasteuser.objects.filter(username=wasteuser)
            info.update(cashpledge=str(float(info.all().values()[0]['cashpledge']) - float(manay)))
            Wasteusermanay(
                name=wasteuser,
                state=stateinfo,
                manay=manay,
                for_id=info.all().values()[0]['id'],
                datatimes=str(datetime.date.today())
            ).save()

        return redirect(reverse('waste:wastetradingok'))


def addreceiptsimg(request):
    receiptsimg = request.FILES.getlist('receiptsimg', None)
    if receiptsimg:
        for imgs in receiptsimg:
            img = WasteImg(img_url=imgs, for_id=request.POST.get('for_id'))
            img.save()

    return redirect(reverse('waste:wastetrading'))


def searchinfo(request):
    user_info = list(Wasteuser.objects.filter().all().values())

    return JsonResponse({'user_info': user_info})


class wastecontractor(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        wasteuserinfoid = request.GET.get('wastecontractorid')
        wasteuserinfopage = request.GET.get('wasteuserinfopage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        wasteuserinfos = Wasteuser.objects.all()

        wasteuserinfos = Paginator(wasteuserinfos, 10)
        wasteuserinfos = wasteuserinfos.page(wasteuserinfopage)
        if wasteuserinfoid:
            wasteuserinfo = Wasteuser.objects.filter(id=wasteuserinfoid).all().values()[0]
        else:
            wasteuserinfo = None

        return render(request, 'waste/wastecontractor.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'wasteuserinfos': wasteuserinfos, 'wasteuserinfo': wasteuserinfo,
                       'limits': request.session.get('limits')})

    def post(self, request):
        pass


class wasteproject(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        wasteproid = request.GET.get('wasteproid')
        wastepropage = request.GET.get('wastepropage', 1)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        wastepros = Wastepro.objects.all()

        wastepros = Paginator(wastepros, 10)
        wastepros = wastepros.page(wastepropage)
        if wasteproid:
            wastepro = Wastepro.objects.filter(id=wasteproid).all().values()[0]
        else:
            wastepro = None
        return render(request, 'waste/wasteproject.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'wastepros': wastepros,
                       'wastepro': wastepro, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


class addwastecontractor(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        wasteuserinfoid = request.GET.get('wasteuserinfoid')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        if wasteuserinfoid:
            wasteuserinfo = Wasteuser.objects.filter(id=wasteuserinfoid).all().values()[0]
            info = Wasteusermanay.objects.filter(name=wasteuserinfo['username']).all().values()
        else:
            wasteuserinfo = None
            info = None

        return render(request, 'waste/addwastecontractor.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'wasteuserinfo': wasteuserinfo, 'limits': request.session.get('limits'), 'info': info})

    def post(self, request):
        info = request.POST
        id = info.get('id', None)
        username = info.get('username')
        cashpledge = info.get('cashpledge')
        expirydate = info.get('expirydate')
        phone = info.get('phone')
        stateinfo = info.get('stateinfo')
        manay = info.get('manay')
        if id:
            info = Wasteuser.objects.filter(id=id)
            info.update(
                username=username,
                cashpledge=cashpledge,
                expirydate=expirydate,
                phone=phone
            )
            id = id
        else:
            info = Wasteuser(
                username=username,
                cashpledge=cashpledge,
                expirydate=expirydate,
                phone=phone
            )
            info.save()
            id = info.id

        if stateinfo != '请选择':
            if stateinfo == '扣款':
                info = Wasteuser.objects.filter(id=id)
                info.update(cashpledge=str(float(info.all().values()[0]['cashpledge']) - float(manay)))
                Wasteusermanay(
                    name=info.all().values()[0]['username'],
                    state=stateinfo,
                    manay=manay
                ).save()

            else:
                info = Wasteuser.objects.filter(id=id)
                info.update(cashpledge=str(float(info.all().values()[0]['cashpledge']) + float(manay)))
                Wasteusermanay(
                    name=info.all().values()[0]['username'],
                    state=stateinfo,
                    manay=manay
                ).save()
        return redirect(reverse('waste:addwastecontractor'))


class wastecontractorinfo(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        wasteuserinfoid = request.GET.get('wasteuserinfoid')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        wasteuser = Wasteuser.objects.filter().all().values()
        if wasteuserinfoid:
            wasteuserinfo = Wasteuser.objects.filter(id=wasteuserinfoid).all().values()[0]
        else:
            wasteuserinfo = None

        return render(request, 'waste/wastecontractorinfo.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'wasteuserinfo': wasteuserinfo, 'limits': request.session.get('limits'), 'wasteuser': wasteuser})

    def post(self, request):
        info = request.POST
        print(info)
        id = info.get('id', None)
        username = info.get('username')
        cashpledge = info.get('cashpledge')
        expirydate = info.get('expirydate')
        phone = info.get('phone')

        return redirect(reverse('waste:wastecontractorinfo'))


class addwasteproject(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        wasteproid = request.GET.get('wasteproid')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()

        if wasteproid:
            wastepro = Wastepro.objects.filter(id=wasteproid).all().values()[0]
        else:
            wastepro = None

        return render(request, 'waste/addwasteproject.html',
                      {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                       'wastepro': wastepro, 'limits': request.session.get('limits')})

    def post(self, request):
        info = request.POST
        id = info.get('id', None)
        project = info.get('project')
        unit = info.get('unit')
        units = info.get('units')

        if id:
            info = Wastepro.objects.filter(id=id)
            info.update(
                project=project,
                unit=unit,
                units=units
            )
        else:
            info = Wastepro(
                project=project,
                unit=unit,
                units=units
            )
            info.save()
        return redirect(reverse('waste:addwasteproject'))


class wastediff(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        shopname = request.GET.get('shopname')
        times = request.GET.get('times')
        engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
        if shopname:
            info = list(
                Wastesubsidiary.objects.filter(shopname=shopname).filter(wastepro='门店库存单').order_by(
                    '-datetimes').all().values())
            timeinfo = []
            if len(info) >= 2:
                for i in info[:-1]:
                    timeinfo.append(str(i['datetimes']))
        else:
            timeinfo = None
        if times:
            starttime = \
                list(Wastesubsidiary.objects.filter(shopname=shopname).filter(wastepro='门店库存单').filter(
                    datetimes__lt=times)
                     .order_by('-datetimes').all().values())[0]['datetimes']
            sql = """select distinct wastesdealinfo.wastepro '项目' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes between '{}' and '{}' and shopname='{}';""".format(
                starttime, times, shopname)
            df_info = pandas.read_sql_query(sql, engine)
            df_info['卖出数量'] = 0
            sql = """select wastesdealinfo.wastepro '项目',sum(wastesdealinfo.number) '卖出数量' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes between '{}' and '{}' and shopname='{}' and wastesubsidiary.wastepro='危废交易单' group by wastesdealinfo.wastepro;""".format(
                starttime, times, shopname)
            df_infos = pandas.read_sql_query(sql, engine)
            for i in df_infos.T.to_dict().values():
                df_info.loc[df_info['项目'] == i['项目'], '卖出数量'] = i['卖出数量']
            df_info['客户带走数量'] = 0
            sql = """select wastesdealinfo.wastepro '项目',sum(wastesdealinfo.number) '客户带走数量' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes between '{}' and '{}' and shopname='{}' and wastesubsidiary.wastepro='客户带走单' group by wastesdealinfo.wastepro;""".format(
                starttime, times, shopname)
            df_infos = pandas.read_sql_query(sql, engine)
            for i in df_infos.T.to_dict().values():
                df_info.loc[df_info['项目'] == i['项目'], '客户带走数量'] = i['客户带走数量']
            df_info['上次库存数量'] = 0
            sql = """select wastesdealinfo.wastepro '项目',sum(wastesdealinfo.number) '上次库存数量' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes = '{}' and shopname='{}' and wastesubsidiary.wastepro='门店库存单' group by wastesdealinfo.wastepro;""".format(
                starttime, shopname)
            df_infos = pandas.read_sql_query(sql, engine)
            for i in df_infos.T.to_dict().values():
                df_info.loc[df_info['项目'] == i['项目'], '上次库存数量'] = i['上次库存数量']

            df_info['本次库存数量'] = 0
            sql = """select wastesdealinfo.wastepro '项目',sum(wastesdealinfo.number) '本次库存数量' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes = '{}' and shopname='{}' and wastesubsidiary.wastepro='门店库存单' group by wastesdealinfo.wastepro;""".format(
                times, shopname)
            df_infos = pandas.read_sql_query(sql, engine)
            for i in df_infos.T.to_dict().values():
                df_info.loc[df_info['项目'] == i['项目'], '本次库存数量'] = i['本次库存数量']
            df_info['当前系统总数'] = 0
            for i in df_info.T.to_dict().values():
                df_info.loc[df_info['项目'] == i['项目'], '当前系统总数'] = comment_dict(i['项目'], shopname, starttime, times)[
                    'commendnumber_sql']
            df_info['应剩库存'] = df_info['当前系统总数'] + df_info['上次库存数量'] - df_info['客户带走数量'] - df_info['卖出数量']
            df_info['货品差额'] = df_info['本次库存数量'] - df_info['应剩库存']

            df_info = df_info.T.to_dict()
            df_info = [i for i in df_info.values()]
            dealinfo = Wastesubsidiary.objects.filter(shopname=shopname).filter(
                datetimes__range=(starttime, times)).filter(wastepro='危废交易单').all().values()
            return render(request, 'waste/wastediff.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'timeinfo': timeinfo,
                           'searchinfo': {'shopname': shopname, 'times': str(starttime) + '--' + str(times)},
                           'df_info': df_info, 'dealinfo': dealinfo, 'limits': request.session.get('limits')})

        else:
            df_info = None
            dealinfo = None
            return render(request, 'waste/wastediff.html',
                          {'ShopNames': ShopNames, 'name': name, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'timeinfo': timeinfo,
                           'df_info': df_info, 'dealinfo': dealinfo, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


def wasteproinfo(request):
    info = comment_list()
    return JsonResponse({'info': info})


def searchtime(request):
    info = list(Wastesubsidiary.objects.filter(shopname=request.POST.get('shopname')).filter(wastepro='门店库存单').order_by(
        '-datetimes').all().values())
    new_info = []
    if len(info) >= 2:
        for i in info[:-1]:
            new_info.append({'xianshi': str(i['datetimes'])[:-3], 'zhenshi': str(i['datetimes'])})
    else:
        new_info = ['使用需要创建至少两个门店库存单']

    return JsonResponse({'info': new_info}, safe=False)


def comment_list():
    info = ['轮胎', '刹车片', '刹车盘', '减震器', '半轴', '下支臂', '拉杆', '球头', '羊角', '元宝梁', '竖拉杆', '下弯臂', '轴承', '悬挂', '后桥', '排气管',
            '油箱', '涨紧轮', '发动机支脚', '水泵',
            '刹车分泵', '轮毂', '油底壳', '平衡杆', '转向机', '内/外球笼', '发动机机爪', '变速箱机爪', '气门室盖', '正时侧壳', '正时链条', '进气道总成', '进/排气凸轮轴',
            '曲轴',
            '缸盖', '三元催化', '散热器', '电子扇', '电子扇风圈', '水箱', '冷凝器', '中冷器', '节气门', '水箱框架', '电瓶', '起动机', '发电机', '压缩机', '离合器',
            '升降器',
            '前杠', '后杠', '反光镜', '左/右大灯', '内衬', '发动机护板', '前中网']
    return info


def comment_dict(project, ShopName, StartTime, EndTime):
    dict_info = {
        '涨紧轮': {
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%涨紧轮%%';""".format(
                    ShopName, StartTime, EndTime), ],
            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%涨紧轮%%';""".format(
                    ShopName, StartTime, EndTime), ]
        },
        '发动机支脚': {
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%发动机支脚%%';""".format(
                    ShopName, StartTime, EndTime), ],
            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%发动机支脚%%';""".format(
                    ShopName, StartTime, EndTime), ]
        },
        '水泵': {
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%水泵%%';""".format(
                    ShopName, StartTime, EndTime), ],
            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%水泵%%';""".format(
                    ShopName, StartTime, EndTime), ]
        },
        '轮胎': {
            # 轮胎
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%轮胎%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%免费%%' and ProductName like '%%轮胎%%';""".format(
                    ShopName, StartTime, EndTime), ],
        },

        '刹车片': {
            # 刹车片 单片装和四片装
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName like '%%4 片装%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName like '%%4片装%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName not like '%%4片装%%'and ProductName not like '%%4 片装%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number)*4 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName like '%%4 片装%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number)*4 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName like '%%4片装%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%报警线%%' and ProductName like '%%刹车片%%' and ProductName not like '%%4片装%%'and ProductName not like '%%4 片装%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },

        '刹车盘': {
            # 刹车盘 两片装和单片装
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车盘%%' and ProductName like '%%2片装%%' ;""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车盘%%' and ProductName not like '%%2片装%%' ;""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number)*2 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车盘%%' and ProductName like '%%2片装%%' ;""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车盘%%' and ProductName not like '%%2片装%%' ;""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '减震器': {
            # 减震器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%减震器%%' and ProductName not like '%%轴承%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%减振器%%' and ProductName not like '%%轴承%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%减震器%%' and ProductName not like '%%轴承%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%减振器%%' and ProductName not like '%%轴承%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '半轴': {
            # 半轴 左右之分两者求和
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%油%%' and ProductName like '%%左%%' and ProductName like '%%半轴%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%油%%' and ProductName like '%%右%%' and ProductName like '%%半轴%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%油%%' and ProductName like '%%左%%' and ProductName like '%%半轴%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%油%%' and ProductName like '%%右%%' and ProductName like '%%半轴%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '下支臂': {
            # 下支臂
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%球头%%' and ProductName not like '%%胶套%%' and ProductName like '%%下支臂%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName not like '%%拉杆%%' and ProductName not like '%%球头%%' and ProductName not like '%%胶套%%' and ProductName like '%%下支臂%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '拉杆': {
            # 拉杆 区分对
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%拉杆%%' and ProductName not like '%%竖%%' and ProductName not like '%%球头%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%拉杆%%' and ProductName not like '%%竖%%' and ProductName not like '%%球头%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%拉杆%%' and ProductName not like '%%竖%%' and ProductName not like '%%球头%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%拉杆%%' and ProductName not like '%%竖%%' and ProductName not like '%%球头%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '球头': {

            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球头%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球头%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球头%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number)*2 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球头%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '羊角': {
            # 羊角
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%羊角%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%羊角%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '元宝梁': {
            # 元宝梁
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%元宝梁%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%元宝梁%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '竖拉杆': {
            # 竖拉杆
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%竖拉杆%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%竖拉杆%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

            'number': [
                """select sum(Number)*2 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%竖拉杆%%' and ProductName like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%竖拉杆%%' and ProductName not like '%%对%%';""".format(
                    ShopName, StartTime, EndTime),
            ],

        },
        '下弯臂': {
            # 下弯臂
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%下弯臂%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%下弯臂%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '轴承': {
            # 轴承
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%轴承%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%轴承%%' and ProductName not like '%%顶胶%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '悬挂': {
            # 悬挂
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%悬挂%%' and ProductName not like '%%球头%%' and ProductName not like '%%拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%悬挂%%' and ProductName not like '%%球头%%' and ProductName not like '%%拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '后桥': {
            # 后桥
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%后桥%%' and ProductName not like '%%油%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%后桥%%' and ProductName not like '%%油%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '排气管': {
            # 排气管
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%排气管%%' and ProductName not like '%%垫%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%排气管%%' and ProductName not like '%%垫%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '油箱': {
            # 油箱
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%油箱%%' and ProductName not like '%%盖%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%油箱%%' and ProductName not like '%%盖%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '刹车分泵': {
            # 刹车分泵
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车分泵%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%刹车分泵%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '轮毂': {
            # 轮毂
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%轮毂%%' and ProductName not like '%%修复%%' and ProductName not like '%%螺%%' and ProductName not like '%%轮毂盖%%' and ProductName not like '%%轮胎%%' and ProductName not like '%%修%%' and ProductName not like '%%超平%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%轮毂%%' and ProductName not like '%%修复%%' and ProductName not like '%%螺%%' and ProductName not like '%%轮毂盖%%' and ProductName not like '%%轮胎%%' and ProductName not like '%%修%%' and ProductName not like '%%超平%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '油底壳': {
            # 油底壳
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%油底壳%%' and ProductName not like '%%螺丝%%' and ProductName not like '垫' and ProductName not like '放油螺栓';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%油底壳%%' and ProductName not like '%%螺丝%%' and ProductName not like '垫' and ProductName not like '放油螺栓';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '平衡杆': {
            # 平衡杆
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%平衡杆%%' and ProductName not like '%%球头%%' and ProductName not like '%%连接杆%%' and ProductName not like '%%竖拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%平衡杆%%' and ProductName not like '%%球头%%' and ProductName not like '%%连接杆%%' and ProductName not like '%%竖拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '转向机': {
            # 转向机
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%转向机%%' and ProductName not like '%%拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%转向机%%' and ProductName not like '%%拉杆%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '内/外球笼': {
            # 内外球笼
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球笼%%' and ProductName not like '%%防尘套%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%球笼%%' and ProductName not like '%%防尘套%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '发动机机爪': {
            # 发动机机爪
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发动机机爪%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发动机机爪%%';""".format(
                    ShopName, StartTime, EndTime), ],
        },

        '变速箱机爪': {
            # 变速箱机爪
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%变速箱机爪%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%变速箱机爪%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '气门室盖': {
            # 气门室盖
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%气门室盖%%' and ProductName not like '%%垫%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%气门室盖%%' and ProductName not like '%%垫%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '正时侧壳': {
            # 正时侧壳
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%正时侧壳%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%正时侧壳%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '正时链条': {
            # 正时链条
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%正时链条%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%正时链条%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '进气道总成': {
            # 进气道
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%进气道总成%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%进气道总成%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '进/排气凸轮轴': {
            # 进/排气凸轮轴
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%气凸轮轴%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%气凸轮轴%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '曲轴': {
            # 曲轴
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%曲轴%%' and ProductName not like '%%传感器%%' and ProductName not like '%%油封%%' and ProductName not like '%%通风管%%' and ProductName not like '%%皮带轮%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%曲轴%%' and ProductName not like '%%传感器%%' and ProductName not like '%%油封%%' and ProductName not like '%%通风管%%' and ProductName not like '%%皮带轮%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '缸盖': {
            # 缸盖
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%缸盖%%' and ProductName not like '%%三通%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%缸盖%%' and ProductName not like '%%三通%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '三元催化': {
            # 三元催化
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%三元催化%%' and ProductName not like '%%保养剂%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%三元催化%%'  and ProductName not like '%%保养剂%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '散热器': {
            # 散热器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%散热器%%' and ProductName not like '%%胶圈%%' and ProductName not like '%%垫%%' and ProductName not like '%%管%%' and ProductName not like '%%密封圈%%' and ProductName not like '%%修理包%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%散热器%%' and ProductName not like '%%胶圈%%' and ProductName not like '%%垫%%' and ProductName not like '%%管%%' and ProductName not like '%%密封圈%%' and ProductName not like '%%修理包%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '电子扇': {
            # 电子扇
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电子扇%%' and ProductName not like '%%控制器%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电子扇%%' and ProductName not like '%%控制器%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '电子扇风圈': {
            # 电子扇风圈
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电子扇风圈%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电子扇风圈%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '水箱': {
            # 水箱
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%水箱%%' and ProductName not like '%%剂%%' and ProductName not like '%%水管%%' and ProductName not like '%%框架%%' and ProductName not like '%%护板%%' and ProductName not like '%%胶盖%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%水箱%%' and ProductName not like '%%剂%%' and ProductName not like '%%水管%%' and ProductName not like '%%框架%%' and ProductName not like '%%护板%%' and ProductName not like '%%胶盖%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '冷凝器': {
            # 冷凝器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%冷凝器%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%冷凝器%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '中冷器': {
            # 中冷器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%中冷器%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%中冷器%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '节气门': {
            # 节气门
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%节气门%%' and ProductName not like '%%剂%%' and ProductName not like '%%洗%%' and ProductName not like '%%软管%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%节气门%%' and ProductName not like '%%剂%%' and ProductName not like '%%洗%%' and ProductName not like '%%软管%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '水箱框架': {
            # 水箱框架
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%水箱框架%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%水箱框架%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '电瓶': {
            # 电瓶
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电瓶%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%电瓶%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '起动机': {
            # 起动机
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%起动机%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%起动机%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '发电机': {
            # 发电机
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发电机%%' and ProductName not like '%%皮带%%' and ProductName not like '%%涨紧%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发电机%%' and ProductName not like '%%皮带%%' and ProductName not like '%%涨紧%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '压缩机': {
            # 压缩机
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%压缩机%%' and ProductName not like '%%润滑油%%' and ProductName not like '%%高压管%%' and ProductName not like '%%张紧轮%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%压缩机%%' and ProductName not like '%%润滑油%%' and ProductName not like '%%高压管%%' and ProductName not like '%%张紧轮%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '离合器': {
            # 离合器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%离合器%%' and ProductName not like '%%油%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%离合器%%' and ProductName not like '%%油%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '升降器': {
            # 升降器
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%升降器%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%升降器%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '前杠': {
            # 前杠
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%前杠%%' and ProductName not like '%%卡子%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%前杠%%' and ProductName not like '%%卡子%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '后杠': {
            # 后杠
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%后杠%%' and ProductName not like '%%灯%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%后杠%%' and ProductName not like '%%灯%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '反光镜': {
            # 反光镜
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%反光镜%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%反光镜%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '左/右大灯': {
            # 左/右大灯
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%大灯%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%大灯%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '内衬': {
            # 内衬
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%内衬%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%内衬%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '发动机护板': {
            # 发动机护板
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发动机护板%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%发动机护板%%';""".format(
                    ShopName, StartTime, EndTime), ],

        },
        '前中网': {
            # 前中网
            'project': [
                """select OrderNumber,ProductCode,ProductName,Number,Unit from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%前中网%%';""".format(
                    ShopName, StartTime, EndTime), ],

            'number': [
                """select sum(Number) 'number' from commoditylist where OrderNumber in (select OrderNumber from exportorders where ShopName='{}' and InstallationTime Between '{}' And '{}') and ProductCode not like 'FU%%' and ProductName like '%%前中网%%';""".format(
                    ShopName, StartTime, EndTime), ],
        },
    }
    engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
    df_infos = pandas.DataFrame()
    number = 0

    for sql in dict_info[project]['project']:
        df_info = pandas.read_sql_query(sql, engine)
        df_infos = df_infos.append(df_info)
    df_infos.index = numpy.array(range(df_infos.shape[0]))
    data_info = df_infos.T.to_dict()
    for sql in dict_info[project]['number']:
        numbers = pandas.read_sql_query(sql, engine)
        if numbers['number'].values[0] != None:
            number += int(numbers['number'].values[0])

    return {'commendlist_sql': data_info, 'commendnumber_sql': number}
