from django.contrib import admin
from .models import BasicInfo,Forecast,IndexBase

# Register your models here.

admin.site.register(BasicInfo)
admin.site.register(Forecast)
admin.site.register(IndexBase)
