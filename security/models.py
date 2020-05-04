from datetime import datetime

from django.db import models


# Create your models here.

class BasicInfo(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    webSite = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.code
        # return 'code:%s %s' % (self.code,self.webSite)


class Forecast(models.Model):
    annDate = models.CharField(max_length=200)
    code = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, db_column='code')
    name = models.CharField(max_length=200)
    trade = models.CharField(max_length=200, null=True)
    annPeriod = models.CharField(max_length=200)
    perforType = models.CharField(max_length=200, null=True)
    perforType = models.CharField(max_length=200, null=True)
    perforContent = models.CharField(max_length=4000, null=True)
    changeReason = models.CharField(max_length=4000, null=True)
    upperLimit = models.CharField(max_length=200, null=True)
    lowerLimit = models.CharField(max_length=200, null=True)


class PerforType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class MyFavorite(models.Model):
    code = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, db_column='code')
    myReason = models.CharField(max_length=200)
    addtime = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.code
