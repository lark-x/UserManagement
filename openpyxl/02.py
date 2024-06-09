from openpyxl import Workbook

wb = Workbook()
ws = wb.active
# ws["a1"] = '哈哈'
# ws['g5'] ='hehe'

# cell = ws.cell(1, 2)
# cell.value = 99
# print(cell.value)
# print(cell.coordinate)
x = 1
for i in range(1, 11):
    for j in range(1, 11):
        ws.cell(i, j, x)
        x += 1

for row in ws.values:
    print(row)
