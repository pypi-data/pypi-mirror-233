import httpx
from cashare.common.dname import url1
import pandas as pd


def stock_list(token,type:str):
    if type in['us','hk','ca','eu','tsx','cp','index','etf','fx']:
        url = url1 + '/stock/list/'+type+'/'+ token
        # print(url)
        r = httpx.get(url,timeout=100)
        return pd.DataFrame(r.json())
    else:
        return "type输入错误"

if __name__ == '__main__':
    df = stock_list(type='eu', token='you_token')
    print(df)
    df=stock_list(type='hk',token='you_token')
    print(df)
    pass



