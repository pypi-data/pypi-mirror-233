from cashare.common.dname import url1
import pandas as pd
from cashare.common.get_data import _retry_get
def now_data(type,token):
    li = handle_url(type=type, token=token)
    r =_retry_get(li,timeout=100)
    if str(r) == 'token无效或已超期':
        return r
    else:
        if r.empty:
            return r
        else:
            #将最后一列更新为时间
            r = r.rename(columns={'timestamp':'time'})
            r['time'] = pd.to_datetime(r['time'], unit='s')
            return r
def handle_url(type,token):
    g_url=url1+'/us/stock/nowprice/'+type+'/'+token
    return g_url
if __name__ == '__main__':
    ll=now_data(type='us',token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='hk', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='eu', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='tsx', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='cp', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='index', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='fx', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)
    ll = now_data(type='aapl', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)

    ll = now_data(type='%5EGSPC', token='j2c4291a77c3ea30ebb85fa883a6235dc4g8')
    print(ll)



