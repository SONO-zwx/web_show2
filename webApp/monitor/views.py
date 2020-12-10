import base64
import threading
import time

import pandas
import datetime
import pymysql
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.views import APIView
from sqlalchemy import create_engine
from django.http import JsonResponse
from webApp.monitor.models import Cameralist, Picturessoninfo, Picturesmaininfo, Punish, Punishimg, Performance
# Create your views here.

class Monitor_list(APIView):
    def get(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
        id = request.GET.get('id')
        if id:
            sql = """select cameralist.id '工位id', picturesmaininfo.id 'id', picturessoninfo.dates '日期', picturesmaininfo.shopnameid '门店', cameralist.cameraname '工位', sum(ispunish) '处罚数量', count(picturessoninfo.id)-sum(isok) '未处理数量', sum(pubishmanay) '处罚金额', cameralistid  from picturessoninfo left join picturesmaininfo on picturesmaininfo.id=picturessoninfo.mainid left join cameralist on cameralist.id=picturessoninfo.cameralistid where mainid='{}' group by picturessoninfo.dates, picturesmaininfo.shopnameid, cameralist.cameraname, picturessoninfo.cameralistid;""".format(id)
            df_info = pandas.read_sql_query(sql, engine)
            info = list(df_info.T.to_dict().values())
        else:
            try:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
                sql = """select cameralist.id '工位id', picturesmaininfo.id 'id', picturessoninfo.dates '日期', picturesmaininfo.shopnameid '门店', cameralist.cameraname '工位', sum(ispunish) '处罚数量', count(picturessoninfo.id)-sum(isok) '未处理数量', sum(pubishmanay) '处罚金额', cameralistid  from picturessoninfo left join picturesmaininfo on picturesmaininfo.id=picturessoninfo.mainid left join cameralist on cameralist.id=picturessoninfo.cameralistid where mainid in (select id from picturesmaininfo where data='{}' and cameralist.superior='{}') group by picturessoninfo.dates, picturesmaininfo.shopnameid, cameralist.cameraname, picturessoninfo.cameralistid;""".format(date, request.session.get('superior'))
                df_info = pandas.read_sql_query(sql, engine)
                info = list(df_info.T.to_dict().values())
            except:
                info = []

        return render(request, 'monitor/monitor_list.html', {'info': info, 'limits': request.session.get('limits')})

    def post(self, request):
        return render(request, 'monitor/monitor_list.html')




class monitor_history(APIView):
    def get(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')

        sql = """select data '日期', sum(nonumber) '未处理数量' from picturesmaininfo where nonumber!=0 group by data order by -data;"""
        df_info = pandas.read_sql_query(sql, engine)
        info = list(df_info.T.to_dict().values())

        date = request.GET.get('date', None)
        if date:
            hhdealinfo = list(Picturesmaininfo.objects.filter(data=date).all().values())
        else:
            hhdealinfo = None
        return render(request, 'monitor/monitor_history.html', {'info': info, 'limits': request.session.get('limits'), 'hhdealinfo': hhdealinfo})

    def post(self, request):
        return render(request, 'monitor/monitor_history.html')


class Monitor_detail(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id:
            info = list(Picturessoninfo.objects.filter(mainid=id).filter(cameralistid=request.GET.get('num')).all().values())
            fourreceiptspage = request.GET.get('fourreceiptspage', 1)
            accountpaginator = Paginator(info, 6)
            print(fourreceiptspage)
            info = accountpaginator.page(fourreceiptspage)
        else:
            info = None

        return render(request, 'monitor/monitor_detail.html', {'info': info, 'limits': request.session.get('limits'), 'id': id, 'num': request.GET.get('num')})

    def post(self, request):
        return render(request, 'monitor/monitor_detail.html')


class Handle_pic(APIView):
    def get(self, request):
        id = request.GET.get('id')
        info = Picturessoninfo.objects.filter(id=id).all().values()[0]
        engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
        sql = """select distinct post from performance where performance.isus=1;"""
        gangwei_info = pandas.read_sql(sql, engine).to_dict()

        return render(request, 'monitor/handle_pic.html', {'info': info, 'gangwei_info': gangwei_info})

    def post(self, request):
        id = request.POST.get('id')
        canvas = request.POST.get('canvas', None)
        pubish = request.POST.get('pubish')
        pubishuser = request.POST.get('pubishuser')
        pubishmanay = request.POST.get('pubishmanay')
        performance = request.POST.get('performance')
        isokremark = request.POST.get('isokremark')
        if canvas:
            canvas = 'data:' + canvas.split('data:')[1]
        info = Picturessoninfo.objects.filter(id=id)
        if pubish == '通过':
            info.update(okpictures=canvas, isok=1, ispunish=0, isokremark=isokremark, isokdatatime=datetime.datetime.now().strftime('%Y-%m-%d'))
        else:
            info.update(okpictures=canvas,isok=1,ispunish=1 ,pubish=pubish ,pubishuser=pubishuser ,pubishmanay=pubishmanay ,isokname=isokremark ,isokdatatime=datetime.datetime.now().strftime('%Y-%m-%d'))

            shopnameinfo = Picturesmaininfo.objects.filter(id=info.all().values()[0]['mainid']).all().values()[0]
            punish = Punish(
                project=Performance.objects.filter(id=performance).all().values()[0]['particulars'],
                number=1,
                staffname=pubishuser,
                price=pubishmanay,
                remark=isokremark,
                datatimes=datetime.datetime.now().strftime('%Y-%m-%d'),
                shopname=shopnameinfo['shopnameid'],
                corporation=shopnameinfo['superior']
            )
            punish.save()
            imginfo = base64_to_jpg(canvas, 'photos/' + str(id))
            img = Punishimg(img_url=imginfo, for_id=punish.id)
            img.save()

        sql = """select mainid from picturessoninfo where id='{}' ;""".format(id)
        mainid = SaveInfo().select(sql)
        sql = """select sum(isok), count(id), count(id)-sum(isok) from picturessoninfo where mainid='{}' ;""".format(mainid[0][0])
        picturessoninfo = SaveInfo().select(sql)[0]

        sql = """update picturesmaininfo set oknumber='{}', number='{}', nonumber='{}'  where id='{}';""".format(int(picturessoninfo[0]), int(picturessoninfo[1]), int(picturessoninfo[2]), int(mainid[0][0]))
        SaveInfo().add_date_one(sql=sql)

        return render(request, 'monitor/handle_pic.html')

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


def seeperformance(request):
    info = list(Performance.objects.filter(isus=1, post=request.POST.get('post'), project="OA").all().values())
    return JsonResponse({'info': info})


def seefen(request):
    info = Performance.objects.filter(id=request.POST.get('performance')).all().values()[0]
    print(info)
    return JsonResponse({'info': info})


class SaveInfo:

    def __init__(self):
        self.conn = pymysql.connect(
            host='192.168.0.115',
            port=3306,
            user='root',
            password='root',
            database='stuhu',
            charset='utf8'
        )

        self.cursor = self.conn.cursor()
        self.cursor_lock = threading.Lock()

    def make_db(self, repeat_measurement, make_new_form_sql):
        if not self.cursor.execute(repeat_measurement).fetchall():
            self.cursor.execute(make_new_form_sql)
            self.conn.commit()

        # 添加单条数据

    def add_date_one(self, sql):
        with self.cursor_lock:
            self.cursor.execute(sql)
        self.conn.commit()

        # 添加多条数据

    def select(self, sql):
        self.cursor.execute(sql)
        info = self.cursor.fetchall()
        return info

    def add_dates(self, sql, list):
        with self.cursor_lock:
            self.cursor.executemany(sql, list)
        self.conn.commit()


    def search_wecharinfo(self):
        sql = """select * from wechat_message where status='0';"""
        info = self.select(sql)
        return info

    def updatestatus_wecharinfo(self, wechatid):
        sql = """update wechat_message set status='1',send_datatime=now() where id='{}';""".format(wechatid)
        self.add_date_one(sql)
