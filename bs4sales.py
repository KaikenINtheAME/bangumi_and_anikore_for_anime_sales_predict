from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

title_list = []
sales_list = []

# the 'tr' parts of this page looks like:
#
# <tr>
# <td>*29,066pt　</td>
# <td>**3,633pt　</td>
# <td>乙女ゲームの破滅フラグしかない悪役令嬢に転生してしまった…　</td>
# .........
# </tr>
#
# so it's easy to get the average sales and titles
# and that's why I can use 'title = td.split('pt')[2]'
# in line 41

re_tr = re.compile(r'[0-9*,]+pt')

html = urlopen('http://rankstker.net/')
soup = BeautifulSoup(html, 'html.parser')
text = soup.find_all('tr')

for i in range(len(text)):
    td = text[i].get_text()
    if len(re_tr.findall(td)) < 2:
        continue
    avg = re_tr.findall(td)[1]
    avg.replace('pt', '')
    avg.replace(',', '')
    avg.replace('*', '')
    print('catch avg:')
    print(avg)
    sales_list.append(avg)

    title = td.split('pt')[2]
    title.strip()
    print('catch title:')
    print(title)
    title_list.append(title)

sales = pd.DataFrame({'title': title_list, 'sales': sales_list})
sales.to_csv('sales.csv')

