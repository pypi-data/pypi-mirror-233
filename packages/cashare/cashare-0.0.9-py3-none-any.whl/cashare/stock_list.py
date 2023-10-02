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
    df = stock_list(type='eu', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)

    df=stock_list(type='hk',token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)
    df = stock_list(type='ca', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)
    df = stock_list(type='us', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)
    df = stock_list(type='tsx', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)

    df = stock_list(type='cp', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)

    df = stock_list(type='etf', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)
    df = stock_list(type='index', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)

    df = stock_list(type='fx', token='f2c4291a77c3ea30e902289c92c03500785')
    print(df)

    pass



