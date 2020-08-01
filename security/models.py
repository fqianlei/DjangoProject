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
    fullname = models.CharField(max_length=100, null=True)#股票全称
    enname = models.CharField(max_length=100, null=True)#英文全称
    market = models.CharField(max_length=100, null=True)#市场类型 （主板/中小板/创业板/科创板）
    exchange = models.CharField(max_length=100, null=True)#交易所代码  交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    curr_type = models.CharField(max_length=100, null=True)#交易货币
    list_status = models.CharField(max_length=100, null=True)#上市状态： L上市 D退市 P暂停上市
    list_date = models.CharField(max_length=100, null=True)#上市日期
    delist_date = models.CharField(max_length=100, null=True)#退市日期
    is_hs = models.CharField(max_length=100, null=True)#是否沪深港通标的，N否 H沪股通 S深股通
    chairman = models.CharField(max_length=100, null=True)#法人代表
    manager = models.CharField(max_length=100, null=True)#总经理
    secretary = models.CharField(max_length=100, null=True)#董秘
    reg_capital = models.CharField(max_length=100, null=True)#注册资本
    setup_date = models.CharField(max_length=100, null=True)#注册日期
    province = models.CharField(max_length=100, null=True)#所在省份
    city = models.CharField(max_length=100, null=True)#所在城市
    introduction = models.CharField(max_length=100, null=True)#公司介绍
    email = models.CharField(max_length=100, null=True)#电子邮件
    office = models.CharField(max_length=100, null=True)#办公室
    employees = models.CharField(max_length=100, null=True)#员工人数
    main_business = models.CharField(max_length=100, null=True)#主要业务及产品
    business_scope = models.CharField(max_length=100, null=True)  # 经营范围

    roe = models.FloatField(max_length=20, null=True) #净资产收益率ROE
    dfql = models.FloatField(max_length=20, null=True) #权益乘数
    efql = models.FloatField(max_length=20, null=True) #总资产周转率
    ffql = models.FloatField(max_length=20, null=True) #净利润/营业总收入
    gfql = models.FloatField(max_length=20, null=True) #净利润/利润总额
    hfql = models.FloatField(max_length=20, null=True) #利润总额/息税前利润
    ifql = models.FloatField(max_length=20, null=True) #应收账款
    jfql = models.FloatField(max_length=20, null=True) #应收票据
    kfql = models.FloatField(max_length=20, null=True) #2019净利润
    lfql = models.FloatField(max_length=20, null=True) #2020 Q1净利润2
    mfql = models.FloatField(max_length=20, null=True)  # 2017营业收入
    nfql = models.FloatField(max_length=20, null=True)  # 2018营业收入
    ofql = models.FloatField(max_length=20, null=True)  # 2019营业收入
    pfql = models.FloatField(max_length=20, null=True)  # 2017同比增长
    qfql = models.FloatField(max_length=20, null=True)  # 2018同比增长
    rfql = models.FloatField(max_length=20, null=True)  # 2019同比增长
    sfql = models.FloatField(max_length=20, null=True)  # 动态市盈率
    tfql = models.FloatField(max_length=20, null=True)  # 市净率
    ufql = models.FloatField(max_length=20, null=True)  # 总市值

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
    ts_code = models.CharField(max_length=200,null=True) # 股票代码
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

