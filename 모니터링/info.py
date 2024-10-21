class Info:
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

    ### CONST
    생산모니터링_TABLE_HEADERS =  ['line_no','생산capa', 'start_time', 'end_time', 'plan_qty', 'job_qty', '달성률', '운영가동률','운영tt','status']   
    생산모니터링_TABLE_HEADERS_Display =  ['공정명','생산Capa', '시작', '종료', '계획수량', '투입수량', '달성률', '운영가동률','운영TT','Status']  
    생산모니터링_Table_생산UpTime = 10 ### 10초미만이면 생산up 표시