from django.urls import path

from . import views

app_name = 'security'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('allsecurity', views.allsecurity, name='allsecurity'),
    path('allforecast', views.allForcast, name='allForcast'),
    path('allForcastPage', views.allForcastPage, name='allForcastPage'),
    path('forcast/<perforType>', views.forcast, name='forcast'),
    path('addReason', views.addReason, name='addReason'),
    path('toaddreason', views.toAddReason, name='toaddreason'),
    path('toreason', views.toreason, name='toreason'),
    path('tosearch', views.tosearch, name='tosearch'),
    path('search', views.search, name='search'),
    path('bannianbao/<perforType>', views.bannianbao, name='bannianbao'),
    path('kanguo', views.kanguo, name='kanguo'),
    path('deleteMyfavorate', views.deleteMyfavorate, name='deleteMyfavorate'),
]
