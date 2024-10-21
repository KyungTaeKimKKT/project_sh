from apscheduler.schedulers.blocking import BlockingScheduler
from asyncio import run, Queue, create_task
# from ping3 import ping
from aioping import ping
import requests, datetime, json
import time
import websocket
import os

import pydot_ as PyDot

from ws_client import WS_Client as WS

API_적용_URL = 'http://192.168.7.108:9999'

API_URL_사내IP_DB = f'{API_적용_URL}/모니터링/사내IP-DB/?page_size=0'
API_URL_사내IP_RESULT_IMG = f'{API_적용_URL}/모니터링/사내IP-PING결과_IMAGE/'

WS_URL_사내IP_RESULT_IMG  = 'ws://192.168.7.108:9998/broadcast/ping_result/'

TIME_OUT = 4 ## 초단위
MAX_QUEUE = 256
RETRY = False

############################
## https://stackoverflow.com/questions/75682507/taking-advantage-of-both-async-and-multithreading-to-make-rapid-code-in-python
############################

async def ping_host(host:str, taskQueue:Queue, resultsQueue:Queue, timeout:int, retry:bool=False):
	try:
		delay = await ping(host, timeout)
		await resultsQueue.put([True, host, delay])
	except TimeoutError:
		if retry:
			try:
				delay = await ping(host, timeout)
				await resultsQueue.put([True, host, delay])
			except: await resultsQueue.put([False, host, f"{host} timed out (retried)."])
		else: await resultsQueue.put([False, host, f"{host} timed out."])
	taskQueue.task_done()
	taskQueue.get_nowait()

async def async_ping_Hosts( pingList :list ) -> list:
	s = time.time()
	results = []
	taskQueue: Queue = Queue(maxsize=MAX_QUEUE)
	resultsQueue: Queue = Queue()

	for pingObj in pingList:
		pingObj:dict
		await taskQueue.put( create_task ( ping_host(pingObj.get('IP_주소'), taskQueue, resultsQueue, TIME_OUT, RETRY)))
		# result.append(ping(pingObj.get('IP_주소'), timeout=TIME_OUT))
	
	await taskQueue.join()
	while not resultsQueue.empty():
		results.append(await resultsQueue.get())
		resultsQueue.task_done()
	await resultsQueue.join()


	# print('ping 소요시간:', time.time() - s)
	# print( results )
	return results

def get_ping_list( url:str=API_URL_사내IP_DB  ) -> list:
	try:
		s = time.time()
		res = requests.get( url)
		if res.ok:
			# print ( res.json() )
			return res.json()
			# ws.send ( json.dumps( _get_sendMsg( msg=res.json()) , ensure_ascii=False ) )
		else:
			print ( f'{url} FETCH ERROR')
		# print ( '모니터링-소요시간 :', time.time() - s )
	except Exception as e:
		print (f'{url} request error:', e)
	
	return []

async def main(ws):
	ping_lists = get_ping_list() 
	results = await async_ping_Hosts( ping_lists  )
	# PyDot.test()

	filepath = PyDot.main( ping_lists, results )
	res = requests.post(url=API_URL_사내IP_RESULT_IMG , files= {'file':open(filepath, 'rb') })
	os.remove(filepath)
	if res.ok:
		# ws =websocket.create_connection(WS_URL_사내IP_RESULT_IMG )
		ws.send( json.dumps({
			"type":"broadcast",
			"sender":"system",
			"message" : res.json(),
			"send_time" :  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
		} , ensure_ascii=False) ) 
		# print ( res.json() )

	else:
		print ( 'ping결과 post error:', res.status_code )

	# print ( 'main:', results)


if __name__ == '__main__':
	ws = WS(WS_URL_사내IP_RESULT_IMG)
	ws.run()

	run( main(ws) )

	scheduler = BlockingScheduler(job_defaults={'max_instances': 1})
	scheduler.add_job(lambda: run( main(ws) ), trigger='interval', seconds=30  , id='network')
	# scheduler.add_job( ws_기상청, trigger='interval', seconds=30,  args=[ws], id='ws_기상청')
	scheduler.start()

	# run ( main(ws) )
	# run (async_ping_Hosts( get_ping_list() ) ).
	# ping_result = async_ping( get_ping_list())