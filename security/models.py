from datetime import datetime

from django.db import models


# Create your models here.

class BasicInfo(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    webSite = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Forecast(models.Model):
    annDate = models.DateField()
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    trade = models.CharField(max_length=200, null=True)
    annPeriod = models.DateField()
    perforType = models.CharField(max_length=200, null=True)
    perforType = models.CharField(max_length=200, null=True)
    perforContent = models.CharField(max_length=4000, null=True)
    changeReason = models.CharField(max_length=4000, null=True)
    upperLimit = models.CharField(max_length=200, null=True)
    lowerLimit = models.CharField(max_length=200, null=True)
