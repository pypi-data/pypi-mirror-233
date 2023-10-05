import csv

from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPoint
from PyQt5.QtGui import QPen, QColor, QPalette, QBrush, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGroupBox, QComboBox, QPushButton, QSpinBox
from PyQt5.QtWidgets import QLabel, QRadioButton, QCheckBox, QLineEdit 
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
import qwt

from xnode.sampling import SamplingThread
from xnode.sampling import scan_serial_ports
from xnode.sampling import MAX_CHANNEL, SAMPLE_RANGE
from xnode.sampling import EXCEPT_SERIAL_EXIT

PLOT_X_INIT_MAX = 8

class SensorMonotor(QMainWindow):
    changeCurveSignal = pyqtSignal(int, bool)
    
    def __init__(self):
        super().__init__()
 
        self.samplingThread = SamplingThread(self)
        
        self.samplingThread.samplingSignal.connect(self.onSignalPlot)
        self.samplingThread.errorSignal.connect(self.onSignalError)
        
        self.portCheckTimer = QTimer()
        self.portCheckTimer.setInterval(1500)
        self.portCheckTimer.timeout.connect(self.onPortListTimer)
        self.portCheckTimer.start()
        
        self.portList = None
        self.isWait = True
        
        self.initGUI()
          
    def closeEvent(self, event):
        self.samplingThread.isRun = False
        self.samplingThread.terminate()

    def resizeTable(self):
        header = self.tbDatas.horizontalHeader()
        wfactor = self.tbDatas.width() // header.count() - 1

        for column in range(header.count()):
            header.resizeSection(column, wfactor)

    def resizeEvent(self, event):  
        self.resizeTable()
                
    def onAbout(self):
        QMessageBox.information(self, "Sensor Monitor", "© 2020 PlanX-Labs. All rights reserved.\n\nVersion: 1.0.0\nPyQt6: 5.15.2\nnumpy: 1.19.3\npyserial: 3.4") 

    def onReset(self):
        self.samplingThread.reset()
        
        for i in range(self.channelLen): 
            self.curves[i].setSamples([0], [0])
        
        self.bodyInner.removeWidget(self.tbDatas)
        del self.tbDatas
        self.initTable()

        self.btSaveData.setEnabled(False)
        
    def onStopStart(self):        
        if self.btStopStart.text() == "Stop":
            self.btStopStart.setText("Start")
            self.isWait = True
            if self.tbDatas.rowCount():
                self.btSaveData.setEnabled(True)
        else:
            self.btStopStart.setText("Stop")
            self.isWait = False
            self.btSaveData.setEnabled(False)
            
    def onPortListTimer(self):
        portList = scan_serial_ports()
        portList.sort()
        
        if self.portList != portList:   
            self.portList = portList
            
            self.cbPortList.clear()
                   
            for name in self.portList:
                self.cbPortList.addItem(name)
    
    def onDisconnect(self):       
        self.isWait = True       
        self.samplingThread.stop()

        for i in range(self.channelLen):
            self.chCurves[i].setChecked(False)
            self.chCurves[i].setEnabled(False)
        
        self.chCurvesSelect.setCheckState(Qt.Unchecked)
        self.chCurvesSelect.setEnabled(False)
        self.iRawCurves = 0
            
        self.btConnect.setEnabled(True)
        self.btDisconnect.setEnabled(False)
        self.btReset.setEnabled(False)
        self.btStopStart.setEnabled(False)
        self.btStopStart.setText("Stop")
                
        self.cbPortList.setEnabled(True)
        self.cbPortBaud.setEnabled(True)
        
        if self.tbDatas.rowCount():
            self.btSaveData.setEnabled(True)

        if not self.portCheckTimer.isActive():
            self.portCheckTimer.start()
        
        self.sbText.setText('Idle')
                
    def onConnect(self):           
        if not self.samplingThread.openSerial(self.cbPortList.currentText(), int(self.cbPortBaud.currentText())):
            QMessageBox.critical(self, "Serial Monitor", "Can not open serial port!")
            return
        
        self.channelLen = self.samplingThread.getChannelLen()
        if not self.channelLen:
            QMessageBox.critical(self, "Serial Monitor", "Invalied data!")
            self.samplingThread.stop()
            return
        
        self.samplingThread.start()        

        for i in range(self.channelLen):
            self.chCurves[i].setChecked(True)
            self.chCurves[i].setEnabled(True)
        
        self.chCurvesSelect.setEnabled(True)
        self.chCurvesSelect.setCheckState(Qt.Checked)
        self.iRawCurves = 2 ** self.channelLen - 1
                                   
        self.btConnect.setEnabled(False)
        self.btDisconnect.setEnabled(True)
        self.btReset.setEnabled(True)
        self.btStopStart.setEnabled(True)
        
        self.cbPortList.setEnabled(False)
        self.cbPortBaud.setEnabled(False)
        self.btSaveData.setEnabled(False)
        
        self.plot.setAxisScale(qwt.QwtPlot.xBottom, 0, PLOT_X_INIT_MAX, 0.5)
        for i in range(self.channelLen):
            self.curves[i].setPen(self.pens[i])
            self.curves[i].setSamples([0], [0])
                           
        self.bodyInner.removeWidget(self.tbDatas)
        del self.tbDatas
        self.initTable()

        self.sbText.setText('Running')

        if self.portCheckTimer.isActive():
            self.portCheckTimer.stop()
        
        self.isWait = False

    def onSignalError(self, err):
        self.onPortListTimer()
        
        if err == EXCEPT_SERIAL_EXIT:
            if not self.btConnect.isEnabled():
                QMessageBox.critical(self, "Serial Monitor", "Disable serial port")

        self.onDisconnect()
            
    def setTwItem(self, row, column, data):
        item = QTableWidgetItem(str(data))
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor(90,90,90))
        item.setBackground(QColor(250,250,250))
        
        self.tbDatas.setItem(row, column, item)
    
    def setTableData(self, t, data):               
        row = self.tbDatas.rowCount()
        self.tbDatas.insertRow(row)
        
        self.setTwItem(row, 0, t)        
        for i in range(self.channelLen): 
            self.setTwItem(row, i+1, data[i])
            
        self.tbDatas.selectRow(row)
            
    def onSignalPlot(self, samples):
        if self.isWait: return

        x_time = samples[0:1, :].reshape(SAMPLE_RANGE)
        y_data = samples[1:, :]
        
        for i in range(self.channelLen): 
            self.curves[i].setData(qwt.QwtPointArrayData(x_time, y_data[i], len(x_time), True))

        self.plot.setAxisScale(qwt.QwtPlot.xBottom, x_time[0], max(PLOT_X_INIT_MAX, x_time[-1]), 0.5)
        self.plot.replot()
        
        self.setTableData(x_time[-1], y_data[:, -1:].reshape(self.channelLen))
        
    def onChCurve(self, index):
        stat = (self.chCurves[index].checkState() == Qt.Checked)
        
        if stat:
            self.curves[index].setPen(self.pens[index])
            self.iRawCurves |= 1 << index
        else:
            self.curves[index].setPen(QPen(Qt.darkGray, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            self.iRawCurves &= ~(1 << index)

        if self.iRawCurves == 0:
            self.chCurvesSelect.setCheckState(Qt.Unchecked)
        elif self.iRawCurves == 2 ** self.channelLen  - 1:
            self.chCurvesSelect.setCheckState(Qt.Checked)
        else:
            self.chCurvesSelect.setCheckState(Qt.PartiallyChecked)

        self.changeCurveSignal.emit(index, stat)

    def onChCurveSelect(self, _):
        stat = self.chCurvesSelect.checkState()
       
        if stat == Qt.PartiallyChecked:
            self.chCurvesSelect.setCheckState(Qt.Checked)
            
        for i in range(self.channelLen):
            self.chCurves[i].setChecked(stat)
            self.onChCurve(i)
        
    def onRbAuto(self):
        self.leMin.setEnabled(False)
        self.leMax.setEnabled(False)
        self.btManualOk.setEnabled(False)
        
        self.plot.setAxisAutoScale(qwt.QwtPlot.yLeft)
                
    def onRbManual(self):
        self.leMin.setEnabled(True)
        self.leMax.setEnabled(True)
        self.btManualOk.setEnabled(True)
        
    def onBtManualOk(self):
        try:
            min = float(self.leMin.text())
            max = float(self.leMax.text())
        except ValueError:
            return
        
        self.plot.setAxisScale(qwt.QwtPlot.yLeft, min, max)
    
    def onCurveStyle(self):
        for i in range(self.channelLen):
            self.curves[i].setStyle(self.cbCurveStyle.currentIndex())
                
    def onPlotBgColor(self):
        self.plot.setCanvasBackground(self.plotBgColors[self.cbPlotBgColor.currentText()])
    
    def onCurveWidth(self):
        w = int(self.cbCurveWidth.currentText())
        self.pens = [QPen(c, w, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin) for c in self.colors]
        
        for i in range(self.channelLen):
            if self.chCurves[i].checkState():
                self.curves[i].setPen(self.pens[i])
    
    def onSaveData(self):
        fname = QFileDialog.getSaveFileName(self, filter='CSV (*.csv)')[0]
        if not fname:
            return
        
        column_len = self.channelLen
        
        line = ['Data' + str(i) for i in range(column_len)]
        line.insert(0, 'Time')
        column_len += 1
        
        with open(fname, 'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(line)
                    
            for row in range(self.tbDatas.rowCount()):
                for column in range(column_len):
                    item = self.tbDatas.item(row, column)
                    if item:
                        d = item.text()
                    else:
                        d = '0'
                    line[column] = d
                writer.writerow(line)
        
        self.onReset()
        
    def initGUI(self):  
        import os
        
        self.setWindowTitle("Sensor Monitor")
        self.resize(1280, 800)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + "/smon.png"))
        
        self.initMenuStatusBar()

        header = self.initHeader()
        body = self.initBody()
                
        central = QWidget()
        centralInner = QVBoxLayout()
        centralInner.addWidget(header)
        centralInner.addWidget(body)
        central.setLayout(centralInner)
        self.setCentralWidget(central)
        
        self.channelLen = 0
        self.iRawCurves = 0
        self.onRbAuto()
    
    def initHeader(self):
        self.colors = [QColor(name) for name in [
            'deeppink', 'hotpink', 'lightpink',
            'dodgerblue', 'deepskyblue', 'lightskyblue', 
            'forestgreen', 'lime', 'greenyellow', 
            'orange', 'gold', 'yellow',
            'darkmagenta', 'darkorchid', 'magenta', 'violet',] 
        ]

        self.pens = [QPen(c, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin) for c in self.colors ]
             
        header = QGroupBox("Configuration")
        headerInner = QGridLayout()
        
        headerInner00 = QWidget()
        headerInner10 = QWidget()
        
        headerInnerChCurve = self.initHeaderInnerChCurve()
        headerInnerOption = self.initHeaderInnerOption()
        
        headerInner00.setLayout(headerInnerChCurve)
        headerInner10.setLayout(headerInnerOption)

        headerInner.addWidget(headerInner00, 0, 0)
        headerInner.addWidget(headerInner10, 1, 0)
        
        self.cbPortList = QComboBox()
        headerInner.addWidget(self.cbPortList,0,1)
        self.onPortListTimer()
        
        self.cbPortBaud = QComboBox()
        self.cbPortBaud.addItems(['115200', '57600', '38400', '19200', '9600'])
        headerInner.addWidget(self.cbPortBaud, 1, 1)
        
        self.btConnect = QPushButton("Connect")
        self.btConnect.clicked.connect(self.onConnect)
        
        self.btDisconnect = QPushButton("Disconnect")
        self.btDisconnect.clicked.connect(self.onDisconnect)
        self.btDisconnect.setEnabled(False)

        headerInner.addWidget(self.btConnect, 0, 2)
        headerInner.addWidget(self.btDisconnect, 1, 2)        
        header.setLayout(headerInner)
        
        return header

    def initHeaderInnerChCurve(self):
        headerInnerChCurve = QHBoxLayout()
        
        self.chCurves = [None] * (MAX_CHANNEL + 1)

        for i in range(MAX_CHANNEL):
            self.chCurves[i] = self.initChCurve("D"+str(i), self.colors[i], self.onChCurve, i)
            headerInnerChCurve.addWidget(self.chCurves[i])

        self.chCurvesSelect = self.initChCurve("ALL", Qt.darkGray, self.onChCurveSelect, -1)
        self.chCurvesSelect.setTristate(True) 
        headerInnerChCurve.addWidget(self.chCurvesSelect)
        
        return headerInnerChCurve
    
    def initHeaderInnerOption(self):
        headerInnerOption = QHBoxLayout()

        rbAuto = QRadioButton('Auto')
        rbAuto.clicked.connect(self.onRbAuto)
        rbAuto.setChecked(True)
        rbManual = QRadioButton('Manual')
        rbManual.clicked.connect(self.onRbManual)
        
        self.leMin = QLineEdit()
        self.leMin.setText('-10')
        self.leMin.setFixedWidth(50)
        self.leMax = QLineEdit()
        self.leMax.setText('10')
        self.leMax.setFixedWidth(50)
        
        self.btManualOk = QPushButton('Ok')
        self.btManualOk.clicked.connect(self.onBtManualOk)
        self.cbCurveStyle = QComboBox()
        self.cbCurveStyle.addItems(['Lines', 'Sticks', 'Steps', 'Dots'])
        self.cbCurveStyle.currentIndexChanged.connect(self.onCurveStyle)
        
        self.plotBgColors = {'Whitesmoke':QBrush(QColor('Whitesmoke')), 
                             'Lightgray':QBrush(QColor('Lightgray')), 
                             'Indigo':QBrush(QColor('Indigo')), 
                             'Midnightblue':QBrush(QColor('Midnightblue')), 
                             'Darkslategray':QBrush(QColor('Darkslategray')), 
                             'Black':QBrush(QColor('Black'))}
        
        self.cbPlotBgColor = QComboBox()
        self.cbPlotBgColor.addItems(list(self.plotBgColors))
        self.cbPlotBgColor.setCurrentIndex(4)
        self.cbPlotBgColor.currentIndexChanged.connect(self.onPlotBgColor)
        self.cbCurveWidth = QComboBox()
        self.cbCurveWidth.addItems(['2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.cbCurveWidth.setFixedWidth(50)
        self.cbCurveWidth.currentIndexChanged.connect(self.onCurveWidth)
        
        self.btSaveData = QPushButton('Save As')
        self.btSaveData.setEnabled(False)
        self.btSaveData.clicked.connect(self.onSaveData)
        self.btReset = QPushButton("Reset")
        self.btReset.clicked.connect(self.onReset)
        self.btReset.setEnabled(False)
        
        self.btStopStart = QPushButton("Stop")
        self.btStopStart.clicked.connect(self.onStopStart)
        self.btStopStart.setEnabled(False)
        
        headerInnerOption.addStretch(1)
        headerInnerOption.addWidget(rbAuto)
        headerInnerOption.addWidget(rbManual)
        headerInnerOption.addWidget(self.leMin)
        headerInnerOption.addWidget(QLabel('~'))
        headerInnerOption.addWidget(self.leMax)
        headerInnerOption.addWidget(self.btManualOk)
        headerInnerOption.addStretch(1)
        headerInnerOption.addWidget(QLabel('Style'))
        headerInnerOption.addWidget(self.cbCurveStyle)
        headerInnerOption.addWidget(QLabel('BgColor'))
        headerInnerOption.addWidget(self.cbPlotBgColor)
        headerInnerOption.addWidget(QLabel('Width'))
        headerInnerOption.addWidget(self.cbCurveWidth)        
        headerInnerOption.addStretch(2)
        headerInnerOption.addWidget(self.btSaveData)
        headerInnerOption.addWidget(self.btReset)
        headerInnerOption.addWidget(self.btStopStart)        
        headerInnerOption.addStretch(1)
        
        return headerInnerOption

    def initBody(self):
        body = QGroupBox('Plot') 
        self.bodyInner = QVBoxLayout()
        body.setLayout(self.bodyInner)
  
        self.initPlot()       
        self.initTable()        
        
        return body        
                
    def initPlot(self):
        self.plot = qwt.QwtPlot(self)

        grid = qwt.QwtPlotGrid()
        grid.setMajorPen(QPen(Qt.darkGray, 0, Qt.DotLine))
        grid.attach(self.plot)
        
        self.plot.setCanvasBackground(QBrush(QColor('Darkslategray')))
        self.plot.setAxisTitle(qwt.QwtPlot.xBottom, 'Time')
        self.plot.setAxisScale(qwt.QwtPlot.xBottom, 0, PLOT_X_INIT_MAX, 0.5)
        self.plot.setAxisTitle(qwt.QwtPlot.yLeft, 'Value')
        self.plot.setAxisAutoScale(qwt.QwtPlot.yLeft)
        
        self.curves = [qwt.QwtPlotCurve() for _ in range(MAX_CHANNEL)]

        for i in range(MAX_CHANNEL):
            self.curves[i].setRenderHint(qwt.QwtPlotItem.RenderAntialiased)
            self.curves[i].setPen(self.pens[i])
            self.curves[i].setStyle(qwt.QwtPlotCurve.Lines)
            self.curves[i].attach(self.plot)

        self.bodyInner.addWidget(self.plot)

    def initTable(self):
        lbHeader = ['Time']
        lbHeader += ['D' + str(i) for i in range(MAX_CHANNEL)]
         
        self.tbDatas = QTableWidget()
        self.tbDatas.setColumnCount(MAX_CHANNEL+1)
        self.tbDatas.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbDatas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbDatas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbDatas.setHorizontalHeaderLabels(lbHeader)
        self.tbDatas.setFixedHeight(185)
        self.tbDatas.setMinimumWidth(1280)
        
        self.bodyInner.addWidget(self.tbDatas)
        self.resizeTable()
    
    def initMenuStatusBar(self):
        help_menu = self.menuBar().addMenu("&Help")        
        about = QAction("&About", self)
        about.setShortcut('F1')
        about.setStatusTip('About the Sensor Monotor')
        about.triggered.connect(self.onAbout)
        help_menu.addAction(about)
       
        self.sbText = QLabel('Idle')
        self.statusBar().addWidget(self.sbText, 1)
        
    def initChCurve(self, label, color, connect_fn, connect_param):
        checkBox = QCheckBox(label, self)
        checkBox.setChecked(False)
        p = QPalette()
        #p.setColor(QPalette.Foreground, color)
        p.setColor(QPalette.Window, color)
        checkBox.setPalette(p)
        checkBox.clicked.connect(lambda: connect_fn(connect_param))
        checkBox.setEnabled(False)
        
        return checkBox