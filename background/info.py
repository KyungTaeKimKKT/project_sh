class Info :
    양산URL_API = 'http://mes.swgroup.co.kr'
    개발URL_API = 'http://192.168.7.108'

    양산URL_WS = 'ws://192.168.10.249'
    개발URL_WS = 'ws://192.168.7.108'

    PORT_API = '9999'
    PORT_WS  = '9998'

    적용URL_API = 양산URL_API
    # 적용URL_API = 개발URL_API
    # 적용URL_WS = 양산URL_WS
    적용URL_WS = 개발URL_WS

    With_No_Page = '?page_size=0'

    baseURL_API = 적용URL_API + ':' + PORT_API
    baseURL_WS = 적용URL_WS + ':' + PORT_WS

    AUTH_URL = baseURL_API + '/api-auth/jwt/'

    UserInfo = {'user_mailid':'admin', 'password':'1q2w3e4r5*!!'}

    ### URL APIS
    URL_생산DATA = '/생산모니터링/KISOK/당일계획실적/'
    URL_무재해DB = '/생산모니터링/무재해db/'

    ### URL WS
    URL_WS_기상청 = baseURL_WS + '/broadcast/weather/'
    URL_WS_생산모니터링 = baseURL_WS + '/broadcast/production_monitoring/'
    URL_WS_NETWORK_STATUS = baseURL_WS + '/broadcast/ping_result/'

    ### 기상청 const
    URL_기상청_공공DATA =  "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    ServiceKey_기상청_공공DATA =  "LMM%2FCWJCmoQdcWolP63E8%2Fs7yf3OLQ4ZyYzqbvGsPWhGj6R76dHHnah2enePqGxVBtdgeZtIySfREk%2FT2lrapg%3D%3D"