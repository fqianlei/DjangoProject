from datetime import datetime

from django.db import models


# Create your models here.

class BasicInfo(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    webSite = models.CharField(max_length=100,null=True)
