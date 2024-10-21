from PyQt6.QtCore import *

import time, datetime


class Clock(QThread):
    timeout = pyqtSignal(object)    

    def __init__(self):
        super().__init__()
        self.second = 0

    def run(self):
        while True:
            now = datetime.datetime.now()
            if ( self.second != now.second): 
                self.timeout.emit ( now.strftime("%Y-%m-%d %H:%M:%S"))
                self.second = now.second