import sys, traceback
from PyQt6 import QtCore, QtGui, QtWidgets, sip
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtSvgWidgets, QtSvg
import json
import pandas as pd
import urllib
from datetime import date, datetime
from pprint import pprint

# import user module
# from modules.Ui.Ui_page_network_ping import Ui_Wid_ping_result
# from modules.Ui.Ui_page_network_ping_graphicview import Ui_Wid_ping_result
from modules.Ui.Ui_page_network_ping_svgwidget import Ui_Wid_ping_result


from modules.user.api import Api_SH
from modules.user.async_api import Async_API_SH
import modules.PyQt.Qthreads as QThs
import modules.user.utils as utils
from analog_clock import Clock
# from .update import Update

from info import Info


class Wid_Network_Status(QtWidgets.QWidget ):
	def __init__(self, parent, async_API:object, apiURL:str='', wsURL:str=''):        
		super().__init__(parent)    
		self.parent = parent    
		self.async_API = async_API
		self.async_API : Async_API_SH
		self.apiURL = apiURL
		self.wsURL = wsURL        

		self.is_first = True
		self.ui = Ui_Wid_ping_result()
		self.ui.setupUi(self)
		### add svg widget
		self.wid_svg = QtSvgWidgets.QSvgWidget()
		self.ui.vLayout_svg.addWidget( self.wid_svg )
		
		### init
		self.__init__WS(self.wsURL)
		# self.__init__API()

		self.timer_1sec = QTimer()
		self.timer_1sec.timeout.connect(self.slot_Timer_1sec)
		self.timer_1sec.start(1000)

		self.is_Analog_Clock_Active = False

	def close(self):
		print ('close : web socket closing')
		# self.ws.close()

	def closeEvent(self, event:QtCore.QEvent):
		self.close()
		self.ws.close()
		event.accept()

	# def UI(self) -> None:
	# 	""" init, render  UI"""
	# 	if hasattr(self, 'vlayout') : self.deleteLayout(self.vlayout)

	# 	self.vlayout = QtWidgets.QVBoxLayout()
	# 	self.vlayout.setContentsMargins( 0,0,0,0)
	# 	self.vlayout.setSpacing(1)
	# 	self.setLayout(self.vlayout)

	def __init__WS(self,  wsUrl:str):		
		self.ws = QThs.User_WS_Client(wsUrl)
		self.ws.Message.connect(self.slot_WS_Message)
		self.ws.start()

	def __init__API(self):
		# self.async_API = Async_API_SH()
		# self.async_API.signal_login.connect( self.slot_api_login )
		# self.async_API.signal_Finished.connect( self.slot_api_Finished  )
		_json = self.async_API.Get(self.apiURL )
		# print ( _json )
		if _json:
			self.gen_table(msgList=_json)
		else:
			print ( 'fetch error:')


	# def resizeEvent(self, event):
	#     print ("resize :", self.width(), self.height() )
	#     self.ui.Win_width = self.width()
	#     self.ui.Win_height = self.height()
	#     QtWidgets.QMainWindow.resizeEvent(self, event)


###############slot##############################
	@pyqtSlot()
	def slot_Timer_1sec(self):
		pass
   
	@pyqtSlot(dict)
	def slot_WS_Message(self, _json:dict):
		# {"type": "broadcast", "sender": "system", "message": {"id": 4, "file": "http://192.168.7.108:9999/media/%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81/ping_image/0c23b225-e26b-463b-bd4d-9e71a5cc28cb/2024-10-18T14101729229032.png", "timestamp": "2024-10-18T14:23:52.398768"}, "send_time": "2024-10-18T14:23:52"}
		if not _json : return

		match _json.get('type'):
			case 'broadcast':
				messageContents = _json.get('message')
				if messageContents:
					# self.render_Result(messageContents)
					# self.render_Result_in_graphview(messageContents)
					self.render_Result_svg(messageContents)

				else:
					print ( 'ws_message empty!!!:')


#################################################
	def render_Result(self, msg:dict) -> None:
		width = 1000
		height = 700
		pixmap = self._getPixMapFromUrl(url=msg.get('file'))

		pixmap = pixmap.scaled(
			width,
			height,
			QtCore.Qt.AspectRatioMode.KeepAspectRatio,
			QtCore.Qt.TransformationMode.SmoothTransformation
		)
		self.ui.label_img_ping_result.setPixmap ( pixmap )
		self.ui.label_img_ping_result.adjustSize() 
		self.ui.label_timestamp.setText(msg.get('timestamp'))

	def render_Result_in_graphview(self, msg:dict) ->None:
		# pic = QGraphicsPixmapItem()
		# pic.setPixmap( self._getPixMapFromUrl(url=msg.get('file')) )
		scene = QGraphicsScene()
		scene.addPixmap( self._getPixMapFromUrl(url=msg.get('file')) )
		# scene.setSceneRect(0, 0, 1000, 800)
		self.ui.graphicsView.setScene(scene)
	
	def render_Result_svg(self, msg:dict) -> None:
		data = urllib.request.urlopen(msg.get('file')).read()
		self.wid_svg.renderer().load ( data)
		self.ui.label_timestamp.setText(msg.get('timestamp'))

	def _getPixMapFromUrl(self, url:str) -> QPixmap:
		data = urllib.request.urlopen(url).read()
		image = QImage()
		image.loadFromData(data)
		return QPixmap(image)
	
	def _getQImageFromUrl(self, url:str) -> QImage:
		data = urllib.request.urlopen(url).read()
		image = QImage()
		image.loadFromData(data)
		return image

	def deleteLayout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.deleteLayout(item.layout())
			sip.delete(layout)


