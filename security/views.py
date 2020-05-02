from django.shortcuts import render
from django.http import HttpResponse
from .models import BasicInfo,Forecast,PerforType
from django.template import loader
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    all_perforType_list = PerforType.objects.all()
    context = {
        'all_perforType_list': all_perforType_list
    }
    return render(request, 'index.html', context)

def allsecurity(request):
    all_security_list = BasicInfo.objects.all()
    template = loader.get_template('allsecurity.html')
    context = {
        'all_security_list': all_security_list
    }
    return HttpResponse(template.render(context,request))


def allForcast(request):
    all_forcast_list = Forecast.objects.all()
    #template = loader.get_template('allforcast.html')
    context = {
        'all_forcast_list': all_forcast_list
    }
    #return HttpResponse(template.render(context,request))
    return render(request,'allforcast.html',context)

def allForcastPage(request):
    all_forcast_list = Forecast.objects.all()
    paginator = Paginator(all_forcast_list,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'focastlist.html', {'page_obj': page_obj})

def forcast(request,perforType):
    all_forcast_list = Forecast.objects.filter(perforType__exact=perforType)
    paginator = Paginator(all_forcast_list,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'focastlist.html', {'page_obj': page_obj, 'perforType':perforType})
