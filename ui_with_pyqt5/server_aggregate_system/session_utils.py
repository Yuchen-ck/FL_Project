from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time


closeAppTimeMin = 30 #設定session time 為 100秒
closeAppTime = closeAppTimeMin*60

class WorkerThread(QThread):
    trigger = pyqtSignal(str)
    finished = pyqtSignal()

    deadLine = closeAppTime
    isRunning  = True
    def __init__(self,):
        super().__init__()

    def run(self):
        while self.deadLine>=0 and self.isRunning:
            time.sleep(1)
            self.trigger.emit(str(self.deadLine))
            self.deadLine = self.deadLine - 1
            
        #send signal to windows
        self.finished.emit()