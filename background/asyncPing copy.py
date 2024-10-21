from asyncio import run, Queue, create_task
from ping3 import ping
import requests, datetime, json
import time

API_URL_사내IP_DB = 'http://192.168.7.108:9999/모니터링/사내IP-DB/?page_size=0'
TIME_OUT = 1 ## 초단위
MAX_QUEUE = 256

async def async_ping( ip:str, timeout:int ) :
	return ping ( ip, timeout)

async def async_ping_Hosts( pingList :list ) -> list:
	s = time.time()
	results = []
	taskQueue: Queue = Queue(maxsize=MAX_QUEUE)
	resultsQueue: Queue = Queue()

	for pingObj in pingList:
		pingObj:dict
		await taskQueue.put( create_task ( async_ping(pingObj.get('IP_주소'), timeout=TIME_OUT) ))
		# result.append(ping(pingObj.get('IP_주소'), timeout=TIME_OUT))
	
	await taskQueue.join()
	while not resultsQueue.empty():
		results.append(await resultsQueue.get())
		resultsQueue.task_done()
	await resultsQueue.join()


	print('ping 소요시간:', time.time() - s)
	print( results )
	return results

def get_ping_list( url:str=API_URL_사내IP_DB  ) -> list:
	try:
		s = time.time()
		res = requests.get( url)
		if res.ok:
			print ( res.json() )
			return res.json()
			# ws.send ( json.dumps( _get_sendMsg( msg=res.json()) , ensure_ascii=False ) )
		else:
			print ( f'{url} FETCH ERROR')
		# print ( '모니터링-소요시간 :', time.time() - s )
	except Exception as e:
		print (f'{url} request error:', e)
	
	return []


if __name__ == '__main__':
	run (async_ping_Hosts( get_ping_list() ) )
	# ping_result = async_ping( get_ping_list())