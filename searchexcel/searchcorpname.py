import openpyxl
import os
import re
import sys

workDirHist='E:\\wps sync folder\\历史分配记录'
workDir='E:\\wps sync folder'
books=['2022月分配表.xlsx',
       '2020月分配表.xlsx',
       '2021月分配表.xlsx',
       '2022月分配表（6月前）.xlsx']
matchRe=re.compile(sys.argv[1])

for bookName in books:
    if books.index(bookName)==0:
        os.chdir(workDir)
    else:
        os.chdir(workDirHist)
    wb=openpyxl.load_workbook(bookName)
    print('searching in workbook: '+bookName)
    sheets=wb.sheetnames
    for sheetName in sheets:
        sheet=wb[sheetName]
        print('   searching in sheet:'+sheetName)
        for cellObj in sheet['E']:
            found=matchRe.search(str(cellObj.value))
            if found:
                print('        ', cellObj.coordinate, cellObj.value)
                