import ssl
import sys
from urllib.request import Request, urlopen
from datetime import datetime


def crawling(
        url='',
        encoding='utf-8',
        proc1=lambda data: data, # 안넣으면 그냥 들어간 데이터 반환하는 익명함수
        proc2=lambda data: data,
        err=lambda e: print(f'{e} : {datetime.now()}', file=sys.stderr),
        ):
    try:
        request = Request(url)
        # ssl._create_default_https_context = ssl._create_unverified_context()
        context = ssl._create_unverified_context()
        response = urlopen(request, context=context)

        receive = response.read()
        print(f'{datetime.now()}: success for request [{url}]')
        html = receive.decode(encoding, errors='replace')
        return proc2(proc1(html)) # 3항 연산자 -> 람다식 받은것 익명함수

    except Exception as e:
        err(e)

