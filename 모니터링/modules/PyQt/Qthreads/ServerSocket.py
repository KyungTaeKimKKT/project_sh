from PyQt6.QtCore import *
import json, numpy, base64, time, datetime
import cv2
import socket
import sounddevice
import pickle

import modules.user.utils as utils


class ServerSocket(QThread):
    timeout = pyqtSignal(object, object) 

    def __init__(self, ip, port):
        super().__init__()
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.sock = None
        self.conn = None
        self.socketOpen()
        self.is_Run = True
        self.FirstHEADER_LEN = 16
        self.socketErrCnt = 0

    def run(self):
        list_소요time = []
        list_bytes = []
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client', self.conn.getpeername())
        while self.is_Run:            
            try:                
                t0 = time.time()
                header_len = str(self.recvall(self.conn, self.FirstHEADER_LEN).decode('utf-8')).strip()
                header = self.recvall(self.conn, int(header_len))
                # print ( '받은:', header )
                header = header.decode('utf-8')
                # print ( 'decode 후:', header )
                headerDict = json.loads(header)
                headerDict['connected_to'] = self.conn.getpeername()[0]
                stringData = self.recvall(self.conn, int(headerDict['length']))
                # print ( len(headerDict), headerDict)
                list_소요time.append(time.time() - t0 )
                list_bytes.append(int(header_len) + len(stringData) )
                if (sum_time := sum(list_소요time) )>= 1 :
                    # utils.pprint ( f"{sum_time}초 {sum(list_bytes)} bytes : {sum(list_bytes)/sum_time} bytes/초 ")
                    list_소요time, list_bytes = [], []                                  

                match str(headerDict['type']).lower() :
                    case 'video':
                        data = pickle.loads(stringData)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(data, headerDict['stime'], (10,50), font, 1.5, (0,255,0), 2, cv2.LINE_AA)
                        self.timeout.emit(headerDict, data )

                        # data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
                        # self.timeout.emit(headerDict, cv2.imdecode(data, 1) )
                    case 'voice':
                        # print ('receive voice : ', headerDict['length'] )
                        self.timeout.emit(headerDict, pickle.loads(stringData) )
                        # self.timeout.emit(headerDict, base64.b64decode(stringData) )
                    
                    case _:
                        pass

            except Exception as e:
                utils.pprint(f'{self.TCP_PORT} socket error:{e} ')
                self.socketErrCnt +=1
                if self.socketErrCnt > 100 :
                    utils.pprint(f'socket close by {self.socketErrCnt} errors')
                    self.close()

                # continue
                # self.socketClose()
                # cv2.destroyAllWindows()
                # self.socketOpen()

    def stop(self):
        self.is_Run = False
        
    def close(self):
        self.stop()
        self.socketClose()

    def restart(self):
        self.is_Run = True

    def socketClose(self):
        # OSError: [Errno 9] 파일 디스크립터가 잘못됨
        # self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        print ( 'socketOpen : ', self.sock)
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')

    
    def tts(self, msg):
        strType = 'tts'
   
        HEADER = {
            'type':strType,
            'format' : 'text', 
            'stime' : datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'tts': msg,
        }

        json_str = json.dumps(HEADER, ensure_ascii=False).encode('utf-8')
        print ( json_str, str(len(json_str)).encode('utf-8').ljust(16))
        self.conn.send (str(len(json_str)).encode('utf-8').ljust(16))
        self.conn.sendall( json_str )

    def ftp_ready(self):
        pass
        
    def ftp(self, fName, file):        
        if self.conn is None:  self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client', self.conn.getpeername())

        stime = time.time()
        strType = 'ftp'
        streamData = file.read()
        if not streamData : 
            utils.pprint('ftp streamData is Empty')
            return
        # streamData = str(data).encode()

        HEADER = {
            'type':strType,
            'fName' : fName, 
            'stime' : datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'fileLength': len(streamData) ,
        }
        json_str = json.dumps(HEADER, ensure_ascii=False).encode('utf-8')
        self.conn.send (str(len(json_str)).encode('utf-8').ljust(16))
        self.conn.sendall( json_str )
        self.conn.sendall( streamData )
    
        print ('전송file:',fName, '  ,전송시간:', time.time() - stime, '  ,전송size: ', len(streamData))
    # def receiveImages(self):

    #     try:
    #         while True:
    #             length = self.recvall(self.conn, 64)
    #             length1 = length.decode('utf-8')
    #             stringData = self.recvall(self.conn, int(length1))
    #             stime = self.recvall(self.conn, 64)
    #             print('send time: ' + stime.decode('utf-8'))
    #             now = time.localtime()
    #             print('receive time: ' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f') )
    #             # print('receive time: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
    #             data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
    #             decimg = cv2.imdecode(data, 1)
    #             self.timeout.emit(decimg)
    #             # cv2.imshow("image", decimg)
    #             # cv2.waitKey(1)
    #     except Exception as e:
    #         print(e)
    #         self.socketClose()
    #         cv2.destroyAllWindows()
    #         self.socketOpen()
    #         self.receiveThread = threading.Thread(target=self.receiveImages)
    #         self.receiveThread.start()
        
    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

