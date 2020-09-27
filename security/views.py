import datetime
from datetime import date
import tushare as ts
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from security.models import BasicInfo, Forecast, MyFavorite,CCTVNews
from django.core.paginator import Paginator
import openpyxl
import numpy as np
import pandas

# Create your views here.  m = MyFavorite.objects.values('code')
#f = MyFavorite.objects.values_list('code',flat=True)
"""

class IndexView(generic.ListView):
    context_object_name = 'all_perforType_list'
    model = PerforType
    template_name = 'index.html'
"""
def index(request):
    with connection.cursor() as cursor:
        context_object_name = cursor.execute('''select f.perforType,count(id),notkanguo.newp from security_forecast f
                    left join (select ff.perforType,count(ff.id) newp from security_forecast ff where ff.kanguo is null group  by ff.perforType) notkanguo 
                    on notkanguo.perforType = f.perforType group by f.perforType''').fetchall()
    context = {
        'context_object_name': context_object_name,
    }
    return render(request, 'index.html', context)


def forcast(request, perforType):
    #all_forcast_list = Forecast.objects.filter(perforType__exact=perforType,kanguo=None,trade).order_by('-annDate')
    all_forcast_list = Forecast.objects.raw('''select * from security_forecast f 
    where f.kanguo is null and perforType=%s order by f.annDate desc''',[perforType])
    paginator = Paginator(all_forcast_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'focastlist.html', {'page_obj': page_obj, 'perforType': perforType})

def addReason(request):
    if len(request.POST['myReason'])>2:
        code = BasicInfo.objects.get(pk=str(request.POST['code']))
        myf = MyFavorite(code=code, myReason=request.POST['myReason'])
        myf.save()
    if int(request.POST['fid'])!=99999:
        forcasta = Forecast.objects.get(pk = str(request.POST['fid']))
        forcasta.kanguo = '是'
        forcasta.save()
    return HttpResponse("<script>alert('保存成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

def toAddReason(request):
    return render(request, 'searchresult.html')

def tosearch(request):
    return render(request, 'tosearch.html')

def search(request):
    #将字符串根据换行符切割为列表
    listCode1 = request.POST['code'].split('\r\n')
    listCode = []
    for i in range(len(listCode1)):
        if len(listCode1[i])==6:
            listCode.append(listCode1[i])
            #取值包含证券市场的代码，如：000411.SZ
        elif len(listCode1[i])==9:
            listCode.append(listCode1[i][0:6])
            print(listCode1[i][0:6])
        else:
            if len(listCode1[i])>2:
                if listCode.append(BasicInfo.objects.get(name = listCode1[i])):
                    listCode.append(BasicInfo.objects.get(name=listCode1[i]))
    basicinfo = BasicInfo.objects.filter(code__in=listCode).order_by('sfql')
    return render(request, 'searchresult.html', {'basicinfo': basicinfo})


def deleteMyfavorate(request):
    MyFavorite.objects.get(pk = request.POST['fid']).delete()
    return HttpResponse("<script>alert('删除成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

def cctvnews(request):
    yesterday = str(date.today() - datetime.timedelta(days=1)).replace('-', '')
    with connection.cursor() as cursor:
        yesnews = cursor.execute('select * from security_cctvnews where date=%s',[yesterday]).fetchone()
        if yesnews:
            print("新闻已存在，无需重复添加")
        else:
            ts.set_token('619aac806adb72235ee6feb086f2cbb17cdeb4c85322e75c4f2f7e5d')
            pro = ts.pro_api()
            data = pro.cctv_news(date=yesterday)
            train_data = np.array(data)  # 先将数据框转换为数组
            train_data_list = train_data.tolist()  # 其次转换为列表
            #print(train_data_list)
            for i in range(len(train_data_list)):
                cctv =CCTVNews(date=train_data_list[i][0],title=train_data_list[i][1],content=train_data_list[i][2],)
                print('添加第',i,'条新闻')
                cctv.save()

    cctvnews = CCTVNews.objects.all().order_by('-id')
    paginator = Paginator(cctvnews, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cctvnews.html', {'page_obj': page_obj})

def insertForcast(request):
    wb = openpyxl.load_workbook('D:\业绩预告.xlsx')
    sheet = wb.worksheets[0]
    rows = sheet.max_row
    daoruhang = 0
    for i in range(2, rows):
        annDate = sheet['A' + str(i)].value
        code = sheet['B' + str(i)].value
        annPeriod = sheet['E' + str(i)].value
        perforType = sheet['F' + str(i)].value
        name = sheet['C' + str(i)].value
        with connection.cursor() as cursor:
            context_object_name = cursor.execute('select * from security_forecast where annDate=%s and code=%s and annPeriod=%s and perforType=%s',[annDate,code,annPeriod,perforType]).fetchone()
            if context_object_name:
                pass
            else:
                searchname = cursor.execute('select name from security_basicinfo where code=%s',[code]).fetchone()
                if searchname:
                    # cursor.execute('insert into security_basicinfo (code,name) VALUES (%s,%s)', [code,'test'])
                    trade = sheet['D' + str(i)].value
                    perforContent = sheet['G' + str(i)].value
                    changeReason = sheet['H' + str(i)].value
                    upperLimit = sheet['I' + str(i)].value
                    lowerLimit = sheet['J' + str(i)].value
                    sheetForcast = [annDate, code, name, trade, annPeriod, perforType, perforContent, changeReason,
                                    upperLimit, lowerLimit, datetime.datetime.now()]
                    daoruhang = daoruhang + 1
                    with connection.cursor() as cursor:
                        cursor.execute('insert into security_forecast (annDate,code,name,trade,annPeriod,perforType,perforContent,changeReason,upperLimit,lowerLimit,addtime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',sheetForcast)
                        #cursor.execute('delete  from security_forecast where  code not in (select code from security_basicinfo)')
                else:
                    pass
    print('本次共导入',daoruhang , '条业绩预告')
    return HttpResponse("<script>alert('更新业绩预告成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

#两个EXCEL，先导入业绩预告 ，再导入ROE等数据
def insertRoe(request):
    # 导入ROE等内容，先删除股票名称，再全部复制粘贴EXCEL，主要是去除双引号
    wb = openpyxl.load_workbook('D:\ROE等导入.xlsx')
    sheet = wb.worksheets[0]
    rows = sheet.max_row
    daoruhang = 0
    for i in range(2, rows):
        code = sheet['B' + str(i)].value
        roe = sheet['C' + str(i)].value
        dfql = sheet['D' + str(i)].value  #权益乘数
        efql = sheet['E' + str(i)].value #总资产周转率
        ffql = sheet['F' + str(i)].value #净利润/营业总收入
        gfql = sheet['G' + str(i)].value #净利润/利润总额
        hfql = sheet['H' + str(i)].value #利润总额/息税前利润
        ifql = sheet['I' + str(i)].value #应收账款
        jfql = sheet['J' + str(i)].value #应收票据
        kfql = sheet['K' + str(i)].value #2019净利润
        lfql = sheet['L' + str(i)].value #2020 半年报利润率
        mfql = sheet['M' + str(i)].value # 2017营业收入
        nfql = sheet['N' + str(i)].value  # 2018营业收入
        ofql = sheet['O' + str(i)].value  # 2019营业收入
        pfql = sheet['P' + str(i)].value # 2017同比增长
        qfql = sheet['Q' + str(i)].value # 2018同比增长
        rfql = sheet['R' + str(i)].value  # 2019同比增长
        sfql = sheet['S' + str(i)].value # 动态市盈率
        tfql = sheet['T' + str(i)].value # 市净率
        ufql = sheet['U' + str(i)].value # 总市值
        #print(code,":",rfql)
        daoruhang = daoruhang + 1
        sheetForcast = [roe,dfql,efql,ffql,gfql,hfql,ifql,jfql,kfql,lfql,mfql,nfql,ofql,pfql,qfql,rfql,sfql,tfql,ufql,code]
        with connection.cursor() as cursor:
            cursor.execute('''
            update security_basicinfo set roe=%s,dfql=%s,efql = %s,ffql = %s,gfql =%s,hfql =%s,ifql =%s,jfql =%s,
            kfql =%s,lfql =%s,mfql =%s,nfql =%s,ofql =%s,pfql =%s,qfql =%s,rfql =%s,sfql =%s,tfql =%s,ufql =%s  
            where code =%s''',sheetForcast)
    print('本次更新',daoruhang , '条ROE信息')
    return HttpResponse("<script>alert('更新ROE信息成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")



def readByline(request):
    all_mycode_list = BasicInfo.objects.raw('select * from security_basicinfo where code in (select code from security_myfavorite) order by sfql')
    paginator = Paginator(all_mycode_list, 15)
    #| date:"Y-m-d H:i:s"
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'readByline.html', {'page_obj': page_obj,})

