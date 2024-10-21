import sys, traceback
from PyQt6 import QtCore, QtGui, QtWidgets, sip
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
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

# import contents Widgets
from modules.Pages.생산모니터링_table import Wid_생산모니터링_Table
from modules.Pages.생산모니터링_circular import Wid_생산모니터링_Circular
from modules.Pages.건조로_카메라 import Wid_건조로_카메라
from modules.Pages.network_diagram import Wid_Network_Status

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.show_count = 2   ###😀 시작 page의 list index -1
        self.prevWid:QtWidgets.QWidget|None = None
        self.curWid:QtWidgets.QWidget|None = None
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        ### init
        self.ws_기상청 = self.__init__WS(url_ws=Info.URL_WS_기상청, slot=self.slot_WS_Message )
        self.__init__API()

        self.init_contents()

        self.timer_1sec = QTimer()
        self.timer_1sec.timeout.connect(self.slot_Timer_1sec)
        self.timer_1sec.start(1000)

        self.is_Analog_Clock_Active = False

        self.timer_1min = QTimer()
        self.timer_1min.timeout.connect(self.slot_Timer_1min)
        self.timer_1min.start(1000*60)

    def init_contents(self) -> dict:
        self.contentsDict = {
            '생산모니터링_table' : """Wid_생산모니터링_Table( 
                                    parent = self, 
                                    async_API=self.async_API, 
                                    apiURL= Info.URL_생산DATA+Info.With_No_Page, 
                                    wsURL= Info.URL_WS_생산모니터링 )""",
            '생산모니터링_progress' : """Wid_생산모니터링_Circular( 
                                    parent = self,
                                    async_API=self.async_API, 
                                    apiURL= Info.URL_생산DATA+Info.With_No_Page, 
                                    wsURL= Info.URL_WS_생산모니터링 )""",
            '건조로_카메라' :""" Wid_건조로_카메라(
                                    parent = self,
                                    async_API=self.async_API, 
                                    apiURL= Info.URL_생산DATA+Info.With_No_Page, 
                                    wsURL= Info.URL_WS_생산모니터링)""",
            'Network_Status' :"""Wid_Network_Status(
                                    parent = self,
                                    async_API=self.async_API, 
                                    apiURL= Info.URL_생산DATA+Info.With_No_Page, 
                                    wsURL= Info.URL_WS_NETWORK_STATUS)"""
            
        }
        self.contentsList = list( self.contentsDict.keys() )

    def run(self):
        if hasattr(self.ui, 'vLayout_contents') : self.deleteLayout(self.ui.vLayout_contents)
        if isinstance(self.curWid, QtWidgets.QWidget):
            self.prevWid = self.curWid
            self.prevWid.close()
        self.ui.vLayout_contents = QtWidgets.QVBoxLayout()
        self.ui.frame_contents.setLayout( self.ui.vLayout_contents )

        key_name = self.get_show_wid() 
        eval_str = self.contentsDict.get( key_name )
        self.curWid = eval(eval_str)
        self.ui.vLayout_contents.addWidget( self.curWid )
        self.ui.label_Title.setText(key_name)

    def closeEvent(self, event:QtCore.QEvent):
        if self.messageBox_with_YesNo():
            print('closeing')
            self.curWid.closeEvent(event)
            event.accept()
        else:
            print('not closeing')
            event.ignore()
    
    def messageBox_with_YesNo(self, title:str="Close !!!", text:str="종료할까요?") -> bool:
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
        return  button == QMessageBox.StandardButton.Yes
           

    def __init__WS(self, url_ws, slot) -> object:
        # self.WS_URL = Info.baseURL_WS +'/broadcast/' + urllib.parse.quote("monitoring") +'/'
        ws = QThs.User_WS_Client(url=url_ws)
        ws.start()
        ws.Message.connect(slot)

    def __init__API(self):
        self.async_API = Async_API_SH()
        self.api_status = self.async_API.Login()
        if not self.api_status:
            print ('login error')
            return
        
        self._update_무재해()

    def _update_무재해(self):
        _res_json = self.async_API.Get(Info.URL_무재해DB+Info.With_No_Page )
        obj = _res_json[0]
        무재해일자 = obj.get('무재해시작')

        delta = date.today() - datetime.strptime(무재해일자, '%Y-%m-%dT%H:%M:%S').date()
        style='font-size:64px;font-weight:700;background-color:green;color:white;'
        self.ui.label_totalDays.setText ( str( delta.days ) + ' 일' )
        self.ui.label_totalDays.setStyleSheet(style)
        self.ui.label_fromDays.setText ( f"({무재해일자.split('T')[0]} ~ )")

        # self.ui.label_img_NoAccident.setPixmap(QtGui.QPixmap('./assets/PyQt/images/무재해.jpg'))
        # self.ui.label_img_NoAccident.setScaledContents(True)

        print(_res_json)

    def _update_weather(self, msg=dict):
        if (fcstTime := msg.get('fcstTime', None)) is None: return
        ptyKey = msg.get('PTY')
        PTY = {
            '0':'강수없음',
            '1':'비',
            '2':'비/눈',
            '3':'눈',
            '5':'빗방물',
            '6':'빗방울눈날림',
            '7':'눈날림'
        }
        self.ui.label_weather_title.setText(f"기상청({fcstTime[0:2]}:00)")
        self.ui.label_weather_temp.setText( f"기온 : {msg.get('T1H')} ℃")
        ptyText = f"{PTY.get(ptyKey)}"+ f"({msg.get('RN1')})" if not ptyKey == '0' else '' 
        self.ui.label_PTY.setText( ptyText )
        if ptyKey == '0':
            path = f"./assets/PyQt/images/{msg.get('LGT')}.png"
        else :
            if ptyKey in ['1','2', '5','6'] :
                path = f'./assets/PyQt/images/5.png'
            else: path = f'./assets/PyQt/images/6.png'
        self.ui.label_weather_img.setPixmap( QtGui.QPixmap(path) )
        self.ui.label_weather_img.setScaledContents(True)


    def resizeEvent(self, event):
        print ("resize :", self.width(), self.height() )
        self.ui.Win_width = self.width()
        self.ui.Win_height = self.height()
        QtWidgets.QMainWindow.resizeEvent(self, event)

###############slot##############################
    @pyqtSlot()
    def slot_Timer_1sec(self):
        # self.ui.frame.hide()
        # self.ui.frame_Table.hide()
        self.render_analog_clock()

    @pyqtSlot()
    def slot_Timer_1min(self):
        self.run()

    @pyqtSlot(object)
    def slot_WS_Message(self, msg:dict):
        print('On Message :', msg)
        if not msg : return 
        # if not msg.get('contents') : return 

        match msg.get('type') :
            case 'login':
                pass
            case 'broadcast':
                self._update_weather(msg=msg.get('message'))
            
            case _:
                pass

    def get_show_wid(self) -> str:
        self.show_count = self.show_count+ 1 if self.show_count <len(self.contentsList )-1 else 0
        return self.contentsList[self.show_count]
    

#################################################

    def render_analog_clock(self):
                # creating hour hand
        self.hPointer = QtGui.QPolygon([QPoint(6, 7),
                                        QPoint(-6, 7),
                                        QPoint(0, -50)])
 
        # creating minute hand
        self.mPointer = QPolygon([QPoint(6, 7),
                                  QPoint(-6, 7),
                                  QPoint(0, -70)])
 
        # creating second hand
        self.sPointer = QPolygon([QPoint(1, 1),
                                  QPoint(-1, 1),
                                  QPoint(0, -90)])
        # colors
        # color for minute and hour hand
        self.bColor = Qt.GlobalColor.green
 
        # color for second hand
        self.sColor = Qt.GlobalColor.red
        self.is_Analog_Clock_Active  = True
        self.update()
 
    # method for paint event
    def paintEvent(self, event):
        
        if not self.is_Analog_Clock_Active : return None
 
        # getting minimum of width and height
        # so that clock remain square
        rec = min(self.ui.frame_Clock.width(), self.ui.frame_Clock.height())
 
        # getting current time
        tik = QTime.currentTime()

        pixmap = QPixmap(self.ui.label_clock.size())
        pixmap.fill(Qt.GlobalColor.transparent)
 
        # creating a painter object
        painter = QPainter(pixmap)
        # painter.begin(self)
 
 
        # method to draw the hands
        # argument : color rotation and which hand should be pointed
        def drawPointer(color, rotation, pointer):
 
            # setting brush
            painter.setBrush(QBrush(color))
 
            # saving painter
            painter.save()
 
            # rotating painter
            painter.rotate(rotation)
 
            # draw the polygon i.e hand
            painter.drawConvexPolygon(pointer)
 
            # restore the painter
            painter.restore()
 
         # tune up painter
        # painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing )
 
        # translating the painter
        x = self.ui.label_clock.x()
        y = self.ui.label_clock.y()
        painter.translate(x+self.ui.frame_Clock.width()/2, y+self.ui.frame_Clock.height()/2)
 
        # scale the painter
        painter.scale(rec / 200, rec / 200)
 
        # set current pen as no pen
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
 
 
        # draw each hand
        drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * tik.second()), self.sPointer)
 
 
        # drawing background
        painter.setPen(QPen(self.bColor))
 
        # for loop
        for i in range(0, 60):
 
            # drawing background lines
            if (i % 5) == 0:
                painter.drawLine(87, 0, 97, 0)
 
            # rotating the painter
            painter.rotate(6)
 
        # ending the painter
        painter.end()

        self.ui.label_clock.setPixmap(pixmap)

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



def main():    
    # update = Update()
    # if update.update_routine():
    #     return 0

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.run()
    window.show()
    app.exec()


if __name__ == "__main__":
    sys.exit( main())