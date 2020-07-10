from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from security.models import BasicInfo, Forecast, MyFavorite,CCTVNews
from django.template import loader
from django.core.paginator import Paginator

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
    print(context_object_name)
    context = {
        'context_object_name': context_object_name,
    }
    return render(request, 'index.html', context)


def forcast(request, perforType):
    #all_forcast_list = Forecast.objects.filter(perforType__exact=perforType,kanguo=None,trade).order_by('-annDate')
    all_forcast_list = Forecast.objects.raw('''select * from security_forecast f 
    where f.kanguo is null and perforType=%s order by f.annDate desc''',[perforType])
    paginator = Paginator(all_forcast_list, 10)

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
    cctvnews = CCTVNews.objects.all().order_by('-id')
    paginator = Paginator(cctvnews, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cctvnews.html', {'page_obj': page_obj})
