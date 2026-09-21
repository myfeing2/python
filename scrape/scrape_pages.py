import requests
from bs4 import BeautifulSoup
# from urllib.request import urlopen
import csv

urlstr = 'https://www.fawanghuihui.org/gb/criminal/all?page='
table = [[]]
n = 1
while n <= 100:
    req = requests.get(urlstr + str(n))
    soup = BeautifulSoup(req.text, 'html.parser')
    html_table = soup.find('table')
    for row in html_table.select('tr:nth-of-type(n+2)'):
        table.append([col.text for col in row if col.text != '\n'])
    n = n + 1
    print(n, end=' ')

with open('ccp.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(table)
