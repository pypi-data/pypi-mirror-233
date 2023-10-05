#!/usr/bin/python3

import sys
from xnode.smonitor import SensorMonotor
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    SensorMonotor().show()
    app.exec()

if __name__ == "__main__":    
    main()