import openpyxl
from django.db import connection
wb = openpyxl.load_workbook('D:\业绩预告.xlsx')
sheet = wb.worksheets[0]
rows = sheet.max_row
for i in range(2, rows):
    annDate = sheet['A'+str(i)].value
    code = sheet['B'+str(i)].value
    annPeriod = sheet['E'+str(i)].value
    perforType = sheet['F'+str(i)].value
    with connection.cursor() as cursor:
        context_object_name = cursor.execute('select * from security_forecast where annDate='' and code='' and annDate='' and perforType=',[annDate,code,annPeriod,perforType]).fetchone()
    print(context_object_name)
print(rows)