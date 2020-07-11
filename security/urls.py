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
    path('toreason', views.toreason, name='toreason'),
    path('tosearch', views.tosearch, name='tosearch'),
    path('search', views.search, name='search'),
    path('kanguo', views.kanguo, name='kanguo'),
    path('deleteMyfavorate', views.deleteMyfavorate, name='deleteMyfavorate'),
    path('cctvnews', views.cctvnews, name='cctvnews'),
    path('insertForcast', views.insertForcast, name='insertForcast'),
]
