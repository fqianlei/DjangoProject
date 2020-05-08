from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from security.models import BasicInfo, Forecast, PerforType, MyFavorite
from django.template import loader
from django.core.paginator import Paginator

# Create your views here.  m = MyFavorite.objects.values('code')
#f = MyFavorite.objects.values_list('code',flat=True)
"""
def index(request):
    all_perforType_list = PerforType.objects.all()
    context = {
        'all_perforType_list': all_perforType_list
    }
    return render(request, 'index.html', context)
"""


class IndexView(generic.ListView):
    context_object_name = 'all_perforType_list'
    model = PerforType
    template_name = 'security/index.html'


def allsecurity(request):
    all_security_list = BasicInfo.objects.all()
    template = loader.get_template('security/allsecurity.html')
    context = {
        'all_security_list': all_security_list
    }
    return HttpResponse(template.render(context, request))


def allForcast(request):
    all_forcast_list = Forecast.objects.all()
    # template = loader.get_template('allforcast.html')
    context = {
        'all_forcast_list': all_forcast_list
    }
    # return HttpResponse(template.render(context,request))
    return render(request, 'security/allforcast.html', context)


def allForcastPage(request):
    all_forcast_list = Forecast.objects.all()
    paginator = Paginator(all_forcast_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'security/focastlist.html', {'page_obj': page_obj})


def forcast(request, perforType):
    all_forcast_list = Forecast.objects.filter(perforType__exact=perforType)
    paginator = Paginator(all_forcast_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'security/focastlist.html', {'page_obj': page_obj, 'perforType': perforType})


def addReason(request):
    code = BasicInfo.objects.get(pk = str(request.POST['code']))
    myf = MyFavorite(code=code, myReason=request.POST['myReason'])
    myf.save()
    return HttpResponse("<script>alert('股票入选原因已经保存成功');window.opener=null;window.top.open('','_self','');window.close(this);</script>")

def toAddReason(request):
    return render(request, 'security/toaddreason.html')


def tosearch(request):
    return render(request, 'security/tosearch.html')

def search(request):
    basicinfo_list = BasicInfo.objects.filter(name__in=[request.POST['name']])
    paginator = Paginator(basicinfo_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'security/toaddreason.html', {'page_obj': page_obj})


def toreason(request):
    #basicinfo_list = BasicInfo.objects.filter(code__in=[600066,300328])
    f = MyFavorite.objects.values_list('code',flat=True)
    basicinfo_list = BasicInfo.objects.filter(code__in=f)
    paginator = Paginator(basicinfo_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'security/toaddreason.html', {'page_obj': page_obj})
