from django.urls import path

from . import views

app_name = 'security'
urlpatterns = [
    path('', views.index, name='index'),
    path('allsecurity', views.allsecurity, name='allsecurity'),
    path('allforecast', views.allForcast, name='allForcast'),
    path('allForcastPage', views.allForcastPage, name='allForcastPage'),
    path('forcast/<perforType>', views.forcast, name='forcast'),
]
