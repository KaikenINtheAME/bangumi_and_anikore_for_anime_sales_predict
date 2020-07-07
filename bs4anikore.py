from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

re_title = re.compile('''.*?（TVアニメ動画）''')
re_score = re.compile('''[0-9]\.[0-9]''')
re_tent = re.compile('''[0-9\.]+?人が棚に入れました''')


# it looks like anikore site not allow access too often
# so I run this crawler twice
urls = [
    #'https://www.anikore.jp/chronicle/2018/winter/ac:tv/',
    #'https://www.anikore.jp/chronicle/2018/spring/ac:tv/',
    #'https://www.anikore.jp/chronicle/2018/summer/ac:tv/',
    #'https://www.anikore.jp/chronicle/2018/autumn/ac:tv/',
     'https://www.anikore.jp/chronicle/2019/winter/ac:tv/',
     'https://www.anikore.jp/chronicle/2019/spring/ac:tv/',
     'https://www.anikore.jp/chronicle/2019/summer/ac:tv/',
     'https://www.anikore.jp/chronicle/2019/autumn/ac:tv/'
]
new_urls = []
# I only scraped two pages. You can try to scrape more.
pages = ['page:2']
for url in urls:
    new_urls.append(url)
    for page in pages:
        new_urls.append(url+page)

title_list = []
score_list = []
tent_list = []

for url in new_urls:
    try:
        html = urlopen(url)
        print('open:{}'.format(url))
    except:
        print('can not open {}'.format(url))
        continue
    soup = BeautifulSoup(html, 'html.parser')

    # the web pages is kind of weird.
    # at most 25 items per page.
    # and some pages least that 25.
    # there are interference factors...

    print('fetching titles...')
    span = str(soup.find_all('span'))
    title = re_title.findall(span)
    title_list.extend(title[:25])
    print('finish.')

    print('fetching scores...')
    strong = str(soup.find_all('strong'))
    score = re_score.findall(strong)
    # ...so you see the code below...
    score_list.extend(score[::4])
    print('finish.')

    print('fetching the number of tent people...')
    div = str(soup.find_all('div'))
    tent = re_tent.findall(div)
    tent_list.extend(tent[:25])
    print('finish.')

    print('title list length:', len(title_list))
    print('score list length:', len(score_list))
    print('tent list length:', len(tent_list))
    print('reshape the title and tent list with length of score list: ',len(score_list))
    # ...and there.
    # I confirm it's correctness manually
    title_list = title_list[:len(score_list):1]
    tent_list = tent_list[:len(score_list):1]
    print('now:')
    print('title list length: ', len(title_list))
    print('tent list length: ', len(tent_list))

    if len(title_list) == len(score_list) and len(tent_list) == len(score_list):
        df = pd.DataFrame({'title':title_list, 'scores': score_list, 'tent':tent_list})
        print('to csv.')
        df.to_csv('anikore2019.csv', encoding='utf-8')