import pdfplumber
import pandas as pd
import openpyxl

columns=['序号','企业名称','证书编号']
files=["D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年第一批备案高新技术企业名单.pdf",
       "D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年认定的高新技术企业第一批补充备案名单.pdf",
       "D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年第二批备案高新技术企业名单.pdf",
       "D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年认定的第三批高新技术企业备案名单.pdf",
       "D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年认定的第四批高新技术企业备案名单.pdf",
       "D:\\feiminyu\\客户资源\\政府企业名单\\国家高企认定\\2021\\上海市2021年认定的第五批高新技术企业备案名单.pdf"]
newdf=pd.DataFrame()

for file in files:
    with pdfplumber.open(file) as pdf:
        print(file)
        totalPage=len(pdf.pages)
        for page in pdf.pages:
            tables = page.extract_tables()
            #print('total tables: ' + str(len(tables)))
            for t in tables:
                df = pd.DataFrame(t,columns=columns)
                newdf=pd.concat([newdf, df])

fdf=newdf[newdf['序号']!="序号"]
fdf.to_excel('output.xlsx',index=False,columns=['企业名称'])
