import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []

    # count(시작점) 무한대로감, break 반드시 필요
    for page in count(start=113):
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
        try:
            request = Request(url)
            # ssl._create_default_https_context = ssl._create_unverified_context()
            context = ssl._create_unverified_context()
            response = urlopen(request, context=context)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')

            print(f'{datetime.now()}: success for request [{url}]')
        except Exception as e:
            # datetime 밑에꺼 import
            print(f'{e} : {datetime.now()}', file=sys.stderr)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            # tag 다 빼고 string 만
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            t = (name, address) + tuple(sidogu)
            results.append(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)

    # for t in results:
    #     print(t)


def crawling_nene():
    results = []

    before_page_first_shop = ''

    # for page in count(start=1):
    for page in range(1, 3):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page

        try:
            request = Request(url)
            response = urlopen(request)
            receive = response.read()
            html = receive.decode('utf-8')

            print(f'{datetime.now()} : success for request[{url}]')
        except Exception as e:
            print(f'{datetime.now()} : {e}', file=sys.stderr)
            break

        bs = BeautifulSoup(html, 'html.parser')

        wrap_div = bs.find('div', attrs={'class': 'shopWrap'})

        shop_divs = wrap_div.findAll('div', attrs={'class': 'shopInfo'})

        now_page_first_shop = wrap_div.find('div', attrs={'class': 'shopName'}).text

        # 끝 검출
        if now_page_first_shop == before_page_first_shop:
            break

        for index, shop in enumerate(shop_divs):
            strings = list(shop.strings)

            if strings[2] != 'Pizza':
                name = strings[4]
                address = strings[6]
            else:
                name = strings[6]
                address = strings[8]

            dosigu = address.split()[:2]
            t = (name, address) + tuple(dosigu)

            if index == 0:
                before_page_first_shop = name

            results.append(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    table.to_csv('__results__/nene.csv', encoding='utf-8', mode='w', index=True)


def ex01():
    results = []

    # count(시작점) 무한대로감, break 반드시 필요
    for page in count(start=113):
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d'%page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class':'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            # tag 다 빼고 string 만
            strings = list(tag_tr.strings)
            print(tag_tr)
            print(strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            t = (name, address)+tuple(sidogu)
            results.append(t)

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)

    # for t in results:
    #     print(t)


def crawling_kyochon():
    retults = []

    for sido1 in range(1, 2):
        for sido2 in count(25, 27):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawler.crawling(url)

            #끝 검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)

                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split()[:2]

                retults.append((name, address) + tuple(sidogu))

    for t in retults:
        print(t)


def crawling_goobne():
    url = 'http://goobne.co.kr/store/search_store.jsp'
    wd = webdriver.Chrome('D:\cafe24\chromedriver_win32\chromedriver.exe')
    wd.get(url)

    time.sleep(5)

    results = []
    for page in range(1, 106):
        # 자바 스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time. sleep(3)

        # 실행결과 HTML( 동적으로 렌더링 된 html) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])
    table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)

    for result in results:
        print(result)


if __name__ == '__main__':
    # pelicana

    # 처음에 에러 SSL: CERTIFICATE_VERIFY_FAILED
    # SSL 무시하도록 crawling_pelicana()에 아래 두줄 추가
    # context=ssl._create_unverified_context()
    # response=urlopen(request, context=context)

    # crawling_pelicana()

    # nene 과제
    # ex01()
    # crawling_kyochon()
    # crawling_goobne()

    crawling_nene()

    # cli에서 할 때는 굽네방식은 할 수 없다. 브라우저 띄워서 하기 때문. 브라우저는 gui 이용해서 띄움
