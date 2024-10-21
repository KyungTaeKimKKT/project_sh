# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import requests, datetime, json
from websocket import create_connection
from urllib.parse import urlencode, quote_plus, unquote

results = []
send_count = 0

WS_URL_기상청 = 'ws://192.168.10.249:9998/broadcast/weather/'

def api_기상청(nx=69, ny=115):
    nx = 69
    ny = 115
    objWeather = {}
    # nx = nx if nx is not None else 69
    # ny = ny if ny is not None else 115
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    # serviceKey = "VOAgXeeBTZflpY2X2s%2BCzGoqgi2McJlHnzVYD1DGh%2Fux8X%2BIo1OjaglLPkLSLLKN4lE5kmZRA30XIBjzV5XTXA%3D%3D"
    serviceKey = "LMM%2FCWJCmoQdcWolP63E8%2Fs7yf3OLQ4ZyYzqbvGsPWhGj6R76dHHnah2enePqGxVBtdgeZtIySfREk%2FT2lrapg%3D%3D"
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

    now = datetime.datetime.now()
    print ( now )
    today = datetime.date.today().strftime("%Y%m%d")
    y = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")
    print ( now.hour, type(now.hour))

    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2330"
            base_date = yesterday
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
            base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
            
    base_date = today


    queryParams = '?' + urlencode({ quote_plus('serviceKey')    : serviceKeyDecoded, 
                                    quote_plus('pageNo')        :'1',
                                    quote_plus('numOfRows')     :'100',
                                    quote_plus('dataType')      : 'json', 
                                    quote_plus('base_date')     : base_date,
                                    quote_plus('base_time')     : base_time, 
                                    quote_plus('nx') : nx, quote_plus('ny') : ny,
                                    })

    try:
        print ( base_date, base_time )
        response = requests.get(url + queryParams, verify=False)
        # res_data = json.loads( response.text )
        # print ( res_data  )
        items_json = response.json().get('response').get('body').get('items').get('item')
        SKY = {
            '1': '맑음',
            '2': '맑음',
            '3': '구름많음',
            '4': ' 흐림',
        }
        PTY = {
            '0':'강수없음',
            '1':'비',
            '2':'비/눈',
            '3':'눈',
            '5':'빗방물',
            '6':'빗방울눈날림',
            '7':'눈날림'
        }

        print (  {obj.get('category'):obj['fcstValue']} for obj in items_json if obj.get('fcstTime') == '1700' )

        fcstTimes = list(set([ obj['fcstTime'] for obj in items_json ]) )
        fcstTimes.sort()
        global results
        results = []
        for fcstTime in fcstTimes:
            objWeather = {}
            filterList = [ obj for obj in items_json if obj['fcstTime'] == fcstTime ]
            objWeather['fcstTime'] = fcstTime
            for obj in filterList:
               objWeather[obj.get('category') ] = obj['fcstValue']
            results.append(objWeather)
        print(results)

        # print ( items_json )
        # for obj in items_json:        
        #     # results.append ( obj)
        #     # if obj['fcstTime'] == getBaseTime() :
        #     objWeather['fcstTime'] = obj['fcstTime']
        #     objWeather[obj.get('category') ] = obj['fcstValue']
        #     print ( objWeather)
        #     if obj.get('category') == 'WSD':
        #         results.append(objWeather)
        # print (results)
    except Exception as e:
        print ( e )



def ws_기상청():
    global send_count
    # print ( 'ws:',results[send_count])
    try:
        if results :
            ws = create_connection(WS_URL_기상청)
            # print ( ws )
            ws.send ( json.dumps( { "type":"broadcast", "message": results[send_count] }, ensure_ascii=False ) )
            send_count += 1
            if send_count == len(results):
                send_count = 0
            ws.close()
        else:
            print ('기상청 data Empty')
    except Exception as e:
        print ('WS ERROR:', e)
        ws.close()


def getBaseTime():
    now = datetime.datetime.now()
    after_hour = now.hour+1
    print ( after_hour , type(after_hour))
    if after_hour<10:
        base_time = "0" + str(after_hour) + "00"
    else:
        base_time = str(after_hour) + "00"
    return base_time

def str_to_time (str):
    # str = '1900'  ==> time  ' 19:00:00'
    time_str = f"{str[0:2]}:{str[2:]}:00"
    return datetime.strptime(time_str, '%H:%M:%S').time()

def str_to_date (str):
    # str = '20220811'  ==> date '2022-08-11'
    date_str = f"{str[0:4]}-{str[4:6]}-{str[6:]}"    
    return datetime.strptime( date_str, "%Y-%m-%d" ).date()


if __name__ == '__main__':
    api_기상청()
    # scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler(job_defaults={'max_instances': 3})
    scheduler.add_job(api_기상청, trigger='interval', minutes=10 , id='기상청')
    scheduler.add_job( ws_기상청, trigger='interval', seconds=30,  id='ws_기상청')
    scheduler.start()