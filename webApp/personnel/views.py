import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from webApp.personnel.models import Shopname, Staffs, Punish, Performance, Punishimg, Users
from django.core.paginator import Paginator


# Create your views here.
class personnel(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        staffid = request.GET.get('staffinfoid', None)
        staffsinfopage = request.GET.get('staffsinfopage', 1)
        if staffid:
            staffinfo = Staffs.objects.filter(id=staffid).all().values()[0]
        else:
            staffinfo = None
        staffs = Staffs.objects.filter(corporation=superior).all()
        staffs = Paginator(staffs, 10)
        staffs = staffs.page(staffsinfopage)

        return render(request, 'personnel/personnel.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'staffinfo': staffinfo, 'staffs': staffs}
                      )

    def post(self, request):
        pass


class performance(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        performanceid = request.GET.get('performanceid', None)
        performancepage = request.GET.get('performancepage', 1)
        if performanceid:
            Performanceinfo = Performance.objects.filter(id=performanceid).all().values()[0]
        else:
            Performanceinfo = None
        performance = Performance.objects.filter(corporation=superior).all()
        performance = Paginator(performance, 10)
        performance = performance.page(performancepage)

        return render(request, 'personnel/performance.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'performanceinfo': Performanceinfo, 'performance': performance}
                      )

    def post(self, request):
        pass


class withhold(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        withholdid = request.GET.get('withholdid', None)
        withholdpage = request.GET.get('withholdpage', 1)
        shopname = request.GET.get('shopname', '')
        status = request.GET.get('status', '')
        starttime = request.GET.get('starttime', '')
        endtime = request.GET.get('endtime', '')
        if withholdpage == '':
            withholdpage = 1
        if withholdid:
            withholdinfo = Punish.objects.filter(id=withholdid).all().values()[0]
            withholdinfo['photos'] = Punishimg.objects.filter(for_id=withholdinfo['id']).all()
        else:
            withholdinfo = None
        withhold = Punish.objects.filter(corporation=superior).order_by('-id')

        if shopname != '' and shopname != '请选择门店':
            withhold = withhold.filter(shopname=shopname)

        if status != '' and status != '请选择状态':
            withhold = withhold.filter(status=status)

        if starttime != '' and endtime != '':
            withhold = withhold.filter(datatimes__range=(starttime + ' 00:00:00', endtime + ' 00:00:00'))

        search_info = {
            'shopname': shopname,
            'status': status,
            'starttime': starttime,
            'endtime': endtime,
        }
        status = list(set([i['status'] for i in Punish.objects.order_by('datatimes').all().values()]))
        status.remove(None)
        withhold = list(withhold.all().values())
        withhold = Paginator(withhold, 10)
        withhold = withhold.page(withholdpage)

        return render(request, 'personnel/withhold.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'search_info': search_info,
                       'ShopNames': ShopNames, 'withholdinfo': withholdinfo, 'withhold': withhold, 'status': status})

    def post(self, request):
        pass


class shenwithhold(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        withholdid = request.GET.get('withholdid', None)
        withholdpage = request.GET.get('withholdpage', 1)
        if withholdid:
            withholdinfo = Punish.objects.filter(id=withholdid).all().values()[0]
            withholdinfo['photos'] = Punishimg.objects.filter(for_id=withholdinfo['id']).all()
        else:
            withholdinfo = None
        withhold = Punish.objects.filter(corporation=superior).filter(status='申诉中').order_by('-datatimes').all()
        withhold = Paginator(withhold, 10)
        withhold = withhold.page(withholdpage)

        return render(request, 'personnel/shenwithhold.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'withholdinfo': withholdinfo, 'withhold': withhold}
                      )

    def post(self, request):
        pass


def shenwithholdtong(request):
    info = request.GET
    punish = Punish.objects.filter(id=info.get('withholdid'))
    punish.update(
        status='已撤销'
    )
    return redirect('personnel:shenwithhold')


def shenwithholdbo(request):
    info = request.GET
    punish = Punish.objects.filter(id=info.get('withholdid'))
    punish.update(
        status='已生效'
    )
    return redirect('personnel:shenwithhold')


class addpersonnel(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        staffid = request.GET.get('staffinfoid', None)

        if staffid:
            staffinfo = Staffs.objects.filter(id=staffid).all().values()[0]
        else:
            staffinfo = None

        return render(request, 'personnel/addpersonnel.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'staffinfo': staffinfo}
                      )

    def post(self, request):
        info = request.POST
        if not info.get('id', None):
            if info.get('departure_date') == '':
                staffinfo = Staffs(
                    staff_name=info.get('staff_name'),
                    shopname=info.get('shopname'),
                    post=info.get('post'),
                    stafftype=info.get('stafftype'),
                    idtypes=info.get('idtypes'),
                    idcard=info.get('idcard'),
                    idcardstart=info.get('idcardstart'),
                    idcardend=info.get('idcardend'),
                    gex=info.get('gex'),
                    nationality=info.get('nationality'),
                    marstatus=info.get('marstatus'),
                    nation=info.get('nation'),
                    politicsstatus=info.get('politicsstatus'),
                    nativeplace=info.get('nativeplace'),
                    censustypes=info.get('censustypes'),
                    censuslocation=info.get('censuslocation'),
                    staffhome=info.get('staffhome'),
                    dateofbirth=info.get('dateofbirth'),
                    age=info.get('age'),
                    dateonboard=info.get('dateonboard'),
                    workingage=info.get('workingage'),
                    contractexpirationdate=info.get('contractexpirationdate'),
                    unsubmittedinformation=info.get('unsubmittedinformation'),
                    openingbank=info.get('openingbank'),
                    bankid=info.get('bankid'),
                    office=info.get('office'),
                    corporation=request.session.get('superior'),
                    status=info.get('status'))
                staffinfo.save()
            else:
                staffinfo = Staffs(
                    staff_name=info.get('staff_name'),
                    shopname=info.get('shopname'),
                    post=info.get('post'),
                    stafftype=info.get('stafftype'),
                    idtypes=info.get('idtypes'),
                    idcard=info.get('idcard'),
                    idcardstart=info.get('idcardstart'),
                    idcardend=info.get('idcardend'),
                    gex=info.get('gex'),
                    nationality=info.get('nationality'),
                    marstatus=info.get('marstatus'),
                    nation=info.get('nation'),
                    politicsstatus=info.get('politicsstatus'),
                    nativeplace=info.get('nativeplace'),
                    censustypes=info.get('censustypes'),
                    censuslocation=info.get('censuslocation'),
                    staffhome=info.get('staffhome'),
                    dateofbirth=info.get('dateofbirth'),
                    age=info.get('age'),
                    dateonboard=info.get('dateonboard'),
                    workingage=info.get('workingage'),
                    contractexpirationdate=info.get('contractexpirationdate'),
                    unsubmittedinformation=info.get('unsubmittedinformation'),
                    openingbank=info.get('openingbank'),
                    bankid=info.get('bankid'),
                    office=info.get('office'),
                    status=info.get('status'),
                    corporation=request.session.get('superior'),
                    departure_date=info.get('departure_date'))
                staffinfo.save()
        else:
            staffinfo = Staffs.objects.filter(id=info.get('id'))
            if info.get('departure_date') == '':
                staffinfo.update(
                    staff_name=info.get('staff_name'),
                    shopname=info.get('shopname'),
                    post=info.get('post'),
                    stafftype=info.get('stafftype'),
                    idtypes=info.get('idtypes'),
                    idcard=info.get('idcard'),
                    idcardstart=info.get('idcardstart'),
                    idcardend=info.get('idcardend'),
                    gex=info.get('gex'),
                    nationality=info.get('nationality'),
                    marstatus=info.get('marstatus'),
                    nation=info.get('nation'),
                    politicsstatus=info.get('politicsstatus'),
                    nativeplace=info.get('nativeplace'),
                    censustypes=info.get('censustypes'),
                    censuslocation=info.get('censuslocation'),
                    staffhome=info.get('staffhome'),
                    dateofbirth=info.get('dateofbirth'),
                    age=info.get('age'),
                    dateonboard=info.get('dateonboard'),
                    workingage=info.get('workingage'),
                    contractexpirationdate=info.get('contractexpirationdate'),
                    unsubmittedinformation=info.get('unsubmittedinformation'),
                    openingbank=info.get('openingbank'),
                    bankid=info.get('bankid'),
                    office=info.get('office'),
                    status=info.get('status'),
                    corporation=request.session.get('superior')
                )
            else:
                staffinfo.update(
                    staff_name=info.get('staff_name'),
                    shopname=info.get('shopname'),
                    post=info.get('post'),
                    stafftype=info.get('stafftype'),
                    idtypes=info.get('idtypes'),
                    idcard=info.get('idcard'),
                    idcardstart=info.get('idcardstart'),
                    idcardend=info.get('idcardend'),
                    gex=info.get('gex'),
                    nationality=info.get('nationality'),
                    marstatus=info.get('marstatus'),
                    nation=info.get('nation'),
                    politicsstatus=info.get('politicsstatus'),
                    nativeplace=info.get('nativeplace'),
                    censustypes=info.get('censustypes'),
                    censuslocation=info.get('censuslocation'),
                    staffhome=info.get('staffhome'),
                    dateofbirth=info.get('dateofbirth'),
                    age=info.get('age'),
                    dateonboard=info.get('dateonboard'),
                    workingage=info.get('workingage'),
                    contractexpirationdate=info.get('contractexpirationdate'),
                    unsubmittedinformation=info.get('unsubmittedinformation'),
                    openingbank=info.get('openingbank'),
                    bankid=info.get('bankid'),
                    office=info.get('office'),
                    status=info.get('status'),
                    departure_date=info.get('departure_date'),
                    corporation=request.session.get('superior')
                )
        return redirect(reverse("personnel:personnel"))


class addperformance(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        performanceid = request.GET.get('performanceid', None)

        if performanceid:
            performanceinfo = Performance.objects.filter(id=performanceid).all().values()[0]
        else:
            performanceinfo = None

        return render(request, 'personnel/addperformance.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'performanceinfo': performanceinfo}
                      )

    def post(self, request):
        info = request.POST
        if not info.get('id', None):
            performance = Performance(
                project=info.get('project'),
                particulars=info.get('particulars'),
                post=info.get('post'),
                corporation=request.session.get('superior')
            )
            performance.save()
        else:
            performance = Performance.objects.filter(id=info.get('id'))
            performance.update(
                project=info.get('project'),
                particulars=info.get('particulars'),
                post=info.get('post')
            )

        return redirect(reverse("personnel:performance"))


class addwithhold(APIView):

    def get(self, request):
        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        withholdid = request.GET.get('withholdid', None)

        if withholdid:
            withholdinfo = Punish.objects.filter(id=withholdid).all().values()[0]
            withholdinfo['photos'] = Punishimg.objects.filter(for_id=withholdinfo['id']).all()
        else:
            withholdinfo = None
        performance = Performance.objects.filter(corporation=superior, isus=1).all().values()
        gangweiinfo = []

        for i in performance:
            gangweiinfo.append(i['post'])

        gangweiinfo = list(set(gangweiinfo))

        return render(request, 'personnel/addwithhold.html',
                      {'ShopName': ShopName, 'limits': limits, 'name': name, 'superior': superior,
                       'ShopNames': ShopNames, 'withholdinfo': withholdinfo, 'gangweiinfo': gangweiinfo}
                      )

    def post(self, request):

        info = request.POST

        if not info.get('id', None):
            punish = Punish(
                project=str(info.get('projectname')),
                number=info.get('number'),
                staffname=info.get('staffname'),
                price=info.get('price'),
                remark=info.get('remark'),
                datatimes=info.get('datatimes'),
                shopname=info.get('shopname'),
                corporation=request.session.get('superior'),
                status='已生效'
            )
            punish.save()
            receiptsimg = request.FILES.getlist('receiptsimg', None)
            if receiptsimg:
                for imgs in receiptsimg:
                    img = Punishimg(img_url=imgs, for_id=punish.id)
                    img.save()
        else:
            punish = Punish.objects.filter(id=info.get('id'))
            punish.update(
                status='申诉中'
            )
        return redirect(reverse("personnel:withhold"))


def seestaffs(request):
    superior = request.session.get('superior')
    shopname = request.POST.get('shopname')
    staffname = list(Users.objects.filter(superior=superior, shopname=shopname, isuse=1).all().values())

    return JsonResponse({'info': staffname})


def seejixiao(request):
    superior = request.session.get('superior')
    post = request.POST.get('post')
    info = list(Performance.objects.filter(corporation=superior, post=post, isus=1).all().values())
    jixiao = [i['particulars'] for i in info]
    return JsonResponse({'info': jixiao})


def seeparticulars(request):
    superior = request.session.get('superior')
    post = request.POST.get('post')
    project = request.POST.get('project')
    staffname = list(Users.objects.filter(superior=superior, post=post, project=project).all().values())

    return JsonResponse({'info': staffname})
