from datetime import datetime
from django.utils import timezone
from django.db import models

# py manage.py makemigrations security    py manage.py migrate
# Create your models here.

class BasicInfo(models.Model):
    code = models.CharField(primary_key=True, max_length=20) #股票代码 600006
    ts_code = models.CharField(max_length=20, null=True) #股票简称  # 股票代码 600006.SH'
    name = models.CharField(max_length=20, null=True) #股票简称
    webSite = models.CharField(max_length=100, null=True)# 网站
    area = models.CharField(max_length=100, null=True) # 所在地域
    industry = models.CharField(max_length=100, null=True)# 所属行业
    market = models.CharField(max_length=100, null=True)#市场类型 （主板/中小板/创业板/科创板）
    exchange = models.CharField(max_length=100, null=True)#交易所代码  交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    list_date = models.CharField(max_length=100, null=True)#上市日期
    province = models.CharField(max_length=100, null=True)#所在省份
    city = models.CharField(max_length=100, null=True)#所在城市
    introduction = models.CharField(max_length=100, null=True)#公司介绍
    business_scope = models.CharField(max_length=100, null=True)  # 经营范围
    PE = models.CharField(max_length=100, null=True)  # 动态市盈率
    PB = models.CharField(max_length=100, null=True)  # 市净率
    GMV = models.CharField(max_length=100, null=True)  # 总市值
    BI = models.CharField(max_length=100, null=True)  # Business Income 营业收入
    OP = models.CharField(max_length=100, null=True)  # operating profit 营业利润
    GPM = models.CharField(max_length=100, null=True)  # 销售毛利率 Gross profit margin
    NPRA = models.CharField(max_length=100, null=True)  # 销售净利率 Net profit rate of sales
    YOY = models.CharField(max_length=100, null=True)  # 营业收入（同比增长率）
    AR = models.CharField(max_length=100, null=True) #应收账款Accounts receivable

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
    perforContent = models.CharField(max_length=4000, null=True)
    changeReason = models.CharField(max_length=4000, null=True)
    upperLimit = models.CharField(max_length=200, null=True)
    lowerLimit = models.CharField(max_length=200, null=True)
    kanguo = models.CharField(max_length=200, null=True)
    addtime = models.DateTimeField(default = timezone.now, null=True)



class MyFavorite(models.Model):
    code = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, db_column='code')
    myReason = models.CharField(max_length=200)
    addtime = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.code


class CCTVNews(models.Model):
    date = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=5000)

class Daily(models.Model):
    code = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, db_column='code')
    trade_date = models.CharField(max_length=200,null=True) #交易日期
    open = models.FloatField(null=True)  # 应收账款
    high = models.FloatField(null=True)  # 最高价
    low = models.FloatField(null=True)  # 最低价
    close = models.FloatField(null=True)  # 收盘价
    pre_close = models.FloatField(null=True)  # 昨收价
    change = models.FloatField(null=True)  # 涨跌额
    pct_chg = models.FloatField(null=True)  # 涨跌幅 （未复权）
    vol = models.FloatField(null=True)  # 成交量 （手）
    amount = models.FloatField(null=True)  # 应成交额 （千元）

class AnnData(models.Model):
    code = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, db_column='code')
    annPeriod = models.CharField(max_length=8, null=True) #报告日期
    annType = models.CharField(max_length=100, null=True)#指标类型
    annResult = models.CharField(max_length=100, null=True) #指标结果


class IndexBase(models.Model):
    annType = models.CharField(max_length=100, null=True)#指标类型：汉字描述
    annTypeEngDes = models.CharField(max_length=100, null=True)  # 指标类型：英文描述
    annTypeEngAbb = models.CharField(max_length=100, null=True)  # 指标类型：英文简称
    useValue  = models.CharField(max_length=100, null=True)  # 指标类型：使用场景，使用价值，计算方法等信息
    def __str__(self):
        return self.annType
