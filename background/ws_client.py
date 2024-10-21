import websocket
import time
# import rel
import threading, json
import utils as Utils

class WS_Client:
    def __init__(self, url:str):
        self.prevMsg = ''
        self.url = url
        self.tryCount = 0
        self.maxRetry =5
        
    def __open__ws(self):
        ws = websocket.WebSocketApp( self.url,
                              on_open = self.on_open,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close)
        
        self.ws = ws
        # self.ws.run_forever( reconnect=5) 
        # self.ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
        # rel.signal(2, rel.abort)  # Keyboard Interrupt
        # rel.dispatch()
    
    def run(self):
        self.__open__ws()
        # self.ws.run_forever()
        self.t = threading.Thread( target = self.ws.run_forever, kwargs=({'reconnect':5}))
        self.t.start()

    def on_message(self, ws, contents):
        # Utils.log_print(msg=f"ws-on message {self.url}:{contents}")
        if self.is_login(contents) and self.prevMsg:
            Utils.log_print(msg=f"ws-login and on message {self.url}:{contents}")
            self.send(self.prevMsg)

    def on_error(self, ws, error):
        Utils.log_print(msg=f"ws-error {self.url}:{error}")
        self.ws.close()
        self.t.join()
        # self.run()

    def on_close(self, ws, close_status_code, close_msg):
        Utils.log_print(msg=f"ws-closed {self.url} :{close_status_code} {close_msg}")
        self.ws.close()
        self.t.join()
        # self.run()

    def on_open(self, ws):
        Utils.log_print(msg=f"ws-opend {self.url} : Opened connection")

    def send(self, msg:str):
        try:
            Utils.log_print(msg=f"ws-send {self.url} : {msg}")
            self.prevMsg = msg
            self.ws.send(msg)
            self.tryCount = 0

        except Exception as e:
            while self.tryCount < self.maxRetry:
                Utils.log_print(msg=f"ws-send {self.url} Exception Error : {e} ")
                Utils.log_print(msg=f"ws-send {self.url} Retry Count (Max Count:{self.maxRetry}) : {self.tryCount+1} ")
                self.ws.close()
                self.t.join()               
                
                try:
                    self.run()
                    self.ws.send(msg)
                except:
                    self.tryCount += 1
                    time.sleep(1)

    def close(self):
        Utils.log_print(msg=f"ws-closing(강제) ")
        self.ws.close()
        self.t.join()

    def is_login(self, contents:str) -> bool:
        contents_dict = json.loads(contents)
        try:
            if contents_dict.get('type') == 'login' :
                return True
            else:
                return False
        except:
            return False



# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/BTCUSD",
#                               on_open=on_open,
#                               on_message=on_message,
#                               on_error=on_error,
#                               on_close=on_close)

#     ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
#     rel.signal(2, rel.abort)  # Keyboard Interrupt
#     rel.dispatch()