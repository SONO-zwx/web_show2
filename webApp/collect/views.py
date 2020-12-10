import numpy
import pandas
import datetime

from django.http import JsonResponse
from rest_framework.views import APIView
from sqlalchemy import create_engine
from django.shortcuts import render
from webApp.collect.models import Shopname, Mouthinfo


# Create your views here.
# 周汇总信息
class week_collect(APIView):

    def get(self, request):
        search_info = request.GET
        StartTime = search_info.get('starttime', '')
        EndTime = search_info.get('endtime', '')
        if StartTime == '' or EndTime == '':
            StartTime = str((datetime.date.today() + datetime.timedelta(days=-8)).strftime("%Y-%m-%d"))
            EndTime = str((datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d"))
        ShopName = request.session.get('ShopName')
        nowshopname = request.session.get('nowshopname')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        if nowshopname != '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
            sql = """select InstallationTime from collect where ShopName='{}';""".format(nowshopname)
            df_info = pandas.read_sql_query(sql, engine)

            min_date = str(min(df_info['InstallationTime'].values))
            max_date = str(max(df_info['InstallationTime'].values))

            sql = """select * from collect where ShopName='{}' and InstallationTime Between '{}' And '{}';""".format(
                nowshopname, StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)

            if StartTime == '' or EndTime == '':
                return render(request, 'collect/week_collect.html')
            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = nowshopname
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return 'ok'

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName='{}' and post like '%%美容%%';""".format(nowshopname)
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            week_df_infos = df_infos.T.to_dict()

            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
            sql = """select * from collect where ShopName='{}' and InstallationTime Between '{}' And '{}';""".format(
                nowshopname, StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)
            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = ShopName
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return render(request, 'collect/week_collect.html',
                              {'post': 'get', 'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'week_df': week_df_infos, 'nowshopname': nowshopname, 'starttime': StartTime,
                               'endtime': EndTime,
                               'limits': request.session.get('limits')}
                              )

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName='{}' and post like '%%美容%%';""".format(nowshopname)
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            staffs_df_infos = df_infos.T.to_dict()
            # 数据库连接
            datas = datassplit(StartTime, EndTime)

            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')

            sql = """select * from collect where ShopName='{}' and InstallationTime Between '{}' And '{}';""".format(
                nowshopname, StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)

            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = ShopName
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return 'ok'

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName='{}' and post like '%%美容%%';""".format(nowshopname)
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)

            if meirong_info.shape[0] != 0:
                meirong_info = meirong_info.groupby(['Start_time', 'End_time', 'contrller'])[
                    'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                    'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                    'ServiceRevenue',
                    'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                    'peopornum', 'performance'].apply(sum)
                indexs = pandas.DataFrame([list(i) for i in meirong_info.index], columns=['a', 'b', 'c'])

                meirong_info['Start_time'] = indexs['a'].values
                meirong_info['End_time'] = indexs['b'].values
                meirong_info['contrller'] = indexs['c'].values
                meirong_info['ShopName'] = ShopName
                meirong_info['list_all'] = round(meirong_info['performance'] / meirong_info['counts'], 2)
                meirong_info['people_days'] = round(meirong_info['peopornum'] / len(datas), 2)
                meirong_info['performance_days'] = round(meirong_info['performance'] / len(datas), 2)
                meirong_info['counts_people'] = round(meirong_info['counts'] / meirong_info['peopornum'], 2)
                meirong_info['Total_guest_are'] = round(meirong_info['performance'] / meirong_info['peopornum'], 2)
                meirong_info['offshore_amplification'] = round(
                    (meirong_info['OffshoreProcurementIncome'] + meirong_info['OffshoreProcurementMargin']) /
                    meirong_info[
                        'peopornum'], 2)
                meirong_info['tuhu_amplification'] = round((meirong_info['performance'] - (
                        meirong_info['OffshoreProcurementIncome'] + meirong_info['OffshoreProcurementMargin'])) /
                                                           meirong_info['peopornum'], 2)
                meirong_info['markup_percentage'] = round(
                    meirong_info['OffshoreProcurementMargin'] / meirong_info['OffshoreProcurementCost'], 2) * 100
                meirong_info = meirong_info.fillna(0)
                meirong_info = meirong_info.replace([numpy.inf, -numpy.inf], 0)

            jixiu_df_info = jixiu_df_info.groupby(['Start_time', 'End_time', 'contrller'])[
                'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                'ServiceRevenue',
                'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                'peopornum', 'performance'].apply(sum)
            indexs = pandas.DataFrame([list(i) for i in jixiu_df_info.index], columns=['a', 'b', 'c'])
            jixiu_df_info['Start_time'] = indexs['a'].values
            jixiu_df_info['End_time'] = indexs['b'].values
            jixiu_df_info['contrller'] = indexs['c'].values
            jixiu_df_info['ShopName'] = ShopName
            jixiu_df_info['list_all'] = round(jixiu_df_info['performance'] / jixiu_df_info['counts'], 2)
            jixiu_df_info['people_days'] = round(jixiu_df_info['peopornum'] / len(datas), 2)
            jixiu_df_info['performance_days'] = round(jixiu_df_info['performance'] / len(datas), 2)
            jixiu_df_info['counts_people'] = round(jixiu_df_info['counts'] / jixiu_df_info['peopornum'], 2)
            jixiu_df_info['Total_guest_are'] = round(jixiu_df_info['performance'] / jixiu_df_info['peopornum'], 2)
            jixiu_df_info['offshore_amplification'] = round(
                (jixiu_df_info['OffshoreProcurementIncome'] + jixiu_df_info['OffshoreProcurementMargin']) /
                jixiu_df_info[
                    'peopornum'], 2)
            jixiu_df_info['tuhu_amplification'] = round((jixiu_df_info['performance'] - (
                    jixiu_df_info['OffshoreProcurementIncome'] + jixiu_df_info['OffshoreProcurementMargin'])) /
                                                        jixiu_df_info['peopornum'], 2)
            jixiu_df_info['markup_percentage'] = round(
                jixiu_df_info['OffshoreProcurementMargin'] / jixiu_df_info['OffshoreProcurementCost'], 2) * 100
            jixiu_df_info = jixiu_df_info.fillna(0)
            jixiu_df_info = jixiu_df_info.replace([numpy.inf, -numpy.inf], 0)

            df_infos = df_infos.groupby(['Start_time', 'End_time'])[
                'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                'ServiceRevenue',
                'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                'peopornum', 'performance'].apply(sum)
            indexs = pandas.DataFrame([list(i) for i in df_infos.index], columns=['a', 'b'])

            df_infos['Start_time'] = indexs['a'].values
            df_infos['End_time'] = indexs['b'].values
            df_infos['contrller'] = '全部'
            df_infos['ShopName'] = ShopName
            df_infos['list_all'] = round(df_infos['performance'] / df_infos['counts'], 2)
            df_infos['people_days'] = round(df_infos['peopornum'] / len(datas), 2)
            df_infos['performance_days'] = round(df_infos['performance'] / len(datas), 2)
            df_infos['counts_people'] = round(df_infos['counts'] / df_infos['peopornum'], 2)
            df_infos['Total_guest_are'] = round(df_infos['performance'] / df_infos['peopornum'], 2)
            df_infos['offshore_amplification'] = round(
                (df_infos['OffshoreProcurementIncome'] + df_infos['OffshoreProcurementMargin']) / df_infos[
                    'peopornum'], 2)
            df_infos['tuhu_amplification'] = round((df_infos['performance'] - (
                    df_infos['OffshoreProcurementIncome'] + df_infos['OffshoreProcurementMargin'])) /
                                                   df_infos['peopornum'], 2)
            df_infos['markup_percentage'] = round(
                df_infos['OffshoreProcurementMargin'] / df_infos['OffshoreProcurementCost'], 2) * 100
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            df_infos = df_infos.astype('str')
            week_df_info = {}
            for i in df_infos.T.to_dict().values():
                week_df_info['info0'] = i
            jixiu_df_info = jixiu_df_info.astype('str')
            for i in jixiu_df_info.T.to_dict().values():
                week_df_info['info1'] = i
            meirong_info = meirong_info.astype('str')

            for i in meirong_info.T.to_dict().values():
                week_df_info['info2'] = i

            return render(
                request, 'collect/week_collect.html',
                {'min_date': min_date, 'max_date': max_date, 'post': 'get', 'ShopName': ShopName, 'name': name,
                 'ShopNames': ShopNames, 'starttime': StartTime, 'endtime': EndTime,
                 'chaweek_df': week_df_info, 'nowshopname': nowshopname,
                 'staffs_df_infos': staffs_df_infos, 'limits': request.session.get('limits')}
            )

        else:
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
            listinfo = [i['shopname'] for i in ShopNames]
            sql = """select InstallationTime from collect where ShopName in {};""".format(tuple(listinfo))
            df_info = pandas.read_sql_query(sql, engine)

            min_date = str(min(df_info['InstallationTime'].values))
            max_date = str(max(df_info['InstallationTime'].values))
            sql = """select * from collect where ShopName in {} and InstallationTime Between '{}' And '{}';""".format(
                tuple(listinfo), StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)

            if StartTime == '' or EndTime == '':
                return render(request, 'collect/week_collect.html')
            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = nowshopname
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return 'ok'

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName='{}' and post like '%%美容%%';""".format(nowshopname)
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            week_df_infos = df_infos.T.to_dict()

            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
            sql = """select * from collect where ShopName in {} and InstallationTime Between '{}' And '{}';""".format(
                tuple(listinfo), StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)
            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = ShopName
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return render(request, 'collect/week_collect.html',
                              {'post': 'get', 'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'week_df': week_df_infos, 'nowshopname': nowshopname, 'starttime': StartTime,
                               'endtime': EndTime,
                               'limits': request.session.get('limits')}
                              )

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName in {} and post like '%%美容%%';""".format(tuple(listinfo))
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            staffs_df_infos = df_infos.T.to_dict()
            # 数据库连接
            datas = datassplit(StartTime, EndTime)

            engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')

            sql = """select * from collect where ShopName in {} and InstallationTime Between '{}' And '{}';""".format(
                tuple(listinfo), StartTime, EndTime)
            df_info = pandas.read_sql_query(sql, engine)

            df_info = df_info.loc[:,
                      ['TechnicalName', 'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost',
                       'HandlingCharge',
                       'ShopGoodsMargin',
                       'OffshoreProcurementMargin', 'InstallationFeeIncome', 'ServiceRevenue',
                       'OtherBeautyServices',
                       'OffshoreProcurementIncome', 'PriceSpread', 'counts', 'peopornum', 'performance']]
            new_df_info = df_info.groupby('TechnicalName').apply(sum)
            new_df_info = round(new_df_info.loc[:,
                                ['TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                                 'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                                 'ServiceRevenue',
                                 'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                                 'peopornum', 'performance']], 2
                                )
            new_df_info['Start_time'] = StartTime
            new_df_info['End_time'] = EndTime
            new_df_info['TechnicalName'] = new_df_info.index
            new_df_info['ShopName'] = ShopName
            new_df_info['list_all'] = round(new_df_info['performance'] / new_df_info['counts'], 2)
            new_df_info['days'] = df_info.groupby('TechnicalName').count()['TotalSales']
            new_df_info['people_days'] = round(new_df_info['peopornum'] / new_df_info['days'], 2)
            new_df_info['performance_days'] = round(new_df_info['performance'] / new_df_info['days'], 2)
            new_df_info['counts_people'] = round(new_df_info['counts'] / new_df_info['peopornum'], 2)
            new_df_info['Total_guest_are'] = round(new_df_info['performance'] / new_df_info['peopornum'], 2)
            new_df_info['offshore_amplification'] = round(
                (new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin']) / new_df_info[
                    'peopornum'], 2)
            new_df_info['tuhu_amplification'] = round((new_df_info['performance'] - (
                    new_df_info['OffshoreProcurementIncome'] + new_df_info['OffshoreProcurementMargin'])) /
                                                      new_df_info['peopornum'], 2)
            new_df_info['markup_percentage'] = round(
                new_df_info['OffshoreProcurementMargin'] / new_df_info['OffshoreProcurementCost'], 2) * 100
            df_infos = new_df_info

            if df_infos.shape[0] == 0:
                return 'ok'

            df_infos.index = numpy.arange(len(df_infos.index))
            df_infos = df_infos.fillna(0)
            meirong_info = pandas.DataFrame()
            jixiu_df_info = pandas.DataFrame()

            sql = """select staffname from staff where ShopName in {} and post like '%%美容%%';""".format(tuple(listinfo))
            staff = pandas.read_sql_query(sql, engine)
            for index, data in df_infos.iterrows():
                if df_infos.loc[index, 'TechnicalName'] in list(staff['staffname'].values):
                    meirong_info = meirong_info.append(df_infos.loc[index, :])
                else:
                    jixiu_df_info = jixiu_df_info.append(df_infos.loc[index, :])

            meirong_info['contrller'] = '美容'
            jixiu_df_info['contrller'] = '机修'
            df_infos = pandas.DataFrame()
            df_infos = df_infos.append(meirong_info)
            df_infos = df_infos.append(jixiu_df_info)
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)

            if meirong_info.shape[0] != 0:
                meirong_info = meirong_info.groupby(['Start_time', 'End_time', 'contrller'])[
                    'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                    'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                    'ServiceRevenue',
                    'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                    'peopornum', 'performance'].apply(sum)
                indexs = pandas.DataFrame([list(i) for i in meirong_info.index], columns=['a', 'b', 'c'])

                meirong_info['Start_time'] = indexs['a'].values
                meirong_info['End_time'] = indexs['b'].values
                meirong_info['contrller'] = indexs['c'].values
                meirong_info['ShopName'] = ShopName
                meirong_info['list_all'] = round(meirong_info['performance'] / meirong_info['counts'], 2)
                meirong_info['people_days'] = round(meirong_info['peopornum'] / len(datas), 2)
                meirong_info['performance_days'] = round(meirong_info['performance'] / len(datas), 2)
                meirong_info['counts_people'] = round(meirong_info['counts'] / meirong_info['peopornum'], 2)
                meirong_info['Total_guest_are'] = round(meirong_info['performance'] / meirong_info['peopornum'], 2)
                meirong_info['offshore_amplification'] = round(
                    (meirong_info['OffshoreProcurementIncome'] + meirong_info['OffshoreProcurementMargin']) /
                    meirong_info[
                        'peopornum'], 2)
                meirong_info['tuhu_amplification'] = round((meirong_info['performance'] - (
                        meirong_info['OffshoreProcurementIncome'] + meirong_info['OffshoreProcurementMargin'])) /
                                                           meirong_info['peopornum'], 2)
                meirong_info['markup_percentage'] = round(
                    meirong_info['OffshoreProcurementMargin'] / meirong_info['OffshoreProcurementCost'], 2) * 100
                meirong_info = meirong_info.fillna(0)
                meirong_info = meirong_info.replace([numpy.inf, -numpy.inf], 0)

            jixiu_df_info = jixiu_df_info.groupby(['Start_time', 'End_time', 'contrller'])[
                'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                'ServiceRevenue',
                'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                'peopornum', 'performance'].apply(sum)
            indexs = pandas.DataFrame([list(i) for i in jixiu_df_info.index], columns=['a', 'b', 'c'])
            jixiu_df_info['Start_time'] = indexs['a'].values
            jixiu_df_info['End_time'] = indexs['b'].values
            jixiu_df_info['contrller'] = indexs['c'].values
            jixiu_df_info['ShopName'] = ShopName
            jixiu_df_info['list_all'] = round(jixiu_df_info['performance'] / jixiu_df_info['counts'], 2)
            jixiu_df_info['people_days'] = round(jixiu_df_info['peopornum'] / len(datas), 2)
            jixiu_df_info['performance_days'] = round(jixiu_df_info['performance'] / len(datas), 2)
            jixiu_df_info['counts_people'] = round(jixiu_df_info['counts'] / jixiu_df_info['peopornum'], 2)
            jixiu_df_info['Total_guest_are'] = round(jixiu_df_info['performance'] / jixiu_df_info['peopornum'], 2)
            jixiu_df_info['offshore_amplification'] = round(
                (jixiu_df_info['OffshoreProcurementIncome'] + jixiu_df_info['OffshoreProcurementMargin']) /
                jixiu_df_info[
                    'peopornum'], 2)
            jixiu_df_info['tuhu_amplification'] = round((jixiu_df_info['performance'] - (
                    jixiu_df_info['OffshoreProcurementIncome'] + jixiu_df_info['OffshoreProcurementMargin'])) /
                                                        jixiu_df_info['peopornum'], 2)
            jixiu_df_info['markup_percentage'] = round(
                jixiu_df_info['OffshoreProcurementMargin'] / jixiu_df_info['OffshoreProcurementCost'], 2) * 100
            jixiu_df_info = jixiu_df_info.fillna(0)
            jixiu_df_info = jixiu_df_info.replace([numpy.inf, -numpy.inf], 0)

            df_infos = df_infos.groupby(['Start_time', 'End_time'])[
                'TotalSales', 'TuHuProductCosts', 'OffshoreProcurementCost', 'HandlingCharge',
                'ShopGoodsMargin', 'OffshoreProcurementMargin', 'InstallationFeeIncome',
                'ServiceRevenue',
                'OtherBeautyServices', 'OffshoreProcurementIncome', 'PriceSpread', 'counts',
                'peopornum', 'performance'].apply(sum)
            indexs = pandas.DataFrame([list(i) for i in df_infos.index], columns=['a', 'b'])

            df_infos['Start_time'] = indexs['a'].values
            df_infos['End_time'] = indexs['b'].values
            df_infos['contrller'] = '全部'
            df_infos['ShopName'] = ShopName
            df_infos['list_all'] = round(df_infos['performance'] / df_infos['counts'], 2)
            df_infos['people_days'] = round(df_infos['peopornum'] / len(datas), 2)
            df_infos['performance_days'] = round(df_infos['performance'] / len(datas), 2)
            df_infos['counts_people'] = round(df_infos['counts'] / df_infos['peopornum'], 2)
            df_infos['Total_guest_are'] = round(df_infos['performance'] / df_infos['peopornum'], 2)
            df_infos['offshore_amplification'] = round(
                (df_infos['OffshoreProcurementIncome'] + df_infos['OffshoreProcurementMargin']) / df_infos[
                    'peopornum'], 2)
            df_infos['tuhu_amplification'] = round((df_infos['performance'] - (
                    df_infos['OffshoreProcurementIncome'] + df_infos['OffshoreProcurementMargin'])) /
                                                   df_infos['peopornum'], 2)
            df_infos['markup_percentage'] = round(
                df_infos['OffshoreProcurementMargin'] / df_infos['OffshoreProcurementCost'], 2) * 100
            df_infos = df_infos.fillna(0)
            df_infos = df_infos.replace([numpy.inf, -numpy.inf], 0)
            df_infos = df_infos.astype('str')
            week_df_info = {}
            for i in df_infos.T.to_dict().values():
                week_df_info['info0'] = i
            jixiu_df_info = jixiu_df_info.astype('str')
            for i in jixiu_df_info.T.to_dict().values():
                week_df_info['info1'] = i
            meirong_info = meirong_info.astype('str')

            for i in meirong_info.T.to_dict().values():
                week_df_info['info2'] = i

            return render(
                request, 'collect/week_collect.html',
                {'min_date': min_date, 'max_date': max_date, 'post': 'get', 'ShopName': ShopName,
                 'name': name, 'ShopNames': ShopNames, 'starttime': StartTime, 'endtime': EndTime,
                 'chaweek_df': week_df_info, 'nowshopname': nowshopname,
                 'staffs_df_infos': staffs_df_infos, 'limits': request.session.get('limits')}
            )


# 日汇总信息
class day_collect(APIView):

    def get(self, request):

        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
        nowshopname = request.session.get('nowshopname')
        superior = request.session.get('superior')
        starttime = request.GET.get('starttime')
        endtime = request.GET.get('endtime')

        if nowshopname == '总部':
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            listinfo = tuple([i['shopname'] for i in ShopNames])
            sql = """select InstallationTime from collect where ShopName in {};""".format(listinfo)
            df_info = pandas.read_sql_query(sql, engine)
            min_date = str(min(df_info['InstallationTime'].values))
            max_date = str(max(df_info['InstallationTime'].values))
            sql = """select * from collect where ShopName in {} and InstallationTime between '{}' and '{}' order by TechnicalName,InstallationTime;""".format(
                listinfo, starttime, endtime)
            df_info = pandas.read_sql_query(sql, engine)
            df_info['markup_percentage'] = round(df_info['markup_percentage'] * 100, 2)
            df_info = df_info.T.to_dict()

        else:
            sql = """select InstallationTime from collect where ShopName='{}';""".format(nowshopname)
            df_info = pandas.read_sql_query(sql, engine)
            min_date = str(min(df_info['InstallationTime'].values))
            max_date = str(max(df_info['InstallationTime'].values))
            sql = """select * from collect where ShopName = '{}' and InstallationTime between '{}' and '{}' order by TechnicalName,InstallationTime;""".format(
                nowshopname, starttime, endtime)
            df_info = pandas.read_sql_query(sql, engine)
            df_info['markup_percentage'] = round(df_info['markup_percentage'] * 100, 2)
            df_info = df_info.T.to_dict()

        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/day_collect.html',
                      {'min_date': min_date, 'max_date': max_date, 'df_info': df_info, 'nowshopname': nowshopname,
                       'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames, 'starttime': starttime,
                       'endtime': endtime,
                       'limits': request.session.get('limits')})


class month_collect(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        superior = request.session.get('superior')
        limits = request.session.get('limits')
        name = request.session.get('name')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/month_collect.html',
                      {'nowshopname': nowshopname, 'ShopName': ShopName, 'name': name,
                       'ShopNames': ShopNames, 'limits': request.session.get('limits')})

    def post(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
        nowshopname = request.session.get('nowshopname')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        shopname = request.POST.get('shopname')
        searchinfo = {
            'starttime': starttime,
            'endtime': endtime,
            'shopname': shopname
        }

        if starttime != '' and endtime != '' and shopname != '' and starttime < endtime:
            nowinfo = Mouthinfo.objects.filter(starttime=starttime, endtime=endtime, shopname=shopname,
                                               type='实际').all().values()
            if len(nowinfo) == 0 or request.POST.get('save') == 'ok':
                sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                nowinfo = {}
                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])
                nowinfo['chengbenxiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3

                nowinfo['one'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['three'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname, starttime, endtime)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])
                nowinfo['xiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3

                nowinfo['daione'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['daitwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['daithree'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' and two in ( '大客户代付') order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3
                nowinfo['yinone'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['yintwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['yinthree'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                try:
                    if df_info[0]['金额']:
                        nowinfo['应收金额'] = df_info[0]['金额']
                    else:
                        nowinfo['应收金额'] = 0.0
                except:
                    nowinfo['应收金额'] = 0.0
                sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已完成', '资料审批', '资料审批驳回','资料补充', '已打款');""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['成本合计'] = df_info[0]['金额']
                else:
                    nowinfo['成本合计'] = 0.0

                sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' );""".format(
                    starttime, endtime, shopname, starttime, endtime)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['应付收入'] = df_info[0]['金额']
                else:
                    nowinfo['应付收入'] = 0.0

                sql = """select sum(allprice) '金额' from income where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['其他收入'] = df_info[0]['金额']
                else:
                    nowinfo['其他收入'] = 0.0

                sql = """select sum(zhimanay) '金额' from wastesubsidiary where datetimes between '{}' and '{}' and wastepro ='危废交易单' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['危废收入'] = df_info[0]['金额']
                else:
                    nowinfo['危废收入'] = 0.0

                if request.POST.get('save') == 'ok':
                    mouthinfo = Mouthinfo(
                        shopname=shopname,
                        starttime=starttime,
                        endtime=endtime,
                        type='实际',
                        info=nowinfo
                    )
                    mouthinfo.save()
                ShopName = request.session.get('ShopName')
                name = request.session.get('name')
                superior = request.session.get('superior')
                ShopNames = Shopname.objects.filter(superior=superior).all().values()
                return render(request, 'collect/month_collect.html',
                              {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                               'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'limits': request.session.get('limits'), 'nowinfo': nowinfo})
            else:
                nowinfo = eval(nowinfo[0]['info'])
                ShopName = request.session.get('ShopName')
                name = request.session.get('name')
                superior = request.session.get('superior')
                ShopNames = Shopname.objects.filter(superior=superior).all().values()
                return render(request, 'collect/month_collect.html',
                              {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                               'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'limits': request.session.get('limits'), 'nowinfo': nowinfo})
        else:

            ShopName = request.session.get('ShopName')
            name = request.session.get('name')
            superior = request.session.get('superior')
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            return render(request, 'collect/month_collect.html',
                          {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                           'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                           'limits': request.session.get('limits'), 'nowinfo': None})


def xiangqing(request):
    info = request.GET
    type = info.get('type')
    starttime = info.get('starttime', '')
    endtime = info.get('endtime', '')
    project = info.get('project')
    shopname = info.get('shopname')
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
    info = {}
    info['project'] = project
    if starttime != '' and endtime != '':
        if type == '收入类':
            if project == '危废收入':
                sql = """select wastesdealinfo.wastepro '项目名称', wastesdealinfo.zhimanay '金额' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes between '{}' and '{}' and wastesubsidiary.wastepro ='危废交易单' and wastesubsidiary.status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)

            elif project == '其他收入':
                sql = """select  income_dealproject.project_name '项目名称', income_dealproject.amount '金额' from income left join income_dealproject on income.id=income_dealproject.for_id  where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
            elif project == '应收金额':
                sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types in ( '大客户代付');""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
            else:
                df_info = pandas.DataFrame()
        elif type == '支出类':
            sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types='{}';""".format(
                starttime, endtime, shopname, project)
            df_info = pandas.read_sql_query(sql, engine)
        elif type == '应付类':
            sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and  (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) and dealproject.types='{}';""".format(
                starttime, endtime, shopname, starttime, endtime, project)
            df_info = pandas.read_sql_query(sql, engine)
        elif type == '应收类':
            sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types='{}';""".format(
                starttime, endtime, shopname, project)
            df_info = pandas.read_sql_query(sql, engine)
        else:
            df_info = pandas.DataFrame()
    else:
        df_info = pandas.DataFrame()

    if int(len(df_info) % 3) > 0:
        lenth = (len(df_info) // 3) + 1
    else:
        lenth = len(df_info) // 3

    info['one'] = list(df_info[0:lenth].T.to_dict().values())
    info['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
    info['three'] = list(df_info[lenth * 2:].T.to_dict().values())
    return render(request, 'collect/xiangqing.html', {'nowinfo': info})


def fenxiangqing(request):
    info = request.GET
    type = info.get('type')
    starttime = info.get('starttime', '')
    endtime = info.get('endtime', '')
    project = info.get('project')
    shopname = info.get('shopname')
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
    info = {}
    info['project'] = project
    if starttime != '' and endtime != '':
        if type == '收入类':
            if project == '危废收入':
                sql = """select wastesdealinfo.wastepro '项目名称', wastesdealinfo.zhimanay '金额' from wastesubsidiary left join wastesdealinfo on wastesubsidiary.id=wastesdealinfo.forid where datetimes between '{}' and '{}' and wastesubsidiary.wastepro ='危废交易单' and wastesubsidiary.status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)

            elif project == '其他收入':
                sql = """select  income_dealproject.project_name '项目名称', income_dealproject.amount '金额' from income left join income_dealproject on income.id=income_dealproject.for_id  where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
            elif project == '应收金额':
                sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types in ( '大客户代付');""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
            else:
                df_info = pandas.DataFrame()
        elif type == '支出类':
            sql = """select dealproject.projectname '项目名称',dealproject.price/receipts.tantimes '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where (receipts.zhidates between '{}' and '{}' or '{}' between receipts.tanstarttime and receipts.tanendtime or '{}' between receipts.tanstarttime and receipts.tanendtime)  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types='{}';""".format(
                starttime, endtime, starttime, endtime, shopname, project)
            df_info = pandas.read_sql_query(sql, engine)
        elif type == '应付类':
            sql = """select dealproject.projectname '项目名称',dealproject.price/receipts.tantimes '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where (receipts.dates between '{}' and '{}' or '{}' between receipts.tanstarttime and receipts.tanendtime or '{}' between receipts.tanstarttime and receipts.tanendtime)  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) and dealproject.types='{}';""".format(
                starttime, endtime, starttime, endtime, shopname, project)
            df_info = pandas.read_sql_query(sql, engine)
        elif type == '应收类':
            sql = """select dealproject.projectname '项目名称',dealproject.price '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') and dealproject.types='{}';""".format(
                starttime, endtime, shopname, project)
            df_info = pandas.read_sql_query(sql, engine)
        else:
            df_info = pandas.DataFrame()
    else:
        df_info = pandas.DataFrame()

    if int(len(df_info) % 3) > 0:
        lenth = (len(df_info) // 3) + 1
    else:
        lenth = len(df_info) // 3

    info['one'] = list(df_info[0:lenth].T.to_dict().values())
    info['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
    info['three'] = list(df_info[lenth * 2:].T.to_dict().values())

    return render(request, 'collect/xiangqing.html', {'nowinfo': info})


class year_collect(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        superior = request.session.get('superior')
        limits = request.session.get('limits')
        name = request.session.get('name')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/year_collect.html',
                      {'nowshopname': nowshopname, 'ShopName': ShopName, 'name': name,
                       'ShopNames': ShopNames, 'limits': request.session.get('limits')})

    def post(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
        nowshopname = request.session.get('nowshopname')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        shopname = request.POST.get('shopname')
        searchinfo = {
            'starttime': starttime,
            'endtime': endtime,
            'shopname': shopname
        }
        sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
        df_info1 = pandas.read_sql_query(sql, engine)

        nowinfo = {}
        df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                        ascending=False,
                                                                                                        by=['一级分类'])
        nowinfo['chengbenxiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

        if int(len(df_info) % 3) > 0:
            lenth = (len(df_info) // 3) + 1
        else:
            lenth = len(df_info) // 3

        nowinfo['one'] = list(df_info[0:lenth].T.to_dict().values())
        nowinfo['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
        nowinfo['three'] = list(df_info[lenth * 2:].T.to_dict().values())

        sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) group by receipts.types,dealproject.types ;""".format(
            starttime, endtime, shopname, starttime, endtime)
        df_info = pandas.read_sql_query(sql, engine)
        sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
        df_info1 = pandas.read_sql_query(sql, engine)

        df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                        ascending=False,
                                                                                                        by=['一级分类'])
        nowinfo['xiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

        if int(len(df_info) % 3) > 0:
            lenth = (len(df_info) // 3) + 1
        else:
            lenth = len(df_info) // 3

        nowinfo['daione'] = list(df_info[0:lenth].T.to_dict().values())
        nowinfo['daitwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
        nowinfo['daithree'] = list(df_info[lenth * 2:].T.to_dict().values())
        sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已完成', '资料审批', '资料审批驳回','资料补充', '已打款');""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['成本合计'] = df_info[0]['金额']
        else:
            nowinfo['成本合计'] = 0.0

        sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' );""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['应付收入'] = df_info[0]['金额']
        else:
            nowinfo['应付收入'] = 0.0

        sql = """select sum(allprice) '金额' from income where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['其他收入'] = df_info[0]['金额']
        else:
            nowinfo['其他收入'] = 0.0

        sql = """select sum(zhimanay) '金额' from wastesubsidiary where datetimes between '{}' and '{}' and wastepro ='危废交易单' and status='已完成' and shopname='{}';""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['危废收入'] = df_info[0]['金额']
        else:
            nowinfo['危废收入'] = 0.0

        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/month_collect.html',
                      {'df_info': df_info, 'nowshopname': nowshopname, 'searchinfo': searchinfo,
                       'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                       'limits': request.session.get('limits'), 'nowinfo': nowinfo})


class fenyear_collect(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        superior = request.session.get('superior')
        limits = request.session.get('limits')
        name = request.session.get('name')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/fenyear_collect.html',
                      {'nowshopname': nowshopname, 'ShopName': ShopName, 'name': name,
                       'ShopNames': ShopNames, 'limits': request.session.get('limits')})

    def post(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
        nowshopname = request.session.get('nowshopname')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        shopname = request.POST.get('shopname')
        searchinfo = {
            'starttime': starttime,
            'endtime': endtime,
            'shopname': shopname
        }
        sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
        df_info1 = pandas.read_sql_query(sql, engine)

        nowinfo = {}
        df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                        ascending=False,
                                                                                                        by=['一级分类'])
        nowinfo['chengbenxiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

        if int(len(df_info) % 3) > 0:
            lenth = (len(df_info) // 3) + 1
        else:
            lenth = len(df_info) // 3

        nowinfo['one'] = list(df_info[0:lenth].T.to_dict().values())
        nowinfo['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
        nowinfo['three'] = list(df_info[lenth * 2:].T.to_dict().values())

        sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) group by receipts.types,dealproject.types ;""".format(
            starttime, endtime, shopname, starttime, endtime)
        df_info = pandas.read_sql_query(sql, engine)
        sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
        df_info1 = pandas.read_sql_query(sql, engine)

        df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                        ascending=False,
                                                                                                        by=['一级分类'])
        nowinfo['xiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

        if int(len(df_info) % 3) > 0:
            lenth = (len(df_info) // 3) + 1
        else:
            lenth = len(df_info) // 3

        nowinfo['daione'] = list(df_info[0:lenth].T.to_dict().values())
        nowinfo['daitwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
        nowinfo['daithree'] = list(df_info[lenth * 2:].T.to_dict().values())
        sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已完成', '资料审批', '资料审批驳回','资料补充', '已打款');""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['成本合计'] = df_info[0]['金额']
        else:
            nowinfo['成本合计'] = 0.0

        sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' );""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['应付收入'] = df_info[0]['金额']
        else:
            nowinfo['应付收入'] = 0.0

        sql = """select sum(allprice) '金额' from income where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['其他收入'] = df_info[0]['金额']
        else:
            nowinfo['其他收入'] = 0.0

        sql = """select sum(zhimanay) '金额' from wastesubsidiary where datetimes between '{}' and '{}' and wastepro ='危废交易单' and status='已完成' and shopname='{}';""".format(
            starttime, endtime, shopname)
        df_info = pandas.read_sql_query(sql, engine)
        df_info = list(df_info.T.to_dict().values())
        if df_info[0]['金额']:
            nowinfo['危废收入'] = df_info[0]['金额']
        else:
            nowinfo['危废收入'] = 0.0

        ShopName = request.session.get('ShopName')
        limits = request.session.get('limits')
        name = request.session.get('name')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/month_collect.html',
                      {'df_info': df_info, 'nowshopname': nowshopname, 'searchinfo': searchinfo,
                       'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                       'limits': request.session.get('limits'), 'nowinfo': nowinfo})


class fenmonth_collect(APIView):

    def get(self, request):
        nowshopname = request.session.get('nowshopname')
        superior = request.session.get('superior')
        limits = request.session.get('limits')
        name = request.session.get('name')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        return render(request, 'collect/fenmonth_collect.html',
                      {'nowshopname': nowshopname, 'ShopName': ShopName, 'name': name,
                       'ShopNames': ShopNames, 'limits': request.session.get('limits')})

    def post(self, request):
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/stuhu')
        nowshopname = request.session.get('nowshopname')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        shopname = request.POST.get('shopname')
        searchinfo = {
            'starttime': starttime,
            'endtime': endtime,
            'shopname': shopname
        }
        if starttime != '' and endtime != '' and shopname != '' and starttime < endtime:
            nowinfo = Mouthinfo.objects.filter(starttime=starttime, endtime=endtime, shopname=shopname,
                                               type='分摊').all().values()
            if len(nowinfo) == 0 or request.POST.get('save') == 'ok':
                sql = """select receipts.types '一级分类',dealproject.types '二级分类',round(sum(dealproject.price/receipts.tantimes), 2) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where (receipts.zhidates between '{}' and '{}' or '{}' between receipts.tanstarttime and receipts.tanendtime or '{}' between receipts.tanstarttime and receipts.tanendtime) and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                nowinfo = {}
                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])
                nowinfo['chengbenxiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3

                nowinfo['one'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['two'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['three'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select receipts.types '一级分类',dealproject.types '二级分类',round(sum(dealproject.price/receipts.tantimes), 2) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where  (receipts.zhidates between '{}' and '{}' or '{}' between receipts.tanstarttime and receipts.tanendtime or '{}' between receipts.tanstarttime and receipts.tanendtime) and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' ) group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, starttime, endtime, shopname, starttime, endtime)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])
                nowinfo['xiaoji'] = list(df_info.groupby(['一级分类'])['金额'].sum().reset_index().to_dict().values())

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3

                nowinfo['daione'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['daitwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['daithree'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select receipts.types '一级分类',dealproject.types '二级分类',sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                sql = """select one '一级分类',two '二级分类' from newcategory where classname='支出单据' and two in ('大客户代付') order by 'one';"""
                df_info1 = pandas.read_sql_query(sql, engine)

                df_info = pandas.merge(df_info1, df_info, on=['一级分类', '二级分类'], how='left').fillna(0).sort_index(axis=0,
                                                                                                                ascending=False,
                                                                                                                by=[
                                                                                                                    '一级分类'])

                if int(len(df_info) % 3) > 0:
                    lenth = (len(df_info) // 3) + 1
                else:
                    lenth = len(df_info) // 3

                nowinfo['yinone'] = list(df_info[0:lenth].T.to_dict().values())
                nowinfo['yintwo'] = list(df_info[lenth:lenth * 2].T.to_dict().values())
                nowinfo['yinthree'] = list(df_info[lenth * 2:].T.to_dict().values())

                sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.zhidates between '{}' and '{}' and dealproject.types in ( '大客户代付') and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('待打款', '待月结', '已月结', '已完成', '资料审批', '资料审批驳回','资料补充', '已打款') group by receipts.types,dealproject.types ;""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                try:
                    if df_info[0]['金额']:
                        nowinfo['应收金额'] = df_info[0]['金额']
                    else:
                        nowinfo['应收金额'] = 0.0
                except:
                    nowinfo['应收金额'] = 0.0

                sql = """select round(sum(dealproject.price/receipts.tantimes), 2) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where (receipts.zhidates between '{}' and '{}' or '{}' between receipts.tanstarttime and receipts.tanendtime or '{}' between receipts.tanstarttime and receipts.tanendtime) and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and paymenttyoe in ('已完成', '资料审批', '资料审批驳回','资料补充', '已打款');""".format(
                    starttime, endtime, endtime, starttime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['成本合计'] = df_info[0]['金额']
                else:
                    nowinfo['成本合计'] = 0.0

                sql = """select sum(dealproject.price) '金额' from receipts left join dealproject on receipts.id = dealproject.receiptsid where receipts.dates between '{}' and '{}'  and receipts.types!='外采' and receipts.types!='外采退换货' and shopname='{}' and (paymenttyoe in ('待打款', '待月结') or receipts.zhidates not between '{}' and '{}' );""".format(
                    starttime, endtime, shopname, starttime, endtime)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['应付收入'] = df_info[0]['金额']
                else:
                    nowinfo['应付收入'] = 0.0

                sql = """select sum(allprice) '金额' from income where zhidates between '{}' and '{}' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['其他收入'] = df_info[0]['金额']
                else:
                    nowinfo['其他收入'] = 0.0

                sql = """select sum(zhimanay) '金额' from wastesubsidiary where datetimes between '{}' and '{}' and wastepro ='危废交易单' and status='已完成' and shopname='{}';""".format(
                    starttime, endtime, shopname)
                df_info = pandas.read_sql_query(sql, engine)
                df_info = list(df_info.T.to_dict().values())
                if df_info[0]['金额']:
                    nowinfo['危废收入'] = df_info[0]['金额']
                else:
                    nowinfo['危废收入'] = 0.0

                if request.POST.get('save') == 'ok':
                    mouthinfo = Mouthinfo(
                        shopname=shopname,
                        starttime=starttime,
                        endtime=endtime,
                        type='分摊',
                        info=nowinfo
                    )
                    mouthinfo.save()
                ShopName = request.session.get('ShopName')
                limits = request.session.get('limits')
                name = request.session.get('name')
                superior = request.session.get('superior')
                ShopNames = Shopname.objects.filter(superior=superior).all().values()
                return render(request, 'collect/fenmonth_collect.html',
                              {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                               'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'limits': request.session.get('limits'), 'nowinfo': nowinfo})
            else:
                nowinfo = eval(nowinfo[0]['info'])
                ShopName = request.session.get('ShopName')
                name = request.session.get('name')
                superior = request.session.get('superior')
                ShopNames = Shopname.objects.filter(superior=superior).all().values()
                return render(request, 'collect/month_collect.html',
                              {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                               'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                               'limits': request.session.get('limits'), 'nowinfo': nowinfo})
        else:
            ShopName = request.session.get('ShopName')
            limits = request.session.get('limits')
            name = request.session.get('name')
            superior = request.session.get('superior')
            ShopNames = Shopname.objects.filter(superior=superior).all().values()
            return render(request, 'collect/fenmonth_collect.html',
                          {'nowshopname': nowshopname, 'searchinfo': searchinfo,
                           'ShopName': ShopName, 'name': name, 'ShopNames': ShopNames,
                           'limits': request.session.get('limits'), 'nowinfo': None})


# 日期拆分
def datassplit(StartTime, EndTime):
    dt = datetime.datetime.strptime(StartTime, "%Y-%m-%d")
    end_dt = datetime.datetime.strptime(EndTime, "%Y-%m-%d")

    dates = []

    while dt <= end_dt:
        dates.append(dt.strftime("%Y-%m-%d"))
        if dt == end_dt:
            return dates
        dt = dt + datetime.timedelta(days=1)


class Technician_data(APIView):
    def get(self, request):
        starttime = request.GET.get('starttime',
                                    str((datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")))
        endtime = request.GET.get('endtime',
                                  str((datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")))
        shopname = request.GET.get('shopname', request.session.get('nowshopname'))
        staffsname = request.GET.get('staffsname', '无')
        name = request.session.get('name')
        ShopName = request.session.get('ShopName')
        superior = request.session.get('superior')
        ShopNames = Shopname.objects.filter(superior=superior).all().values()
        data = getinfo(starttime=starttime, endtime=endtime, shopname=shopname, staffsname=staffsname)
        datas = getcommentinfo(starttime=starttime, endtime=endtime, shopname=shopname, staffsname=staffsname)
        staffsnamelist = get_staff(starttime=starttime, endtime=endtime, shopname=shopname)
        return render(request, 'collect/technician_data.html',
                      {'nowshopname': shopname, 'ShopName': ShopName, 'name': name, 'size': len(data['data']),
                       'zongyeji': data['zongyeji'],
                       'ShopNames': ShopNames, 'limits': request.session.get('limits'), 'data': data['data'],
                       'starttime': starttime, 'staffsname': staffsname, 'staffsnamelist': staffsnamelist, 'datas': datas,
                       'endtime': endtime})

    def post(self, request):
        return render(request, 'collect/technician_data.html')


def get_staffs(request):
    starttime = request.POST.get('starttime')
    endtime = request.POST.get('endtime')
    shopname = request.POST.get('shopname')
    engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
    sql = """select distinct TechnicalName from exportorders where exportorders.InstallationTime between '{}' and '{}' and exportorders.ShopName='{}';""".format(
        starttime, endtime, shopname)
    staffsname = pandas.read_sql_query(sql, engine)
    staffsname = [foo for foo in staffsname['TechnicalName']]
    return JsonResponse({'TechnicalName': staffsname})


def get_staff(starttime, endtime, shopname):
    engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
    sql = """select distinct TechnicalName from exportorders where exportorders.InstallationTime between '{}' and '{}' and exportorders.ShopName='{}';""".format(
        starttime, endtime, shopname)
    staffsname = pandas.read_sql_query(sql, engine)
    staffsname = [foo for foo in staffsname['TechnicalName']]
    return staffsname


def getinfo(starttime, endtime, shopname, staffsname):
    engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
    sql = """select  exportorders.*,commoditylist.ProductCode,commoditylist.ProductName,commoditylist.Number,commoditylist.Unit,commoditylist.UnitPrice,commoditylist.TotalPrice,orderdetails.PlateNumber '车牌'  from exportorders left join commoditylist on exportorders.OrderNumber=commoditylist.OrderNumber left join orderdetails on exportorders.OrderNumber=orderdetails.OrderNumber where exportorders.InstallationTime between '{}' and '{}' and exportorders.ShopName='{}' and exportorders.TechnicalName='{}';""".format(
        starttime, endtime, shopname, staffsname)
    df_info_commoditylist = pandas.read_sql_query(sql, engine)
    df_info_commoditylist = df_info_commoditylist.fillna('无')
    sql = """select exportorders.*, orderdetails.PlateNumber '车牌' from exportorders left join orderdetails on exportorders.OrderNumber=orderdetails.OrderNumber where exportorders.InstallationTime between '{}' and '{}' and exportorders.ShopName='{}' and exportorders.TechnicalName='{}';""".format(
        starttime, endtime, shopname, staffsname)
    df_info = pandas.read_sql_query(sql, engine)
    size = df_info.shape
    data = {}
    df_infos = df_info.loc[:,
               ['InstallationTime', 'OrderNumber', 'TuHuProductCosts', '车牌', 'OffshoreProcurementCost',
                'OffshoreProcurementMargin', 'TotalSales', 'OrderWay']]
    df_infos['业绩'] = round(df_info['HandlingCharge'].apply(lambda x: float(x)), 2) + round(
        df_info['ShopGoodsMargin'].apply(lambda x: float(x)), 2) + round(
        df_info['OffshoreProcurementMargin'].apply(lambda x: float(x)), 2) + round(
        df_info['InstallationFeeIncome'].apply(lambda x: float(x)), 2) + round(
        df_info['ServiceRevenue'].apply(lambda x: float(x)), 2) + round(
        df_info['OtherBeautyServices'].apply(lambda x: float(x)), 2) + round(
        df_info['OffshoreProcurementIncome'].apply(lambda x: float(x)), 2) + round(
        df_info['PriceSpread'].apply(lambda x: float(x)), 2) + round(
        df_info['CashPriceSpread'].apply(lambda x: float(x)), 2)
    zongyeji = df_infos['业绩'].sum()
    info = df_infos.groupby('车牌').sum().reset_index()
    for i in info.index:
        data[info.loc[i, '车牌']] = {'业绩': round(info.loc[i, '业绩'], 2)}
    for i in data.keys():
        data[i]['订单'] = [{'订单号': df_infos.loc[foo, 'OrderNumber'],
                          '订单金额': df_infos.loc[foo, '业绩'],
                          '日期': df_infos.loc[foo, 'InstallationTime']} for foo in
                         df_infos[df_infos['车牌'] == i].index]

    df_info_commoditylist['hupin'] = df_info_commoditylist['ProductCode']
    df_info_commoditylist['hupin'] = df_info_commoditylist['hupin'].apply(
        lambda x: '1' if str(x).split('-')[0] not in ['TEMP', 'FU'] else (
            '2' if str(x).split('-')[0] == 'TEMP' else '3'))
    df_info_commoditylist['业绩'] = round(df_info_commoditylist['ShopGoodsMargin'].apply(lambda x: float(x)), 2)
    df_info_commoditylist['其他'] = round(
        df_info_commoditylist['PriceSpread'].apply(lambda x: float(x)), 2) + round(
        df_info_commoditylist['OtherBeautyServices'].apply(lambda x: float(x)), 2) + round(
        df_info_commoditylist['ServiceRevenue'].apply(lambda x: float(x)), 2) + round(
        df_info_commoditylist['HandlingCharge'].apply(lambda x: float(x)), 2) + round(
        df_info_commoditylist['CashPriceSpread'].apply(lambda x: float(x)), 2)
    df_info_commodity_numer = df_info_commoditylist.groupby(['车牌', 'OrderNumber', 'OrderWay', 'hupin']).count().T.to_dict()

    df_info_commoditylist['Number'] = df_info_commoditylist['Number'].apply(
        lambda x: float(str(x).replace('￥', '').replace(' ', '').replace(',', '').replace('无', '0')) if x else 0)
    df_info_commoditylist['OffshoreProcurementMargin'] = df_info_commoditylist['OffshoreProcurementMargin'].apply(
        lambda x: float(str(x).replace('￥', '').replace(' ', '').replace(',', '').replace('无', '0')) if x else 0)
    df_info_commoditylist['OffshoreProcurementCost'] = df_info_commoditylist['OffshoreProcurementCost'].apply(
        lambda x: float(str(x).replace('￥', '').replace(' ', '').replace(',', '').replace('无', '0')) if x else 0)
    df_info_commoditylist['UnitPrice'] = df_info_commoditylist['UnitPrice'].apply(
        lambda x: float(str(x).replace('￥', '').replace(' ', '').replace(',', '').replace('无', '0')) if x else 0)
    df_info_commoditylist['TotalPrice'] = df_info_commoditylist['TotalPrice'].apply(
        lambda x: float(str(x).replace('￥', '').replace(' ', '').replace(',', '').replace('无', '0')) if x else 0)
    df_info_commodity_price = df_info_commoditylist.groupby(['车牌', 'OrderNumber', 'OrderWay', 'hupin']).nth(0).T.to_dict()
    df_info_commodity_gongprice = df_info_commoditylist.groupby(['车牌', 'OrderNumber', 'OrderWay', 'hupin']).sum().T.to_dict()

    for keys, values in data.items():
        data[keys]['虎品业绩'] = 0
        data[keys]['虎品转化业绩'] = 0
        data[keys]['外采业绩'] = 0
        data[keys]['外采成本'] = 0
        data[keys]['外采数量'] = 0
        data[keys]['服务费'] = 0
        data[keys]['虎品数量'] = 0
        data[keys]['虎品转化数量'] = 0
        data[keys]['其他收益'] = 0
        data[keys]['上一订单'] = '无'
        for i in values['订单']:
            if (keys, i['订单号'], '线上', '1') in df_info_commodity_price.keys():
                a = df_info_commodity_price[(keys, i['订单号'], '线上', '1')]['业绩']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '1') in df_info_commodity_price.keys():
                b = df_info_commodity_price[(keys, i['订单号'], '线下', '1')]['业绩']
            else:
                b = 0

            if keys != data[keys]['上一订单'] and data[keys]['上一订单'] != '无':
                data[keys]['虎品转化业绩'] += b + a
            data[keys]['虎品业绩'] += a + b
            if (keys, i['订单号'], '线上', '1') in df_info_commodity_price.keys():
                a = df_info_commodity_price[(keys, i['订单号'], '线上', '1')]['其他']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '1') in df_info_commodity_price.keys():
                b = df_info_commodity_price[(keys, i['订单号'], '线下', '1')]['其他']
            else:
                b = 0
            data[keys]['其他收益'] += a + b

            if (keys, i['订单号'], '线上', '2') in df_info_commodity_price.keys():
                a = df_info_commodity_price[(keys, i['订单号'], '线上', '2')]['OffshoreProcurementCost']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '2') in df_info_commodity_price.keys():
                b = df_info_commodity_price[(keys, i['订单号'], '线下', '2')]['OffshoreProcurementCost']
            else:
                b = 0
            data[keys]['外采成本'] += a + b
            if (keys, i['订单号'], '线上', '2') in df_info_commodity_price.keys():
                a = df_info_commodity_price[(keys, i['订单号'], '线上', '2')]['OffshoreProcurementMargin']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '2') in df_info_commodity_price.keys():
                b = df_info_commodity_price[(keys, i['订单号'], '线下', '2')]['OffshoreProcurementMargin']
            else:
                b = 0
            data[keys]['外采业绩'] += a + b

            if data[keys]['外采成本'] == 0:
                if (keys, i['订单号'], '线上', '1') in df_info_commodity_price.keys():
                    a = df_info_commodity_price[(keys, i['订单号'], '线上', '1')]['OffshoreProcurementCost']
                else:
                    a = 0
                if (keys, i['订单号'], '线下', '1') in df_info_commodity_price.keys():
                    b = df_info_commodity_price[(keys, i['订单号'], '线下', '1')]['OffshoreProcurementCost']
                else:
                    b = 0
                data[keys]['外采成本'] += a + b
            if data[keys]['外采业绩'] == 0:
                if (keys, i['订单号'], '线上', '1') in df_info_commodity_price.keys():
                    a = df_info_commodity_price[(keys, i['订单号'], '线上', '1')]['OffshoreProcurementMargin']
                else:
                    a = 0
                if (keys, i['订单号'], '线下', '1') in df_info_commodity_price.keys():
                    b = df_info_commodity_price[(keys, i['订单号'], '线下', '1')]['OffshoreProcurementMargin']
                else:
                    b = 0
                data[keys]['外采业绩'] += a + b

            if (keys, i['订单号'], '线上', '3') in df_info_commodity_gongprice.keys():
                a = df_info_commodity_gongprice[(keys, i['订单号'], '线上', '3')]['TotalPrice']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '3') in df_info_commodity_gongprice.keys():
                b = df_info_commodity_gongprice[(keys, i['订单号'], '线下', '3')]['TotalPrice']
            else:
                b = 0
            data[keys]['服务费'] += a + b
            if (keys, i['订单号'], '线上', '1') in df_info_commodity_numer.keys():
                a = df_info_commodity_numer[(keys, i['订单号'], '线上', '1')]['InstallationTime']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '1') in df_info_commodity_numer.keys():
                b = df_info_commodity_numer[(keys, i['订单号'], '线下', '1')]['InstallationTime']
            else:
                b = 0
            data[keys]['虎品数量'] += a + b
            if keys != data[keys]['上一订单'] and data[keys]['上一订单'] != '无':
                data[keys]['虎品转化数量'] += b + a
            if (keys, i['订单号'], '线上', '2') in df_info_commodity_numer.keys():
                a = df_info_commodity_numer[(keys, i['订单号'], '线上', '2')]['InstallationTime']
            else:
                a = 0
            if (keys, i['订单号'], '线下', '2') in df_info_commodity_numer.keys():
                b = df_info_commodity_numer[(keys, i['订单号'], '线下', '2')]['InstallationTime']
            else:
                b = 0
            data[keys]['外采数量'] += a + b
            data[keys]['上一订单'] = keys
        try:
            data[keys]['外采加价率'] = round(data[keys]['外采业绩'] / data[keys]['外采成本'], 2)
        except ZeroDivisionError:
            data[keys]['外采加价率'] = 0
        data[keys]['总金额'] = data[keys]['虎品业绩'] + data[keys]['服务费'] + data[keys]['外采业绩']
        try:
            data[keys]['虎品转化金额权重'] = round(data[keys]['虎品转化业绩'] / data[keys]['总金额'], 2) * 100
        except ZeroDivisionError:
            data[keys]['虎品转化金额权重'] = 0

        try:
            data[keys]['外采金额权重'] = round(data[keys]['外采业绩'] / data[keys]['总金额'], 2) * 100
        except ZeroDivisionError:
            data[keys]['外采金额权重'] = 0

        data[keys]['外采客均增幅'] = data[keys]['外采业绩'] / len(data[keys]['订单'])
        try:
            data[keys]['服务费权重'] = round(data[keys]['服务费'] / data[keys]['总金额'], 2) * 100
        except ZeroDivisionError:
            data[keys]['服务费权重'] = 0

    return {'data': data, 'size': size, 'zongyeji': zongyeji}


def getcommentinfo(starttime, endtime, shopname, staffsname):
    engine = create_engine('mysql+mysqlconnector://root:root@192.168.0.115:3306/stuhu')
    sql = """select  exportorders.*,commoditylist.ProductCode,commoditylist.ProductName,commoditylist.Number 'shuliang',commoditylist.Unit,commoditylist.UnitPrice,commoditylist.TotalPrice '销售价',commoditylist.costprice '成本价',orderdetails.PlateNumber '车牌',commoditylist.pinlei,commoditylist.pinpai  from exportorders left join commoditylist on exportorders.OrderNumber=commoditylist.OrderNumber left join orderdetails on exportorders.OrderNumber=orderdetails.OrderNumber where exportorders.InstallationTime between '{}' and '{}' and exportorders.ShopName='{}' and exportorders.TechnicalName='{}';""".format(
        starttime, endtime, shopname, staffsname)
    df_info = pandas.read_sql_query(sql, engine)
    df_info = df_info.fillna('无')
    df_infos = df_info.loc[:,
               ['InstallationTime', 'OrderNumber', 'OrderWay', 'shuliang', 'ProductName', 'pinlei', 'pinpai']]
    df_infos = df_infos[df_infos['pinlei'] != '工时费']

    df_infos['业绩'] = round(
        df_info['销售价'].apply(lambda x: float(x.replace('￥', '').replace(',', '').replace('无', '0'))), 2) - (round(
        df_info['成本价'].apply(lambda x: float(str(x).replace('无', '0'))), 2) * round(
        df_info['shuliang'].apply(lambda x: float(str(x).replace('无', '0'))), 2))
    df_infos['工时费'] = round(df_info['InstallationFeeIncome'].apply(lambda x: float(x)), 2)
    df_infos['工时费权重'] = df_infos['工时费']/(df_infos['工时费'] + df_infos['业绩']) * 100
    commentlistdf_infos = df_infos.groupby(['OrderNumber', 'pinlei'])['ProductName']
    commentlistdf_infostwo = df_infos.groupby(['OrderNumber', 'pinlei'])['pinpai']
    commentlistdf_dict = {}
    for i in commentlistdf_infos:
        commentlistdf_dict[i[0]] = [foo for foo in i[1]]
    commentlistdf_dicttwo = {}
    for i in commentlistdf_infostwo:
        commentlistdf_dicttwo[i[0]] = [foo for foo in i[1]]

    info = df_infos.groupby(['InstallationTime', 'OrderNumber', 'OrderWay', 'pinlei']).nth(0).T.to_dict()
    princeinfo = df_infos.groupby(['OrderNumber']).sum().T.to_dict()


    for keys,values in info.items():
        info[keys]['产品名称'] = commentlistdf_dict[(keys[1], str(keys[3]))]
    for keys,values in info.items():
        info[keys]['品牌'] = commentlistdf_dicttwo[(keys[1], keys[3])]
    for keys, values in info.items():
        try:
            info[keys]['工时费权重'] = round(princeinfo[keys[1]]['工时费']/(princeinfo[keys[1]]['工时费'] + princeinfo[keys[1]]['业绩']), 2) * 100
        except ZeroDivisionError:
            info[keys]['工时费权重'] = 0

        try:
            info[keys]['业绩权重'] = round(info[keys]['业绩'] / (princeinfo[keys[1]]['工时费'] + princeinfo[keys[1]]['业绩']),2) * 100
        except ZeroDivisionError:
            info[keys]['业绩权重'] = 0


    return info

class Product_data(APIView):
    def get(self, request):
        return render(request, 'collect/product.html')

    def post(self, request):
        return render(request, 'collect/product.html')
