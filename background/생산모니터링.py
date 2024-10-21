# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import requests, datetime, json
from websocket import create_connection
from urllib.parse import urlencode, quote_plus, unquote
import time

from ws_client import WS_Client as WS


API_URL_생산모니터링 = 'http://192.168.10.249:9999/생산모니터링/KISOK/당일계획실적/?page_size=0'
WS_URL_생산모니터링 = 'ws://192.168.10.249:9998/broadcast/production_monitoring/'

def api_생산모니터링(ws:WS, url:str =API_URL_생산모니터링):
	try:
		s = time.time()
		res = requests.get(url)
		if res.ok:
			ws.send ( json.dumps( _get_sendMsg( msg=res.json()) , ensure_ascii=False ) )
		else:
			print ( f'{url} FETCH ERROR')
		# print ( '모니터링-소요시간 :', time.time() - s )
	except Exception as e:
		print (f'{url} request error:', e)
 
def _get_sendMsg(msg) -> dict:
	return {
		"type" : "broadcast",
		"sender" : "system",
		"message" : msg,
		"send_time" :  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	}

if __name__ == '__main__':
	ws = WS(WS_URL_생산모니터링)
	ws.run()

	# scheduler = BackgroundScheduler()
	scheduler = BlockingScheduler(job_defaults={'max_instances': 5})
	scheduler.add_job( api_생산모니터링, trigger='interval', seconds=1 , args=[ws], id='api_생산모니터링' )
	scheduler.start()

