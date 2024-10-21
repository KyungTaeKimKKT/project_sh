import sys, traceback
from PyQt6 import QtCore, QtGui, QtWidgets, sip
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import json
import pandas as pd
import urllib
from datetime import date, datetime
from pprint import pprint
import cv2
import time

# import user module
from modules.user.api import Api_SH
from modules.user.async_api import Async_API_SH
import modules.PyQt.Qthreads as QThs
import modules.user.utils as utils

# from .update import Update

from info import Info

from modules.Ui.Ui_건조로_카메라 import Ui_Form

camURLs = ['192.168.14.100:10500', '192.168.14.101:10501',
		'192.168.14.102:10502','192.168.14.103:10503',
		'192.168.14.104:10504', '192.168.14.105:10505', '192.168.14.106:10506',
        '192.168.14.107:10507',
		'192.168.14.108:10508', '192.168.14.109:10509','192.168.14.110:10510',
		'192.168.14.111:10511', '192.168.14.112:10512','192.168.14.113:10513',
		'192.168.14.115:10515',
]

def get_RTSP_url(index:int) ->str :
    return f"rtsp://admin:1q2w3e4r5*!!@{camURLs[index]}"

class RTSP(QThread):
	signal_OCR = pyqtSignal(int, object,) 
	
	def __init__(self, index):
		super().__init__()
		# self.url = url
		self.index = index
		self.is_on = True
		self.cap = None

	#### main run
	def run(self):
		prev_time = 0
		FPS = 1
		# self.fname = self.__get_fName()
		while self.is_on :
			now = time.time()
			경과시간 = now - prev_time
			try:
				if self.cap is None:
					self.cap = cv2.VideoCapture(get_RTSP_url(self.index))
				ret, self.frame = self.cap.read()
				if not ret: 
					continue
				else:
					if 경과시간 > 1/FPS :
						prev_time = time.time()
						self.signal_OCR.emit( self.index, self.frame)
			### cap open fail시 signal 보내고 종료
			except Exception as e:
				print ( 'captrue error:', e)
				# self.close()			
	
	def stop(self):
		self.is_on = False



class Wid_건조로_카메라(QtWidgets.QWidget ):
	def __init__(self, parent, async_API:object, apiURL:str='', wsURL:str=''):        
		super().__init__(parent)     
		self.parent = parent
		self.async_API = async_API
		self.async_API : Async_API_SH
		self.apiURL = apiURL
		self.wsURL = wsURL        
		self.progress_obj = {}
		
		self.ui = Ui_Form()

		self.UI()

		self.run()

	def UI(self) -> None:
		""" init, render  UI"""
		self.ui.setupUi(self)

		self.displayDict = {
			1:[self.ui.label_title_1, self.ui.label_img_1],
			2:[self.ui.label_title_2, self.ui.label_img_2],
			3:[self.ui.label_title_3, self.ui.label_img_3],
			4:[self.ui.label_title_4, self.ui.label_img_4],
			5:[self.ui.label_title_5, self.ui.label_img_5],
			6:[self.ui.label_title_6, self.ui.label_img_6],
			7:[self.ui.label_title_7, self.ui.label_img_7],
			8:[self.ui.label_title_8, self.ui.label_img_8],
			9:[self.ui.label_title_9, self.ui.label_img_9],
			10:[self.ui.label_title_10, self.ui.label_img_10],
			11:[self.ui.label_title_11, self.ui.label_img_11],
			12:[self.ui.label_title_12, self.ui.label_img_12],			
			13:[self.ui.label_title_13, self.ui.label_img_13],
			14:[self.ui.label_title_14, self.ui.label_img_14],
			15:[self.ui.label_title_15, self.ui.label_img_15],
			16:[self.ui.label_title_16, self.ui.label_img_16],	
		}

	def run(self):
		# https://realpython.com/python-pyqt-qthread/
		self.pool = QThreadPool.globalInstance()
		self.rtsp_pool = []
		for index, _ in enumerate( camURLs):
			ocr_rtsp =RTSP(index)
			self.rtsp_pool.append(ocr_rtsp)
			self.displayDict[index+1][0].setText( camURLs[index])
			ocr_rtsp.signal_OCR.connect( self.handle_rtsp_img )

			self.pool.start(ocr_rtsp.run )



	@pyqtSlot( int, object)
	def handle_rtsp_img(self, cam_index:int, image:object):
		if image is not None and cam_index :
			self.render_img_to_label( cam_index, image )


	def render_img_to_label(self, cam_index:int, image:object):
		rgb_image = cv2.cvtColor( image, cv2.COLOR_BGR2RGB)

		qImg = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format.Format_RGB888)
		qImg = qImg.scaled (200,200)

		self.displayDict[cam_index+1][1].setPixmap( QPixmap.fromImage(qImg))
		self.displayDict[cam_index+1][1].setScaledContents(True)

	def close(self):
		print ( 'closing : Wid_건조로_카메라')
		for obj in self.rtsp_pool:
			obj.stop()
		self.pool.clear()

	def closeEvent(self, event:QtCore.QEvent):
		self.close()
		event.accept()

		