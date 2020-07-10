"""
created on Sat 2020-06-27
@author:fengl
功能描述：删除表数据后，从toshare接口重新获取
"""
import tushare as ts
import numpy as np
import pandas as pd
import sqlite3
from datetime import date
import datetime

yesterday = str(date.today()-datetime.timedelta(days=1)).replace('-','')
conn = sqlite3.connect('C:\DjangoProject\db.sqlite3')
c = conn.cursor()
ts.set_token('619aac806adb72235ee6feb086f2cbb17cdeb4c85322e75c4f2f7e5d')
pro = ts.pro_api()
data = pro.cctv_news(date = yesterday )
train_data = np.array(data)  # 先将数据框转换为数组
train_data_list = train_data.tolist()  # 其次转换为列表
c.executemany('''
    INSERT INTO security_cctvnews (date,title,content) 
    VALUES (?,?,?)''', train_data_list)
conn.commit()
conn.close()
