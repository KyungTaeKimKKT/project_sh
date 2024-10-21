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
from modules.Ui.Ui_main import Ui_MainWindow
# from Ui_main_v4 import Ui_MainWindow_byDesigner
# from Ui_main_circular_bar_v1 import Ui_MainWindow_byDesigner
from modules.user.api import Api_SH
from modules.user.async_api import Async_API_SH
import modules.PyQt.Qthreads as QThs
import modules.user.utils as utils
from analog_clock import Clock
# from .update import Update

from info import Info




# class Ui_MainWindow(Ui_MainWindow_byDesigner ):
#     def __init__(self):
#         self.WS_URL = 'ws://192.168.7.108:9998/'+urllib.parse.quote("생산모니터링")+'/broadcast/'
#         self.ws = QThs.User_WS_Client(self.WS_URL)
#         self.ws.start()
#         self.ws.Message.connect(self.slot_WS_Message)


#         Info.생산모니터링_Tabeself.label_names_list = ['line_no','생산capa', 'start_time', 'end_time', 'plan_qty', 'job_qty', '달성률', '운영가동률','운영tt','status']

#         self.prevMsg = {}
#         self.생산UpTime = 10 ## 10초 미만일때 생산 up

#         self.frame_toggle_flag = False

#         self.progress_obj = {}

#         # self.timer_1min = QTimer()
#         # self.timer_1min.timeout.connect(self.toggle_frame_show)
#         # self.timer_1min.start(60*1000)



#     def render_default(self):
#         self.toggle_frame_show()
#         self.label_img_NoAccident.setScaledContents(True)
#         self.label_weather_img.setScaledContents(True)
#         self.label_clock.setScaledContents(True)

#     def run(self):
#         self.render_default()
#         self.gen_head_frame( ['공정명','생산CAPA', '시작','종료','계획수량','실적수량','달성률','운영가동률','운영TT','상태'])
#         # self.gen_body()
#         # self.clock = Clock(self.label)
#         pass
#         # self.model = TableModel(self.data)
#         # self.tableView.setModel(self.model)

#     def toggle_frame_show(self):
#         if self.frame_toggle_flag :
#             self.frame_Table.show()
#             self.frame_Progress.hide()
#         else:
#             self.frame_Table.hide()
#             self.frame_Progress.show()

#         self.frame_toggle_flag = not self.frame_toggle_flag
	
#     def check_prevMsg(self, msg=dict):
#         if (send_time_str :=msg.get('send_time', None) ) is None: 
#             print ( send_time_str)
#             return False
			
#         if ( prevSendTimeStr:=self.prevMsg.get('send_time', None)) is not None:
#             prevSendTime =  datetime.strptime(prevSendTimeStr,'%Y-%m-%dT%H:%M:%S')
#             print ( 'prevsendtime', prevSendTime)
#             if (send_time :=datetime.strptime(send_time_str,'%Y-%m-%dT%H:%M:%S') ) <= prevSendTime : 
#                 print (  '실행되는 시간', send_time, prevSendTime)
#                 return False
#             else:
#                 print ('true경우: ',  send_time, prevSendTime)
#                 return True
#         return True

#     def gen_body(self, msgList=list):        
			
#         self.gen_무재해( msgList[0].get('무재해'))
#         for msgDict in msgList:
#             self.gen_body(msgDict)
	

#     def gen_head_frame(self, headList=list):
#         self.frame_Head = QtWidgets.QFrame(self.frame_Table)
#         self.frame_Head.setEnabled(True)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(3)
#         sizePolicy.setHeightForWidth(self.frame_Head.sizePolicy().hasHeightForWidth())
#         self.frame_Head.setSizePolicy(sizePolicy)
#         self.frame_Head.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_Head.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_Head.setLineWidth(0)
#         self.frame_Head.setObjectName("frame_Head")
#         self.frame_Head.setStyleSheet('background-color:black;border:5px solid white;')
#         self.horizontalLayout_head_frame = QtWidgets.QHBoxLayout(self.frame_Head)
#         self.horizontalLayout_head_frame.setSpacing(0)
#         self.horizontalLayout_head_frame.setObjectName("horizontalLayout_head_frame")

#         font = QtGui.QFont()
#         font.setPointSize(32)

#         for head in headList:
#             label_name = 'head'+'_'+head
#             setattr (self, label_name, QtWidgets.QLabel(self.frame_Head))
#             label = getattr(self, label_name)
#             label.setFont(font)
#             style = "background-color:black;color:white;font-weight:700;border:1px solid black;"
#             label.setStyleSheet(style)
#             label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#             label.setObjectName(label_name)
#             self.horizontalLayout_head_frame.addWidget(label)
#             label.setText(head)
#         self.verticalLayout.addWidget(self.frame_Head)

#     def gen_무재해(self, 무재해일자=str):
#         delta = date.today() - datetime.strptime(무재해일자, '%Y-%m-%d %H:%M:%S').date()
#         style='font-size:96px;font-weight:700;background-color:green;color:white;'
#         self.label_totalDays.setText ( str( delta.days ) + ' 일' )
#         self.label_totalDays.setStyleSheet(style)
#         self.label_fromDays.setText ( f"({무재해일자.split(' ')[0]} ~ )")

#     def gen_body(self, msgDict=dict):
#         line_no = msgDict.get('line_no')
#         frame_name = f'frame_Body_{line_no}'

#         if getattr(self, frame_name, None) is not None:
#             self.update_body_frame(msgDict)
#             return None

#         setattr(self, frame_name, QtWidgets.QFrame(self.frame_Table))
#         frame = getattr(self, frame_name )

#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(2)
#         sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
#         frame.setSizePolicy(sizePolicy)

#         frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame.setObjectName(frame_name)
#         frame.setStyleSheet('background-color:black;border:1px solid gray;')
		

#         h_layout_name = f'horizontalLayout_{line_no}'
#         setattr(self, h_layout_name , QtWidgets.QHBoxLayout(frame))
#         h_layout = getattr(self, h_layout_name )
#         # layout.setContentsMargins(left, top, right, bottom)
#         h_layout.setContentsMargins(-1, -1, -1, -1)
#         h_layout.setSpacing(0)
#         h_layout.setObjectName(h_layout_name )

#         font = QtGui.QFont()
#         font.setPointSize(24)
		
#         for name in Info.생산모니터링_Tabeself.label_names_list:
#             label_name = line_no+'_'+name
#             setattr (self, label_name, QtWidgets.QLabel(frame))
#             label = getattr(self, label_name)
#             label.setFont(font)
#             # label.setStyleSheet("border:1px solid black;")
#             label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#             label.setObjectName(label_name)
#             h_layout.addWidget(label)
		
#         self.verticalLayout.addWidget(frame)

#         self.update_body_frame(msgDict)

#     def update_body_frame(self, msgDict=dict):
#         line_no = msgDict.get('line_no')
#         is_생산Up = self.__is_생산Up(msgDict.get('운영tt') )
			
#         for name in Info.생산모니터링_Tabeself.label_names_list:
#             label_name = line_no+'_'+name
#             label = getattr(self, label_name)
#             text = str(msgDict.get(name))
#             style = "background-color:black;color:white;font-weight:400;border:none;"
#             if name in ['job_qty', ] :
#                 style = "background-color:black;color:yellow; font-weight:700;border:none" if is_생산Up else style
#                 text =  text + '▲' if is_생산Up else text
#             if name in ['start_time','end_time',] :
#                 text = text.split('T')[1]
#                 text = text.split(':')[0]+':'+text.split(':')[1]
#             if name in ['status',]:
#                 style = self.get_style_status(text)
#             label.setText(text)
#             label.setStyleSheet(style)
	
#     def __is_생산Up(self, 운영tt=int):
#         return 운영tt <= self.생산UpTime
	
#     def get_style_status(self, msg=str):
#         style = "background-color:black;color:white;font-weight:400"
#         fontColor = 'white'
#         bgColor = 'black'
#         match msg:
#             case '준비':
#                 bgColor = 'gray'
#             case '종료':
#                 bgColor = 'gray'
#             case '휴식':
#                 bgColor = 'green'
#             case '점심':
#                 bgColor = 'green'
#             case '정지':
#                 bgColor = 'red'
#             case '지연':
#                 bgColor = 'yellow'
#                 fontColor = 'black'
#             case '가동중':
#                 bgColor = 'blue'                

#             case _:
#                 pass
#         style =f'border-radius:10px;border:2px solid {bgColor};background-color:{bgColor};color:{fontColor};font-weight:700;'
#         return style
	
#     def gen_weather(self, msg=dict):
#         if (fcstTime := msg.get('fcstTime', None)) is None: return
#         ptyKey = msg.get('PTY')
#         PTY = {
#             '0':'강수없음',
#             '1':'비',
#             '2':'비/눈',
#             '3':'눈',
#             '5':'빗방물',
#             '6':'빗방울눈날림',
#             '7':'눈날림'
#         }
#         self.label_weather_title.setText(f"기상청({fcstTime[0:2]}:00)")
#         self.label_weather_temp.setText( f"기온 : {msg.get('T1H')} ℃")
#         self.label_PTY.setText(f"{PTY.get(ptyKey)}")
#         if ptyKey == '0':
#             path = f"./assets/PyQt6/images/{msg.get('LGT')}.png"
#         else :
#             if ptyKey in ['1','2', '5','6'] :
#                 path = f'./assets/PyQt6/images/5.png'
#             else: path = f'./assets/PyQt6/images/6.png'
#         self.label_weather_img.setPixmap( QtGui.QPixmap(path) )
#         self.label_weather_img.setScaledContents(True)


#     def gen_Progress_Body(self, msgList=list):
#         for msgDict in msgList:
#             match msgDict.get('line_no'):
#                 case 'MAIN1':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
#                 case 'MAIN2':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
#                 case 'MAIN3':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base, msgDict=msgDict)
#                 case 'M/T-1':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
#                 case 'M/T-2':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
#                 case 'INK-PRT':
#                     self.gen_Progress_Frame(parentObj=self.frame_HI_Base_2, msgDict=msgDict)
#                 case 'P4-LEAN':
#                     self.gen_Progress_Frame(parentObj=self.frame_PO1, msgDict=msgDict)
#                 case 'RIOR':
#                     self.gen_Progress_Frame(parentObj=self.frame_PO1, msgDict=msgDict)
#                 case 'UHC':
#                     self.gen_Progress_Frame(parentObj=self.frame_PO2, msgDict=msgDict)
#                 case '폴리401':
#                     self.gen_Progress_Frame(parentObj=self.frame_PO2, msgDict=msgDict)
#                 case _:
#                     pass



#     def gen_Progress_Frame(self, parentObj, msgDict=dict):
#         line_no = msgDict.get('line_no')
#         w_frame = int(300*self.Win_width / 1749)
#         x_start = 0 + int( (w_frame -300) / 2 )
#         # print ('resize: ', w_frame, x_start)
#         if ( x_start > 0 ):
#             self.progress_obj[line_no]['prod'].setGeometry(QtCore.QRect(x_start, 0, 300, 300))
#             self.progress_obj[line_no]['tt'].setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
#             # self.progress_obj[line_no]['label_lineNo'].setGeometry(QtCore.QRect(x_start+20, 50, 181, 41))
#             # self.progress_obj[line_no]['label_prodQty'].setGeometry(QtCore.QRect( x_start+30, 130, 161, 61))
#             self.progress_obj[line_no]['prod_bg'].setGeometry(QtCore.QRect(x_start, 0, 300, 300))
#             self.progress_obj[line_no]['tt_bg'].setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
#             self.progress_obj[line_no]['container'].setGeometry(QtCore.QRect(x_start+40, 40, 220, 220))

#         def render_생산up(obj,is_up=False):
#             if is_up:
#                 obj.setStyleSheet("QFrame{\n"
#                                 "    border-radius: 110px;    \n"
#                                 "    background-color: yellow;\n"
#                                 "}")
#             else:
#                 obj.setStyleSheet("QFrame{\n"
#                                 "    border-radius: 110px;    \n"
#                                 "    background-color: rgb(58, 58, 102);\n"
#                                 "}")

#         def render_status_by_(obj,msgList=list):
#             text = obj.text()
#             if ( msgList[0] == text ):
#                 obj.setText(msgList[1])
#             else:
#                 obj.setText(msgList[0])

#         frame_name = f'circularProgressBar_{line_no}'

#         frame_TT_Prog_Name = f'circular_TT_Progress_{line_no}'
#         if getattr(self, frame_name, None) is not None:
#             job_qty = msgDict.get('job_qty')
#             plan_qty = msgDict.get('plan_qty')
#             운영tt = msgDict.get('운영tt')
#             TT = msgDict.get('TT')
#             status = msgDict.get('status')

#             if job_qty>0 and plan_qty>0 and 운영tt <= 10 :
#                 render_생산up( self.progress_obj[line_no]['container'], True )
#                 self.progress_obj[line_no]['label_lineNo'].setStyleSheet('color:black;font-weight:bold')
#                 self.progress_obj[line_no]['label_prodQty'].setStyleSheet('color:black;font-weight:bold')
#             else : 
#                 render_생산up( self.progress_obj[line_no]['container'], False )
#                 self.progress_obj[line_no]['label_lineNo'].setStyleSheet('color:white')
#                 self.progress_obj[line_no]['label_prodQty'].setStyleSheet('color:white')


#             self.progress_obj[line_no]['label_lineNo'].setText(line_no)

#             self.progressBarValue_Qty(obj=self.progress_obj[line_no]['prod'], value= job_qty/plan_qty*100 if plan_qty>0 else 0)
#             self.progressBarValue_TT(obj=self.progress_obj[line_no]['tt'], value=운영tt, TT= TT) #msgDict.get('TT'))

#             if status in ['휴식', '점심', '청소_저녁']:
#                 if ( getattr(self, f'timer_status_{line_no}', None)) is not None:
#                     pass
#                 else :
#                     setattr(self, f'timer_status_{line_no}', QTimer())
#                     status_timer = getattr(self,  f'timer_status_{line_no}')
#                     status_timer.timeout.connect( lambda:render_status_by_(obj=self.progress_obj[line_no]['label_prodQty'], msgList=[str(job_qty) +'/' + str(plan_qty), status]) )
#                     status_timer.start(10*1000)
#             else:
#                 self.progress_obj[line_no]['label_prodQty'].setText(str(job_qty) +'/' + str(plan_qty))
#                 if ( status_timer:=getattr(self, f'timer_status_{line_no}', None)) is not None:
#                     status_timer.stop()

#             return None

#         setattr(self, frame_name, QtWidgets.QFrame(parentObj))
#         frame = getattr(self, frame_name )
#         frame.setStyleSheet("background-color: none;")
#         frame.setFrameShape(QtWidgets.QFrame.NoFrame)
#         frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame.setObjectName(frame_name)


#         ### PRODUCT PROGRESS
#         frame_Prod_Prog_Name = f'circular_Production_Progress_{line_no}'
#         setattr(self, frame_Prod_Prog_Name, QtWidgets.QFrame(frame))
#         frame_production_progress = getattr(self, frame_Prod_Prog_Name )

#         # frame_production_progress.setGeometry(QtCore.QRect(0, 0, 300, 300))
#         frame_production_progress.setGeometry(QtCore.QRect(x_start, 0, 300, 300))
#         styleSheet = """
#             QFrame{
#                 border-radius: 150px;
#                 background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.957 rgba(0, 0, 255, 255), stop:0.956 rgba(0, 0, 255, 0));
#                 }
		
#         """

#         frame_production_progress.setStyleSheet(styleSheet)
#         frame_production_progress.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame_production_progress.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame_production_progress.setObjectName(frame_Prod_Prog_Name)


#         frame_Prod_Bg_Name = f'circular_Production_Progress_{line_no}'
#         setattr(self, frame_Prod_Bg_Name, QtWidgets.QFrame(frame))
#         frame_production_bg = getattr(self, frame_Prod_Bg_Name )

#         frame_production_bg.setGeometry(QtCore.QRect(x_start, 0, 300, 300))
#         frame_production_bg.setStyleSheet("QFrame{\n"
#                                         "    border-radius: 150px;    \n"
#                                         "    background-color: rgba(85, 85, 127, 100);\n"
#                                         "}")
#         frame_production_bg.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame_production_bg.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame_production_bg.setObjectName(frame_Prod_Bg_Name)

#         ##circularContainer
#         frame_Circular_Container_Name = f'circular_container_{line_no}'
#         setattr(self, frame_Circular_Container_Name, QtWidgets.QFrame(frame))
#         frame_Circular_Container = getattr(self, frame_Circular_Container_Name )


#         frame_Circular_Container.setGeometry(QtCore.QRect(x_start+40, 40, 220, 220))
#         frame_Circular_Container.setBaseSize(QtCore.QSize(0, 0))
#         frame_Circular_Container.setStyleSheet("QFrame{\n"
#                                         "    border-radius: 110px;    \n"
#                                         "    background-color: rgb(58, 58, 102);\n"
#                                         "}")
#         frame_Circular_Container.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame_Circular_Container.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame_Circular_Container.setObjectName("frame_Circular_Container_Name")

#         ### label LineNo
#         label_lineNo_name = f'label_LineNo_{line_no}'
#         setattr(self, label_lineNo_name, QtWidgets.QLabel(frame_Circular_Container))
#         label_lineNo = getattr(self, label_lineNo_name )

#         label_lineNo.setGeometry(QtCore.QRect(x_start+20, 50, 181, 41))
#         font = QtGui.QFont()
#         font.setPointSize(32)
#         label_lineNo.setFont(font)
#         label_lineNo.setStyleSheet("color:white")
#         label_lineNo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         label_lineNo.setObjectName(label_lineNo_name)

#         ### label 생산수량
#         label_prodQty_name = f'label_prodQty_{line_no}'
#         setattr(self, label_prodQty_name, QtWidgets.QLabel(frame_Circular_Container))
#         label_prodQty = getattr(self, label_prodQty_name )
#         label_prodQty.setGeometry(QtCore.QRect( x_start+30, 130, 161, 61))
#         font = QtGui.QFont()
#         font.setPointSize(32)
#         label_prodQty.setFont(font)
#         label_prodQty.setStyleSheet("color:white")
#         label_prodQty.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
#         label_prodQty.setObjectName(label_prodQty_name)

#         ### TT PROGRESS
#         frame_TT_Prog_Name = f'circular_TT_Progress_{line_no}'
#         setattr(self, frame_TT_Prog_Name, QtWidgets.QFrame(frame))
#         frame_TT_progress = getattr(self, frame_TT_Prog_Name )
#         frame_TT_progress.setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
#         frame_TT_progress.setStyleSheet("QFrame{\n"
#                                             "    border-radius: 130px;    \n"
#                                             "    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.49 rgba(255, 0, 0, 0), stop:0.5 rgba(255, 0, 0, 255));\n"
#                                             "}")
#         frame_TT_progress.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame_TT_progress.setFrameShadow(QtWidgets.QFrame.Raised)
#         # frame_TT_progress.setObjectName(frame_TT_Prog_Name)

#         ### TT BG
#         frame_TT_Bg_Name = f'circular_TT_Progress_{line_no}'
#         setattr(self, frame_TT_Bg_Name, QtWidgets.QFrame(frame))
#         frame_TT_Bg = getattr(self, frame_TT_Bg_Name )



#         frame_TT_Bg = QtWidgets.QFrame(frame)
#         frame_TT_Bg.setGeometry(QtCore.QRect(x_start+20, 20, 260, 260))
#         frame_TT_Bg.setStyleSheet("QFrame{\n"
#                                         "    border-radius: 130px;    \n"
#                                         "    background-color: rgb(225,225,225);\n"
#                                         "}")
#         frame_TT_Bg.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         frame_TT_Bg.setFrameShadow(QtWidgets.QFrame.Raised)
#         frame_TT_Bg.setObjectName("circular_TT_Bg")
#         frame_production_progress.raise_()
#         frame_TT_Bg.raise_()
#         frame_production_bg.raise_()
#         frame_TT_progress.raise_()
#         frame_Circular_Container.raise_()

#         if line_no in ['MAIN1', 'MAIN2', 'MAIN3']:
#             self.h_layout_frame_HI_BASE.addWidget(frame)
#         elif line_no in ['M/T-1','M/T-2','INK-PRT']:
#             self.h_layout_frame_HI_BASE_2.addWidget(frame)
#         elif line_no in ['P4-LEAN', 'RIOR']:
#             self.h_layout_frame_PO1.addWidget(frame)
#         else:
#             self.h_layout_frame_PO2.addWidget(frame)

#         self.progress_obj[line_no] ={
#             'prod':frame_production_progress,
#             'tt':frame_TT_progress,
#             'label_lineNo':label_lineNo,
#             'label_prodQty':label_prodQty,
#             'container':frame_Circular_Container,
#             'prod_bg':frame_production_bg,
#             'tt_bg':frame_TT_Bg,
#         }


#     def progressBarValue_Qty(self, obj, value):
#         # PROGRESSBAR STYLESHEET BASE
#         styleSheet = """
#             QFrame{
#                 border-radius: 150px;
#                 background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(0, 0, 255, 0), stop:{STOP_2} rgba(0, 0, 255, 255));
#             }
#             """
#         # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
#         # stop works of 1.000 to 0.000
#         progress = (100 - value) / 100.0

#         # GET NEW VALUES
#         stop_1 = str(progress - 0.001)
#         stop_2 = str(progress)

#         # SET VALUES TO NEW STYLESHEET
#         newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
#         # APPLY STYLESHEET WITH NEW VALUES
#         obj.setStyleSheet(newStylesheet)


#     def progressBarValue_TT(self, obj, value, TT):
#         value = TT - value
#         # print ( value, TT)
#         if value >= 0:
#             progress = (TT - value ) / TT 
#             styleSheet = """
#             QFrame{
#                 border-radius: 130px;
#                 background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(0,255,0, 255), stop:{STOP_2} rgba(0,255,0, 0));
#             }
#             """
#         elif abs(value) <= TT:
#             progress = abs(value) / TT 
#             styleSheet = """
#             QFrame{
#                 border-radius: 130px;
#                 background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(128,64, 0, 255), stop:{STOP_2} rgba(128,64, 0, 0));
#             }
#             """
#         else:
#             value = abs(value) - TT
#             progress = value / TT  if abs(value) <= TT else 1
#             styleSheet = """
#             QFrame{
#                 border-radius: 130px;
#                 background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255,0,0, 255), stop:{STOP_2} rgba(255,0,0, 0));
#             }
#             """
#         # GET NEW VALUES
#         stop_1 = str(progress - 0.001)
#         stop_2 = str(progress)

#         # SET VALUES TO NEW STYLESHEET
#         newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
#         # print ( obj, newStylesheet)

#         # APPLY STYLESHEET WITH NEW VALUES
#         obj.setStyleSheet(newStylesheet)


 


#     #### slots #######################
#     def slot_WS_Message(self, msg=dict):
#         data = msg.get('data')

#         match (msgType:=msg.get('type', None)):
#             case 'production':       
#                 if not self.check_prevMsg(msg): return None
#                 self.prevMsg = msg       
#                 self.gen_body(data )
#                 self.gen_Progress_Body(data)

#             case 'weather':
#                 self.gen_weather(data)

#                 # self.gen_body(self, msg)
#             # case 'login_client':
#             #     from_list = msg.get('data',{}).get('from',[])
#             #     if not len(from_list) : return
#             #     text = f"{from_list[0]} is Ready!!!"
#             #     self.label_Ready_Client_0.setText( text )
#             # case 'calling':
#             #     self.show_popup('긴급호출', msg)

#             case _:
#                 print ('message type is unknown:', msgType)
#                 pass

#     def slot_Timer_1sec(self):
#         pass


#     ##################################


#     def __get_생산모니터링FromServer(self):
#         self.api = Api_SH()
#         try:
#             self.생산게획 = self.api.getlist(self.생산계획실적URL+f"?page_size=0")

#         except Exception as e:
#             utils.print_Traceback(traceback.format_exc(), sys.exc_info()[2], e )
#         utils.pprint (self.생산게획 )

class Wid_생산모니터링_Table (QtWidgets.QWidget ):
	def __init__(self, parent, async_API:object, apiURL:str='', wsURL:str=''):        
		super().__init__(parent)    
		self.parent = parent    
		self.async_API = async_API
		self.async_API : Async_API_SH
		self.apiURL = apiURL
		self.wsURL = wsURL        

		self.is_first = True

		self.UI()
		
		### init
		self.__init__WS(self.wsURL)
		self.__init__API()

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

	def UI(self) -> None:
		""" init, render  UI"""
		if hasattr(self, 'vlayout') : self.deleteLayout(self.vlayout)

		self.vlayout = QtWidgets.QVBoxLayout()
		self.vlayout.setContentsMargins( 0,0,0,0)
		self.vlayout.setSpacing(1)
		self.setLayout(self.vlayout)

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

	def gen_table(self, msgList:list) -> None:
		self.gen_table_head()
		for msgDict in msgList:
			self.gen_table_body(msgDict=msgDict)

	def gen_table_head(self) :

		frame_name = f'frame_header'

		setattr(self, frame_name, QtWidgets.QFrame(self))
		frame = getattr(self, frame_name )
		frame : QtWidgets.QFrame

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(2)
		sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
		frame.setSizePolicy(sizePolicy)

		frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame.setObjectName(frame_name)
		frame.setStyleSheet('background-color:black;border:1px solid gray;')
		

		h_layout_name = f'hLayout_header'
		setattr(self, h_layout_name , QtWidgets.QHBoxLayout(frame))        
		h_layout = getattr(self, h_layout_name )
		h_layout : QtWidgets.QHBoxLayout
		# layout.setContentsMargins(left, top, right, bottom)
		h_layout.setContentsMargins(-1, -1, -1, -1)
		h_layout.setSpacing(0)
		h_layout.setObjectName(h_layout_name )

		font = QtGui.QFont()
		font.setPointSize(32)
		font.setBold(True)
		
		for (name,displayName) in zip(Info.생산모니터링_TABLE_HEADERS, Info.생산모니터링_TABLE_HEADERS_Display):
			label_name = 'header_'+name
			setattr (self, label_name, QtWidgets.QLabel(frame))
			label = getattr(self, label_name)
			label : QtWidgets.QLabel
			label.setFont(font)
			# label.setStyleSheet("border:1px solid black;")
			label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			label.setObjectName(label_name)

			style = "background-color:black;color:white;border:none;"
			label.setStyleSheet(style)
			label.setText(displayName)
			h_layout.addWidget(label)
		
		self.vlayout.addWidget(frame)

	def gen_table_body(self, msgDict:dict):
		""" TABLE BODY """
		line_no = msgDict.get('line_no')
		frame_name = f'frame_Body_{line_no}'

		if getattr(self, frame_name, None) is not None:
			self.update_body_frame(msgDict)
			return None

		setattr(self, frame_name, QtWidgets.QFrame(self))
		frame = getattr(self, frame_name )
		frame : QtWidgets.QFrame

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(2)
		sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
		frame.setSizePolicy(sizePolicy)

		frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
		frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
		frame.setObjectName(frame_name)
		frame.setStyleSheet('background-color:black;border:1px solid gray;')
		

		h_layout_name = f'hLayout_{line_no}'
		setattr(self, h_layout_name , QtWidgets.QHBoxLayout(frame))        
		h_layout = getattr(self, h_layout_name )
		h_layout : QtWidgets.QHBoxLayout
		# layout.setContentsMargins(left, top, right, bottom)
		h_layout.setContentsMargins(-1, -1, -1, -1)
		h_layout.setSpacing(0)
		h_layout.setObjectName(h_layout_name )

		font = QtGui.QFont()
		font.setPointSize(24)
		
		for name in Info.생산모니터링_TABLE_HEADERS:
			label_name = line_no+'_'+name
			setattr (self, label_name, QtWidgets.QLabel(frame))
			label = getattr(self, label_name)
			label : QtWidgets.QLabel
			label.setFont(font)
			# label.setStyleSheet("border:1px solid black;")
			label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			label.setObjectName(label_name)

			h_layout.addWidget(label)
		
		self.vlayout.addWidget(frame)

		self.update_body_frame(msgDict)

	def update_body_frame(self, msgDict=dict):
		if not isinstance(msgDict, dict): return 
		# print ( 'update body frame: ', type(msgDict))
		line_no = msgDict.get('line_no')
		is_생산Up = self.__is_생산Up(msgDict.get('운영tt') )
			
		for name in Info.생산모니터링_TABLE_HEADERS :
			label_name = line_no+'_'+name
			label = getattr(self, label_name)
			label : QtWidgets.QLabel
			text = str(msgDict.get(name))
			style = "background-color:black;color:white;font-weight:400;border:none;"
			if name in ['job_qty', ] :
				style = "background-color:black;color:yellow; font-weight:700;border:none" if is_생산Up else style
				text =  text + '▲' if is_생산Up else text
			if name in ['start_time','end_time',] :
				text = text.split('T')[1]
				text = text.split(':')[0]+':'+text.split(':')[1]
			if name in ['status',]:
				style = self.get_style_status(text)
			label.setText(text)
			label.setStyleSheet(style)


###############slot##############################
	@pyqtSlot()
	def slot_Timer_1sec(self):
		pass
		# _json = self.async_API.Get(self.apiURL )
		# # print ( _json )
		# if _json:
		# 	for msgDict in _json:
		# 		self.update_body_frame(msgDict=msgDict)
		# else:
		# 	print ( 'fetch error:')

   
	@pyqtSlot(dict)
	def slot_WS_Message(self, _json:dict):
		if not _json : return

		match _json.get('type'):
			case 'broadcast':
				messageContents = _json.get('message')
				if messageContents:
					if self.is_first:
						self.prev_Contents = self.getPrevContents(messageContents)
						self.is_first = False
						
					# 😀 접속 login시 text message 받음
					if isinstance( messageContents, list):
						for msgDict in messageContents:
							if not self.check_same(msgDict=msgDict):
								self.prev_Contents = self.getPrevContents(messageContents)
								print ( '생산up:', msgDict)
							self.update_body_frame(msgDict=msgDict)

				else:
					print ( 'ws_message empty!!!:')


#################################################
	def _check_생산up(self, msg:list) -> bool:
		pass

	def check_same(self, msgDict:dict) -> bool:
		key = 'line_no'
		finded_prev_obj = [ obj for obj in self.prev_Contents if obj.get(key) == msgDict.get(key)][0]
	
		if finded_prev_obj:
			# if msgDict.get(key) == 'MAIN1':
			# 	print ( finded_prev_obj)
			# 	print ( msgDict)
			# 	print ( '\n', finded_prev_obj.items() <= msgDict.items(), '\n')

			return finded_prev_obj.items() <= msgDict.items()
		else:
			return False

		
	def getPrevContents(self, messageContents:list) -> list:
		result = []
		for obj in messageContents:
			result.append( {key:obj.get(key) for key in ['line_no','start_time','end_time', 'plan_qty', 'job_qty']})
		return result

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


