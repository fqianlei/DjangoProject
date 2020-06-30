import tushare as ts

ts.set_token('619aac806adb72235ee6feb086f2cbb17cdeb4c85322e75c4f2f7e5d')
pro = ts.pro_api()


#df = pro.new_share(start_date='20200626', end_date='20200730'  #新股发行计划
df = pro.ggt_top10(trade_date='20200623')
print(df)