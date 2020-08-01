#获取日线数据
import tushare as ts
import numpy as np
import sqlite3
import time

ts.set_token('619aac806adb72235ee6feb086f2cbb17cdeb4c85322e75c4f2f7e5d')
pro = ts.pro_api()

conn = sqlite3.connect('C:\DjangoProject\db.sqlite3')
cur = conn.cursor()
cur.execute("select ts_code from security_basicinfo")

j=1
stocklist = []
for row in cur:
    stocklist.append(row[0])
for i in range(len(stocklist)):
    start = time.perf_counter()
    print(stocklist[i],j)
    j = j + 1
    df = pro.daily(ts_code=stocklist[i], start_date='20200101', end_date='20200725')
    train_data = np.array(df)  # 先将数据框转换为数组
    train_data_list = train_data.tolist()  # 其次转换为列表
    #time.sleep(0.1)
    code = stocklist[i][0:6]
    cur.executemany('''
        insert into security_daily(ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount) 
        values (?,?,?,?,?,?,?,?,?,?,?)''', train_data_list)
    conn.commit()
    """
    for i in range(len(train_data_list)):
        cur.execute('''
        insert into security_daily(ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount,code) 
        values (?,?,?,?,?,?,?,?,?,?,?,?)
        ''',[train_data_list[i][0],train_data_list[i][1],train_data_list[i][2],train_data_list[i][3],train_data_list[i][4],
             train_data_list[i][5], train_data_list[i][6], train_data_list[i][7], train_data_list[i][8],
             train_data_list[i][9],train_data_list[i][10],code])
        #print("正在插入第：",j,"个，当前插入：",code,":",train_data_list[i][1])
        conn.commit()
    """
    end = time.perf_counter()
    print(end - start)