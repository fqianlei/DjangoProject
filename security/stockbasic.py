"""
created on Fri 2020-06-26
@author:fengl
功能描述：删除表数据后，从toshare接口重新获取
"""
import tushare as ts
import numpy as np
import pandas as pd
import sqlite3


conn = sqlite3.connect('D:\PycharmProjects\DjangoProject\db.sqlite3')
c = conn.cursor()
c.execute("delete from security_basicinfo ")
conn.commit()
ts.set_token('619aac806adb72235ee6feb086f2cbb17cdeb4c85322e75c4f2f7e5d')
pro = ts.pro_api()
#list_status='L' 上市股票

def insertBasic(exchange):
    data = pro.stock_basic(exchange=exchange, list_status='L',fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    train_data = np.array(data) #先将数据框转换为数组
    train_data_list = train_data.tolist() #其次转换为列表
    c.executemany('''
        INSERT INTO security_basicinfo (ts_code,code,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,
        list_date,delist_date,is_hs) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', train_data_list)
    conn.commit()

insertBasic('SSE')
insertBasic('SZSE')

def updateBasic(exchange):
    data = pro.stock_company(exchange=exchange,fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
    train_data = np.array(data)  # 先将数据框转换为数组
    train_data_list = train_data.tolist()  # 其次转换为列表
    print(len(train_data_list))
    for i in range(len(train_data_list)):
        c.execute('''
        update security_basicinfo set chairman=?,manager=?,secretary=?,reg_capital=?,setup_date=?,
        province=?,city=?,introduction=?,webSite=?,email=?,office=?,employees=?,main_business=?,business_scope=?  
        WHERE ts_code=?
        ''',[train_data_list[i][1],train_data_list[i][2],train_data_list[i][3],train_data_list[i][4],
             train_data_list[i][5], train_data_list[i][6], train_data_list[i][7], train_data_list[i][8],
             train_data_list[i][9], train_data_list[i][10], train_data_list[i][11], train_data_list[i][12],
             train_data_list[i][13],train_data_list[i][14],train_data_list[i][0]])
        conn.commit()

updateBasic('SSE')
updateBasic('SZSE')


conn.close()