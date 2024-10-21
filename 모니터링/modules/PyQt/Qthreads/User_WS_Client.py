
from PyQt6.QtCore import *
import websocket
import json, datetime, time

import modules.user.utils as Utils


class User_WS_Client(QThread):
    Message = pyqtSignal(object)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.tryCount = 0
        self.maxRetry =5

        self.is_run= True

        self.__open__ws()

    def __open__ws(self):
        ws = websocket.WebSocketApp( self.url,
                              on_open = self.on_open,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close)
        
        self.ws = ws

    def run(self):
        # self.__open__ws()
        
        self.ws.run_forever(reconnect=100)
        # while self.is_run:
        #     pass

        # self.ws.close()
        # self.ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        # rel.signal(2, rel.abort)  # Keyboard Interrupt
        # rel.dispatch()
    
    def close(self):
        self.ws.close()

    def on_open(self, ws):
        open_msg = {
                'type':'login',
                'sender' : Utils.get_IP_Hostname()[0],
                'message':{
                    'to' : 'All',
                    'msg': 'login',
                },
                'send_time' :  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            }
        self.ws.send( json.dumps(open_msg)  )
        self.Message.emit ( open_msg )
        Utils.log_print(msg=f"ws-opend {self.url} : Opened connection")
    
    def on_message(self, ws, msg):
        msg = json.loads(msg)
        Utils.log_print (msg=f'{self.url} On msg: {msg}')

        self.Message.emit(msg)
        # if msg['type'] == 'calling':
        #     self.timeout.emit(msg)

    def send(self, msg):
        try:    
            Utils.log_print(msg=f"ws-send {self.url} : {msg}")
            # self.prevMsg = msg
            self.ws.send(msg)
            self.tryCount = 0

        except Exception as e:
            while self.tryCount < self.maxRetry:
                Utils.log_print(msg=f"ws-send {self.url} Exception Error : {e} ")
                Utils.log_print(msg=f"ws-send {self.url} Retry Count (Max Count:{self.maxRetry}) : {self.tryCount+1} ")
                self.ws.close()
                 
                try:
                    self.run()
                    self.ws.send(msg)
                except:
                    self.tryCount += 1
                    time.sleep(1)        

    def on_error(self, ws, error ):
        Utils.log_print(msg=f"ws-error {self.url}:{error}")
        self.ws.close()
        # try:
        #     self.run() 
        # except:
        #     self.tryCount += 1
        #     time.sleep(1) 
        

    def on_close(self, ws, close_status_code, close_msg):
        Utils.log_print(msg=f"ws-closed {self.url} :{close_status_code} {close_msg}")
        self.ws.close()

