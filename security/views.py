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
                    left join (select ff.perforType,count(ff.id) newp from security_forecast ff where ff.kanguo is null group  by ff.perforType) notkanguo on notkanguo.perforType = f.perforType group by f.perforType''').fetchall()
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
    code = BasicInfo.objects.get(pk = str(request.POST['code']))
    myf = MyFavorite(code=code, myReason=request.POST['myReason'])
    myf.save()

    if request.POST.get('fid',False):
        forcasta = Forecast.objects.get(pk = str(request.POST['fid']))
        forcasta.kanguo = '是'
        forcasta.save()

    return HttpResponse("<script>alert('股票入选原因已经保存成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

def kanguo(request):
    forcasta = Forecast.objects.get(pk = str(request.POST['fid']))
    forcasta.kanguo = '是'
    forcasta.save()
    return HttpResponse("<script>alert('此股票已保存看过记录');window.opener=null;window.top.open('','_self','');window.close(this);</script>")


def toAddReason(request):
    return render(request, 'toaddreason.html')


def tosearch(request):
    return render(request, 'tosearch.html')

def search(request):
    basicinfo_list = BasicInfo.objects.filter(name__in=[request.POST['name']])
    paginator = Paginator(basicinfo_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'toaddreason.html', {'page_obj': page_obj})


def toreason(request):
    #basicinfo_list = BasicInfo.objects.filter(code__in=[600066,300328])
    f = MyFavorite.objects.values_list('code',flat=True)
    basicinfo_list = BasicInfo.objects.filter(code__in=f)
    paginator = Paginator(basicinfo_list, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'toaddreason.html', {'page_obj': page_obj})

def deleteMyfavorate(request):
    MyFavorite.objects.get(pk = request.POST['fid']).delete()
    return HttpResponse()


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
    paginator = Paginator(cctvnews, 4)
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
        with connection.cursor() as cursor:
            context_object_name = cursor.execute('select * from security_forecast where annDate=%s and code=%s and annPeriod=%s and perforType=%s',[annDate,code,annPeriod,perforType]).fetchone()
            if context_object_name:
                pass
            else:
                name = sheet['C' + str(i)].value
                trade = sheet['D' + str(i)].value
                perforContent = sheet['G' + str(i)].value
                changeReason = sheet['H' + str(i)].value
                upperLimit = sheet['I' + str(i)].value
                lowerLimit = sheet['J' + str(i)].value
                sheetForcast = [annDate,code,name,trade,annPeriod,perforType,perforContent,changeReason,upperLimit,lowerLimit,datetime.datetime.now()]
                daoruhang=daoruhang+1
                with connection.cursor() as cursor:
                    print(code)
                    cursor.execute('insert into security_forecast (annDate,code,name,trade,annPeriod,perforType,perforContent,changeReason,upperLimit,lowerLimit,addtime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',sheetForcast)
    print('本次共导入',daoruhang , '条业绩预告')
    return HttpResponse("<script>alert('数据导入成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

