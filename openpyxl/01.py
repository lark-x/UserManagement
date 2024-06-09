from openpyxl import Workbook, load_workbook

# wb = Workbook()
wb = load_workbook(r'D:\Python_test\test.xlsx')
ws1 = wb.active
ws2 = wb.create_sheet('Sheet1', 1)
ws3 = wb.create_sheet('Sheet2', 2)
ws4 = wb.create_sheet('Sheet3', 3)
wb.move_sheet(ws3, -1)
del wb['Sheet2']
print(wb.sheetnames)

