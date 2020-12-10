from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
from webApp.account.models import Users, Shopname, Limits
from django.core.paginator import Paginator


class addaccount(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        accountpage = int(request.GET.get('accountpage', 1))
        userid = request.GET.get('userid', None)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname == '总部':
            account = Users.objects.filter(superior=superior).filter(
                shopname__in=[i['shopname'] for i in ShopNames.values()]).all()
        else:
            account = Users.objects.filter(superior=superior).filter(shopname=nowshopname).all()
        accountpaginator = Paginator(account, 10)
        account = accountpaginator.page(accountpage)
        if userid:
            try:
                userinfo = Users.objects.filter(id=userid).all().values()[0]
                return render(request, 'account/addaccount.html',
                              {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname,
                               'userinfo': userinfo, 'account': account, 'superior': superior, 'limits': request.session.get('limits')})
            except:
                return render(request, 'account/addaccount.html',
                              {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname,
                               'account': account,
                               'superior': superior, 'limits': request.session.get('limits')})
        return render(request, 'account/addaccount.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'account': account,
                       'superior': superior, 'limits': request.session.get('limits')})

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        shopname = data.get('shopname')
        superior = data.get('superior')
        isuse = data.get('isuse')
        types = data.get('types')
        if types == '修改':
            info = Users.objects.filter(id=data.get('id'))
            info.update(
                password=password,
                name=name,
                shopname=shopname,
                isuse=isuse
            )
        else:
            info = Users(
                username=username,
                password=password,
                name=name,
                shopname=shopname,
                superior=superior,
                limits='',
                oneapprover='',
                twoapprover='',
                submit='',
                isuse=isuse,
            )
            info.save()
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        accountpage = int(request.POST.get('accountpage', 1))
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname == '总部':
            account = Users.objects.filter(superior=superior).filter(shopname__in=[i['shopname'] for i in ShopNames.values()]).all()
        else:
            account = Users.objects.filter(superior=superior).filter(shopname=nowshopname).all()
        accountpaginator = Paginator(account, 10)
        account = accountpaginator.page(accountpage)
        return render(request, 'account/addaccount.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'account': account,
                       'superior': superior, 'limits': request.session.get('limits')})


class accountlimits(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        accountpage = int(request.GET.get('accountpage', 1))
        userid = request.GET.get('userid', None)
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        if nowshopname == '总部':
            account = Users.objects.filter(isuse=1).filter(superior=superior).filter(
                shopname__in=[i['shopname'] for i in ShopNames.values()]).all()
        else:
            account = Users.objects.filter(isuse=1).filter(superior=superior).filter(shopname=nowshopname).all()
        accountpaginator = Paginator(account, 10)
        account = accountpaginator.page(accountpage)

        if userid:
            userinfo = Users.objects.filter(isuse=1).filter(id=userid).all().values()[0]
            userinfo['limits'] = list(userinfo['limits'].split(','))
            userinfo['limits'] = [int(i) for i in userinfo['limits'] if i != '']
            limitsinfo = Limits.objects.filter(superior=superior).all().values()

            return render(request, 'account/accountlimit.html',
                          {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname,
                           'userinfo': userinfo, 'account': account, 'superior': superior, 'limitsinfo': limitsinfo, 'limits': request.session.get('limits')})

        return render(request, 'account/accountlimit.html',
                      {'ShopNames': ShopNames, 'ShopName': ShopName, 'nowshopname': nowshopname, 'account': account,
                       'superior': superior, 'limits': request.session.get('limits')})

    def post(self, request):
        pass


def isaccount(request):
    datainfo = request.POST
    username = datainfo.get('username')
    info = Users.objects.filter(username=username).all().values()

    if len(info) == 0:
        return JsonResponse({'msg': 200})
    else:
        return JsonResponse({'msg': 400})


def delaccount(request):
    datainfo = request.POST
    id = datainfo.get('id')
    info = Users.objects.filter(id=id)
    info.update(
        isuse=0
    )
    return JsonResponse({'msg': 200})



def alertaccountlimit(request):
    userid = request.POST.get('userid')
    nowstatus = request.POST.get('nowstatus')
    values = request.POST.get('values')
    field = request.POST.get('field')

    if nowstatus != 'selected':
        if field == 'limits':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['limits']
            userinfo = userinfo.split(',')
            userinfo.append(str(values))
            info.update(limits=",".join(userinfo))

    else:
        if field == 'limits':
            info = Users.objects.filter(id=userid)
            userinfo = info.all().values()[0]['limits']
            userinfo = userinfo.split(',')
            userinfo.remove(str(values))
            info.update(limits=",".join(userinfo))
    return JsonResponse({})

