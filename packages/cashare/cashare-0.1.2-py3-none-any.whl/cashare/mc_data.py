import httpx
from cashare.common.dname import url1
import pandas as pd
import datetime
import json
#获取单个股票市值
def mark_c_data(code,token,start_date,end_date=str(datetime.date.today().strftime('%Y-%m-%d'))):
    if start_date > (datetime.date.today().strftime('%Y-%m-%d')):
        return "start_date大于现在时间"
    elif start_date > end_date:
        return "start_date大于end_date"
    elif end_date > (datetime.date.today().strftime('%Y-%m-%d')):
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    else:
        pass
    url = url1 + '/mc/'+code+'/'+start_date+'/'+end_date+'/'+token
    r = httpx.get(url,timeout=100)

    df=pd.DataFrame(r.json())
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    filtered_df = df[(df['date'] >= str(start_date)) & (df['date'] <= str(end_date))]
    df_reset = filtered_df.reset_index(drop=True)
    return df_reset
if __name__ == '__main__':
    df=mark_c_data(code='AAPL',token='you_token',start_date='2022-09-05',end_date='2022-09-09')
    print(df)
    pass



