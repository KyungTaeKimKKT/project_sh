import sys, traceback
from PyQt6 import QtCore, QtGui, QtWidgets, sip
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import json
import pandas as pd
import urllib
from datetime import date, datetime
from pprint import pprint

# import user module
from modules.user.api import Api_SH
from modules.user.async_api import Async_API_SH
import modules.PyQt.Qthreads as QThs
import modules.user.utils as utils

# from .update import Update

from info import Info

from modules.Ui.Ui_생산모니터링_circular import Ui_Form


class Wid_생산모니터링_Circular(QtWidgets.QWidget , Ui_Form):
	def __init__(self, parent, async_API:object, apiURL:str='', wsURL:str=''):        
		super().__init__(parent)     
		self.parent = parent
		self.async_API = async_API
		self.async_API : Async_API_SH
		self.apiURL = apiURL
		self.wsURL = wsURL        
		self.progress_obj = {}

		self.UI()
		
		### init
		self.__init__WS(self.wsURL)
		self.__init__API()

		# self.timer_1sec = QTimer()
		# self.timer_1sec.timeout.connect(self.slot_Timer_1sec)
		# self.timer_1sec.start(1000)

	def close(self):
		print ('close : web socket closing')
		# self.ws.close()

	def closeEvent(self, event:QtCore.QEvent):
		self.close()
		self.ws.close()
		event.accept()


	def UI(self) -> None:
		""" init, render  UI"""
		self.setupUi(self)

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
			self.gen_Progress_Body(msgList=_json)
		else:
			print ( 'fetch error:')

	def gen_Progress_Body(self, msgList=list):
		for msgDict in msgList:
			match msgDict.get('line_no'):
				case 'MAIN1':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
				case 'MAIN2':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
				case 'MAIN3':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
				case 'M/T-1':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
				case 'M/T-2':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
				case 'INK-PRT':
					self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
				case 'P4-LEAN':
					self.gen_Progress_Frame(parentObj=self.frame_PO1, msgDict=msgDict)
				case 'RIOR':
					self.gen_Progress_Frame(parentObj=self.frame_PO1, msgDict=msgDict)
				case 'UHC':
					self.gen_Progress_Frame(parentObj=self.frame_PO2, msgDict=msgDict)
				case '폴리401':
					self.gen_Progress_Frame(parentObj=self.frame_PO2, msgDict=msgDict)
				case _:
					pass



	def gen_Progress_Frame(self, parentObj, msgDict=dict):
		line_no = msgDict.get('line_no')
		w_frame = int(300*self.parent.width() / 1749)
		x_start = 0 + int( (w_frame -300) / 2 )
		# print ('resize: ', w_frame, x_start)
		if ( x_start > 0 ):
			self.progress_obj[line_no]['prod'].setGeometry(QtCore.QRect(x_start, 0, 300, 300))
			self.progress_obj[line_no]['tt'].setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
			# self.progress_obj[line_no]['label_lineNo'].setGeometry(QtCore.QRect(x_start+20, 50, 181, 41))
			# self.progress_obj[line_no]['label_prodQty'].setGeometry(QtCore.QRect( x_start+30, 130, 161, 61))
			self.progress_obj[line_no]['prod_bg'].setGeometry(QtCore.QRect(x_start, 0, 300, 300))
			self.progress_obj[line_no]['tt_bg'].setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
			self.progress_obj[line_no]['container'].setGeometry(QtCore.QRect(x_start+40, 40, 220, 220))

		def render_생산up(obj,is_up=False):
			if is_up:
				obj.setStyleSheet("QFrame{\n"
								"    border-radius: 110px;    \n"
								"    background-color: yellow;\n"
								"}")
			else:
				obj.setStyleSheet("QFrame{\n"
								"    border-radius: 110px;    \n"
								"    background-color: rgb(58, 58, 102);\n"
								"}")

		def render_status_by_(obj,msgList=list):
			text = obj.text()
			if ( msgList[0] == text ):
				obj.setText(msgList[1])
			else:
				obj.setText(msgList[0])

		frame_name = f'circularProgressBar_{line_no}'

		frame_TT_Prog_Name = f'circular_TT_Progress_{line_no}'
		if getattr(self, frame_name, None) is not None:
			job_qty = msgDict.get('job_qty')
			plan_qty = msgDict.get('plan_qty')
			운영tt = msgDict.get('운영tt')
			TT = msgDict.get('TT')
			status = msgDict.get('status')

			if job_qty>0 and plan_qty>0 and 운영tt <= 10 :
				render_생산up( self.progress_obj[line_no]['container'], True )
				self.progress_obj[line_no]['label_lineNo'].setStyleSheet('color:black;font-weight:bold')
				self.progress_obj[line_no]['label_prodQty'].setStyleSheet('color:black;font-weight:bold')
			else : 
				render_생산up( self.progress_obj[line_no]['container'], False )
				self.progress_obj[line_no]['label_lineNo'].setStyleSheet('color:white')
				self.progress_obj[line_no]['label_prodQty'].setStyleSheet('color:white')


			self.progress_obj[line_no]['label_lineNo'].setText(line_no)

			self.progressBarValue_Qty(obj=self.progress_obj[line_no]['prod'], value= job_qty/plan_qty*100 if plan_qty>0 else 0)
			self.progressBarValue_TT(obj=self.progress_obj[line_no]['tt'], value=운영tt, TT= TT) #msgDict.get('TT'))

			if status in ['휴식', '점심', '청소_저녁']:
				if ( getattr(self, f'timer_status_{line_no}', None)) is not None:
					pass
				else :
					setattr(self, f'timer_status_{line_no}', QTimer())
					status_timer = getattr(self,  f'timer_status_{line_no}')
					status_timer : QTimer
					status_timer.timeout.connect( lambda:render_status_by_(obj=self.progress_obj[line_no]['label_prodQty'], msgList=[str(job_qty) +'/' + str(plan_qty), status]) )
					status_timer.start(10*1000)
			else:
				self.progress_obj[line_no]['label_prodQty'].setText(str(job_qty) +'/' + str(plan_qty))
				if ( status_timer:=getattr(self, f'timer_status_{line_no}', None)) is not None:
					status_timer.stop()

			return None

		setattr(self, frame_name, QtWidgets.QFrame(parentObj))
		frame = getattr(self, frame_name )
		frame : QtWidgets.QFrame
		frame.setStyleSheet("background-color: none;")
		frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
		frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame.setObjectName(frame_name)


		### PRODUCT PROGRESS
		frame_Prod_Prog_Name = f'circular_Production_Progress_{line_no}'
		setattr(self, frame_Prod_Prog_Name, QtWidgets.QFrame(frame))
		frame_production_progress = getattr(self, frame_Prod_Prog_Name )
		frame_production_progress :  QtWidgets.QFrame
		# frame_production_progress.setGeometry(QtCore.QRect(0, 0, 300, 300))
		frame_production_progress.setGeometry(QtCore.QRect(x_start, 0, 300, 300))
		styleSheet = """
			QFrame{
				border-radius: 150px;
				background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.957 rgba(0, 0, 255, 255), stop:0.956 rgba(0, 0, 255, 0));
				}
		
		"""

		frame_production_progress.setStyleSheet(styleSheet)
		frame_production_progress.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame_production_progress.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame_production_progress.setObjectName(frame_Prod_Prog_Name)


		frame_Prod_Bg_Name = f'circular_Production_Progress_{line_no}'
		setattr(self, frame_Prod_Bg_Name, QtWidgets.QFrame(frame))
		frame_production_bg = getattr(self, frame_Prod_Bg_Name )
		frame_production_bg :QtWidgets.QFrame

		frame_production_bg.setGeometry(QtCore.QRect(x_start, 0, 300, 300))
		frame_production_bg.setStyleSheet("QFrame{\n"
										"    border-radius: 150px;    \n"
										"    background-color: rgba(85, 85, 127, 100);\n"
										"}")
		frame_production_bg.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame_production_bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame_production_bg.setObjectName(frame_Prod_Bg_Name)

		##circularContainer
		frame_Circular_Container_Name = f'circular_container_{line_no}'
		setattr(self, frame_Circular_Container_Name, QtWidgets.QFrame(frame))
		frame_Circular_Container = getattr(self, frame_Circular_Container_Name )
		frame_Circular_Container : QtWidgets.QFrame

		frame_Circular_Container.setGeometry(QtCore.QRect(x_start+40, 40, 220, 220))
		frame_Circular_Container.setBaseSize(QtCore.QSize(0, 0))
		frame_Circular_Container.setStyleSheet("QFrame{\n"
										"    border-radius: 110px;    \n"
										"    background-color: rgb(58, 58, 102);\n"
										"}")
		frame_Circular_Container.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame_Circular_Container.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame_Circular_Container.setObjectName("frame_Circular_Container_Name")

		### label LineNo
		label_lineNo_name = f'label_LineNo_{line_no}'
		setattr(self, label_lineNo_name, QtWidgets.QLabel(frame_Circular_Container))
		label_lineNo = getattr(self, label_lineNo_name )
		label_lineNo:QtWidgets.QLabel

		label_lineNo.setGeometry(QtCore.QRect(x_start+20, 50, 181, 41))
		font = QtGui.QFont()
		font.setPointSize(32)
		label_lineNo.setFont(font)
		label_lineNo.setStyleSheet("color:white")
		label_lineNo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		label_lineNo.setObjectName(label_lineNo_name)

		### label 생산수량
		label_prodQty_name = f'label_prodQty_{line_no}'
		setattr(self, label_prodQty_name, QtWidgets.QLabel(frame_Circular_Container))
		label_prodQty = getattr(self, label_prodQty_name )
		label_prodQty : QtWidgets.QLabel
		label_prodQty.setGeometry(QtCore.QRect( x_start+30, 130, 161, 61))
		font = QtGui.QFont()
		font.setPointSize(32)
		label_prodQty.setFont(font)
		label_prodQty.setStyleSheet("color:white")
		label_prodQty.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		label_prodQty.setObjectName(label_prodQty_name)

		### TT PROGRESS
		frame_TT_Prog_Name = f'circular_TT_Progress_{line_no}'
		setattr(self, frame_TT_Prog_Name, QtWidgets.QFrame(frame))
		frame_TT_progress = getattr(self, frame_TT_Prog_Name )
		frame_TT_progress : QtWidgets.QFrame
		frame_TT_progress.setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
		frame_TT_progress.setStyleSheet("QFrame{\n"
											"    border-radius: 130px;    \n"
											"    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.49 rgba(255, 0, 0, 0), stop:0.5 rgba(255, 0, 0, 255));\n"
											"}")
		frame_TT_progress.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame_TT_progress.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		# frame_TT_progress.setObjectName(frame_TT_Prog_Name)

		### TT BG
		frame_TT_Bg_Name = f'circular_TT_Progress_{line_no}'
		setattr(self, frame_TT_Bg_Name, QtWidgets.QFrame(frame))
		frame_TT_Bg = getattr(self, frame_TT_Bg_Name )



		frame_TT_Bg = QtWidgets.QFrame(frame)
		frame_TT_Bg.setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
		frame_TT_Bg.setStyleSheet("QFrame{\n"
										"    border-radius: 130px;    \n"
										"    background-color: rgb(225,225,225);\n"
										"}")
		frame_TT_Bg.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame_TT_Bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame_TT_Bg.setObjectName("circular_TT_Bg")
		frame_production_progress.raise_()
		frame_TT_Bg.raise_()
		frame_production_bg.raise_()
		frame_TT_progress.raise_()
		frame_Circular_Container.raise_()

		if line_no in ['MAIN1', 'MAIN2', 'MAIN3']:
			self.h_layout_frame_HI_BASE.addWidget(frame)
		elif line_no in ['M/T-1','M/T-2','INK-PRT']:
			self.h_layout_frame_HI_BASE_2.addWidget(frame)
		elif line_no in ['P4-LEAN', 'RIOR']:
			self.h_layout_frame_PO1.addWidget(frame)
		else:
			self.h_layout_frame_PO2.addWidget(frame)

		self.progress_obj[line_no] ={
			'prod':frame_production_progress,
			'tt':frame_TT_progress,
			'label_lineNo':label_lineNo,
			'label_prodQty':label_prodQty,
			'container':frame_Circular_Container,
			'prod_bg':frame_production_bg,
			'tt_bg':frame_TT_Bg,
		}


	def progressBarValue_Qty(self, obj, value):
		# PROGRESSBAR STYLESHEET BASE
		styleSheet = """
			QFrame{
				border-radius: 150px;
				background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(0, 0, 255, 0), stop:{STOP_2} rgba(0, 0, 255, 255));
			}
			"""
		# GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
		# stop works of 1.000 to 0.000
		progress = (100 - value) / 100.0

		# GET NEW VALUES
		stop_1 = str(progress - 0.001)
		stop_2 = str(progress)

		# SET VALUES TO NEW STYLESHEET
		newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
		# APPLY STYLESHEET WITH NEW VALUES
		obj.setStyleSheet(newStylesheet)


	def progressBarValue_TT(self, obj, value, TT):
		value = TT - value
		# print ( value, TT)
		if value >= 0:
			progress = (TT - value ) / TT 
			styleSheet = """
			QFrame{
				border-radius: 130px;
				background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(0,255,0, 255), stop:{STOP_2} rgba(0,255,0, 0));
			}
			"""
		elif abs(value) <= TT:
			progress = abs(value) / TT 
			styleSheet = """
			QFrame{
				border-radius: 130px;
				background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(128,64, 0, 255), stop:{STOP_2} rgba(128,64, 0, 0));
			}
			"""
		else:
			value = abs(value) - TT
			progress = value / TT  if abs(value) <= TT else 1
			styleSheet = """
			QFrame{
				border-radius: 130px;
				background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255,0,0, 255), stop:{STOP_2} rgba(255,0,0, 0));
			}
			"""
		# GET NEW VALUES
		stop_1 = str(progress - 0.001)
		stop_2 = str(progress)

		# SET VALUES TO NEW STYLESHEET
		newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
		# print ( obj, newStylesheet)

		# APPLY STYLESHEET WITH NEW VALUES
		obj.setStyleSheet(newStylesheet)


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
		print ( f"{datetime.now()} - WS received ")
		if not _json : return

		match _json.get('type'):
			case 'broadcast':
				messageContents = _json.get('message')
				if messageContents:
					# 😀 접속 login시 text message 받음
					if isinstance( messageContents, list):
						self.gen_Progress_Body(messageContents)
						# for msgDict in messageContents:
						# 	# print ( type(msgDict), msgDict)
						# 	self.gen_Progress_Frame(msgDict=msgDict)
				else:
					print ( 'ws_message empty!!!:')


#################################################
	def __is_생산Up(self, 운영tt=int):
		return 운영tt <= Info.생산모니터링_Table_생산UpTime

	def get_style_status(self, msg=str):
		style = "background-color:black;color:white;font-weight:400"
		fontColor = 'white'
		bgColor = 'black'
		match msg:
			case '준비':
				bgColor = 'gray'
			case '종료':
				bgColor = 'gray'
			case '휴식':
				bgColor = 'green'
			case '점심':
				bgColor = 'green'
			case '정지':
				bgColor = 'red'
			case '지연':
				bgColor = 'yellow'
				fontColor = 'black'
			case '가동중':
				bgColor = 'blue'                

			case _:
				pass
		style =f'border-radius:10px;border:2px solid {bgColor};background-color:{bgColor};color:{fontColor};font-weight:700;'
		return style

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


