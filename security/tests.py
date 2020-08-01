import jqdatasdk
jqdatasdk.auth('13683833962','Cool1983')
date = jqdatasdk.get_price(security='000001.XSHE',frequency='1d')
print(date[1])