import pandas
from django.shortcuts import render
from webApp.login.models import Users, Shopname, Limits
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse
from sqlalchemy import create_engine


# Create your views here.


# 登陆页面
def log(request):
    return render(request, 'login/login.html')


# 登陆验证
def log_in(request):
    info = request.POST
    username = info.get('username')
    password = info.get('password')
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
    if username == '' or password == '':
        return render(request, 'login/login.html')
    sql = """select * from users where username='{}' and password='{}' and isuse=1;""".format(username, password)
    info = pandas.read_sql_query(sql, engine)

    if info.shape[0] == 0:
        return render(request, 'login/login.html')

    limits = Users.objects.filter(username=username).all().values()[0]
    request.session['id'] = limits['id']
    limits = [ i for i in limits['limits'].split(',') if i != '']
    limits = [i['url'] for i in list(Limits.objects.filter(id__in=limits).all().values())]
    superior = info.loc[0, 'superior']
    ShopName = info.loc[0, 'shopname']
    name = info.loc[0, 'name']
    userid = str(info.loc[0, 'id'])
    request.session.set_expiry(0)
    request.session['is_log'] = True
    request.session['name'] = name
    request.session['userid'] = userid
    request.session['username'] = username
    request.session['ShopName'] = ShopName
    request.session['limits'] = limits
    request.session['superior'] = superior
    request.session['nowshopname'] = ShopName
    if request.POST.get('facility') == 'pc':
        if ShopName == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            return render(request, 'login/index.html',
                          {'ShopName': ShopName, 'limits': limits, 'name': name, 'ShopNames': ShopNames,
                           'nowshopname': ShopName,})

        else:
            return render(request, 'login/index.html',
                          {'ShopName': ShopName, 'limits': limits, 'name': name})
    else:
        limits = Users.objects.filter(username=username).all().values()[0]
        request.session['id'] = limits['id']
        limits = [i for i in limits['limits'].split(',') if i != '']
        if '86' in limits or '87' in limits or '106' in limits or '107' in limits:
            return redirect(reverse('offshore:offshore_index'))

        else:
            return redirect(reverse('examine:examine_index'))


def exit_log(request):
    request.session.flush()
    return redirect(reverse('index:log_in'))


def update_pwd(request):
    if request.method.lower() == 'post':
        user_id = request.session['id']
        user_name = request.POST.get('username')
        old_pwd = request.POST.get('old')
        new_pwd = request.POST.get('new')
        user = Users.objects.get(id=user_id)
        if user.username == user_name and user.password == old_pwd:
            user.password = new_pwd
            user.save()
            return redirect(reverse('index:log_in'))
        else:
            return render(request, 'login/update_pwd.html', {'errmsg': '原用户名或密码错误', 'limits': request.session.get('limits')})

    return render(request, 'login/update_pwd.html')


# 切换门店获取信息
# 切换session信息nowshopname
def nowshopname(request):
    info = request.POST
    nowshopname = info.get('nowshopname')
    request.session['nowshopname'] = nowshopname
    return JsonResponse({'msg': 200})


# 验证是否登陆
def id_log_in(f):
    def log_is(request, *args, **kwargs):
        is_log = request.session.get('is_log', False)
        if is_log:
            return f(request, *args, **kwargs)
        else:
            return log(request)

    return log_is


