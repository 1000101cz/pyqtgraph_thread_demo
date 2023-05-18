import sys

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class Worker(QtCore.QThread):
    resultReady = QtCore.pyqtSignal(int)
    time = 12

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

    def run(self):
        while True:
            # Emit a signal with the result
            self.resultReady.emit(1)

            # Sleep for a while before the next computation
            self.msleep(self.time)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("window.ui", self)

        self.setWindowTitle("Curveeno 2023")

        self.curve = None

        self.counter = 0

        # Create a worker thread
        self.worker_thread = Worker()

        # Connect the worker's signal to the update_plot method
        self.worker_thread.resultReady.connect(self.init)

        self.pushButton_plus.clicked.connect(self.plus)
        self.pushButton_minus.clicked.connect(self.minus)

        # Start the worker thread
        self.worker_thread.start()

    def init(self):

        if self.curve is None:
            time = np.arange(0, 8 * np.pi, np.pi / 100)

            data = np.sin(time)

            self.curve = self.graphicsView.plot(data, pen=pg.mkPen(color='b', width=2))
        else:
            time = np.arange(self.counter * (np.pi/100), 8 * np.pi + self.counter * (np.pi/100), np.pi / 100)

            if len(time) > 800:
                time = time[:800]

            data = np.sin(time)
            self.curve.setData(np.arange(0, 800), data)

        self.counter += 1

        if self.counter == 799:
            self.counter = 0

        self.graphicsView.update()

    def plus(self):
        if self.worker_thread.time > 1:
            self.worker_thread.time -= 1
        if self.worker_thread.time == 1:
            self.pushButton_plus.setEnabled(False)

    def minus(self):
        self.worker_thread.time += 1
        self.pushButton_plus.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
