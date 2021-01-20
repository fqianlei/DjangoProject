from django.urls import path

from . import views

app_name = 'security'

'''    path('', views.IndexView.as_view(), name='index'),
path('allForcastPage', views.allForcastPage, name='allForcastPage'),
    path('allsecurity', views.allsecurity, name='allsecurity'),
    path('allforecast', views.allForcast, name='allForcast'),
'''
urlpatterns = [
    path('', views.index, name='index'),
    path('forcast/<perforType>', views.forcast, name='forcast'),
    path('addReason', views.addReason, name='addReason'),
    path('toaddreason', views.toAddReason, name='toaddreason'),
    path('deleteMyfavorate', views.deleteMyfavorate, name='deleteMyfavorate'),
    path('cctvnews', views.cctvnews, name='cctvnews'),
    path('insertForcast', views.insertForcast, name='insertForcast'),
    path('readByline', views.readByline, name='readByline'),
    path('insertRoe', views.insertRoe, name='insertRoe'),
    path('insertAnndata', views.insertAnndata, name='insertAnndata'),
    path('tosearch', views.tosearch, name='tosearch'),
    path('tosearch2', views.tosearch2, name='tosearch2'),
    path('tosearch3', views.tosearch3, name='tosearch3'),
    path('search', views.search, name='search'),
    path('search2', views.search2, name='search2'),
    path('search3', views.search3, name='search3'),
    path('zhibiao/<code>', views.zhibiao, name='zhibiao'),
    path('zhibiao2/<code>', views.zhibiao2, name='zhibiao2'),
    path('printipv6', views.printipv6, name='printipv6'),
]
