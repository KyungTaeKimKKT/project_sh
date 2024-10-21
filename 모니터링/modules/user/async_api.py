from PyQt6.QtCore import QThread, pyqtSignal, QObject

import asyncio
import aiohttp

from info import Info as INFO


class Async_API_SH(QObject):
	signal_login = pyqtSignal(bool)
	signal_Process = pyqtSignal(int, int)
	signal_Finished = pyqtSignal(dict)
	signal_Response = pyqtSignal(object)

	def __init__(self,parent=None):
		super().__init__(parent)
		self.refresh = ''
		self.access = ''
		#### 
		
		# self.headers = self.__get_header()

	def Login(self) -> None:
		return asyncio.run( self.__login__() )

	async def __login__(self) :
		async with aiohttp.ClientSession() as session:
			async with session.post( url=INFO.AUTH_URL, data=INFO.UserInfo ) as response:
				if response.ok:
					res_data = await response.json()
					self.refresh = res_data.get('refresh')
					self.access = res_data.get('access')			
					# self.signal_login.emit()		
				else:
					print ('login error:', response.status )
					# self.signal_login.emit()	
				return response.ok

	def __get_header(self) -> dict:
		return {
				'Authorization'  : 'JWT '+ self.access
			}

	async def fetch(self, url):
		async with aiohttp.ClientSession(
			base_url= INFO.baseURL_API,
			headers=self.__get_header()
		) as session:
			async with session.get( url) as response:
				_json = {}
				if response.ok: # 요청 성공
					_json = await response.json()
					# print('결과:', _json ) # await 주의
				else: # 요청 실패
					print('실패 상태 코드:', response.status)       
				return _json

	def Get(self, url):
		return asyncio.run( self.fetch(url))
	
	async def post ( self, url, data) ->None:
		async with aiohttp.ClientSession(
			base_url= INFO.URI,
			headers=self.__get_header()
		) as session:
			async with session.post( url=url, data=data) as response:
				print ( response.status)
				if response.status == 200: # 요청 성공
					sendData = await response.json()
					print (sendData )
					self.signal_Response.emit(sendData )
				else: # 요청 실패
					print('실패 상태 코드:', response.status)  
					self.signal_Response.emit(None)
	
	async def post_getContents(self, url, data) -> None:
		async with aiohttp.ClientSession(
			base_url= INFO.URI,
			headers=self.__get_header()
		) as session:
			async with session.post( url=url, data=data) as response:
				if response.ok: # 요청 성공
					header = response.headers
					empty_bytes = b''
					result = empty_bytes
					Total_cnt = int( header.get('Content-Length') )
					count = 0
					prevProgress = 0
					buf_size = 128
					while True:
						progress =  int( count*buf_size / Total_cnt * 100 )
						# print ( prevProgress, progress, bool( not prevProgress == progress ))
						if not prevProgress == progress:
							prevProgress = progress
							self.signal_Process.emit( progress , Total_cnt )

						chunk = await response.content.read(buf_size)
						if chunk == empty_bytes:
							break
						result += chunk
						count +=1
					# 😀TypeError: a bytes-like object is required, not 'StreamReader'
					# content = response.content
					self.signal_Finished.emit({
						'headers' :header,
						'contents' : result,
					})
					# return (header, result)
					# _json = await response.json()
					# # print('결과:', _json ) # await 주의
					# return _json
				else: # 요청 실패
					print('실패 상태 코드:', response.status)  
					self.signal_Finished({
						'headers' : None,
						'contents' : None,
					})
	
	def Post_getContents(self, url, data):
		asyncio.run ( self.post_getContents(url, data ))

	def Post(self, url, data):
		asyncio.run ( self.post(url, data) )