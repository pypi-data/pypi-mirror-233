
import time
import numpy as np

from serial import Serial, SerialException
from serial.tools.list_ports import comports

from PyQt5.QtCore import QThread, pyqtSignal

def scan_serial_ports():
    ports = comports()
    return [p.device for p in ports]

MAX_CHANNEL = 16
SAMPLE_RANGE = 100

EXCEPT_SERIAL_EXIT = 0x01

class SamplingThread(QThread):
    samplingSignal = pyqtSignal(object)
    errorSignal = pyqtSignal(int)
    
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._parent.changeCurveSignal.connect(self.onSignalChangeCurve)
        self._serial = Serial(timeout=0)
        self._channelLen = 0
    
    def onSignalChangeCurve(self, index, state):
        self._curveList[index] = state

    def reset(self):
        self._samples = np.array([[0.0] * SAMPLE_RANGE for _ in range(self._channelLen + 1)])
        self._startTime = time.time()
        
    def stop(self):
        self._isRun = False
        while not self.isFinished:
            pass
        self._serial.close()
        
    def openSerial(self, port, baud):
        self._serial.port = port
        self._serial.baudrate = baud

        try:
            self._serial.open()
            self._serial.reset_input_buffer()
        except SerialException as e:
            return False

        return True

    def getChannelLen(self):
        _, tdata = self._read(bytearray())
        if not tdata:
            return 0

        data, tdata = self._read(tdata)
        data = data.decode().rstrip().replace(',', ' ').split()
        
        channelLen = len(data)
        self._channelLen = MAX_CHANNEL if channelLen > MAX_CHANNEL else  channelLen
                    
        return self._channelLen
    
    def run(self):       
        self._curveList = [True] * self._channelLen
        self._isRun = True
        tdata = self.reset()
        
        _, tdata = self._read(bytearray())
        
        while self._isRun: 
            try:
                data, tdata = self._read(tdata)
                pdata = [time.time() - self._startTime]
                pdata += [float(d) if self._curveList[i] else float(0) for i, d in enumerate(data.decode().rstrip().replace(',', ' ').split())]
            except (SerialException, AttributeError):
                self.errorSignal.emit(EXCEPT_SERIAL_EXIT)
                break 
            except ValueError:
                continue
                        
            self._samples[:, -1:] = np.array(pdata).reshape(self._channelLen + 1, 1)                    
            self.samplingSignal.emit(self._samples)
            self._samples = np.roll(self._samples, -1, 1)
            
            self.usleep(10)
            
    def _read(self, tdata):        
        pos = -1
        wait = 300

        while pos == -1:
            while not self._serial.in_waiting and wait > 0:
                self.usleep(1)
                wait -= 1
            
            if wait <= 0:
                return None, None

            tdata += bytearray(self._serial.read(self._serial.inWaiting()))            
            pos = tdata.find(b'\n')

        return tdata[:pos], tdata[pos+1:]
