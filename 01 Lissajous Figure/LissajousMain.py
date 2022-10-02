#!/usr/bin/env python3
# coding=utf-8
# @author: https://github.com/noetid

import ctypes
import os
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUiType

# show icon on taskbar https://stackoverflow.com/questions/1551605/
myappid = 'Lissajous 0.1'  # arbitrary string
if os.name == 'nt':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pg.setConfigOption('foreground', 'k')
pg.setConfigOption('background', 'w')

app = QApplication(sys.argv)
app.setApplicationName('PyQtEx')
form_class, base_class = loadUiType('LissajousForm.ui')


class MainWindow(QWidget, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setWindowIcon(QIcon('LissajousMainIco.ico'))
        self.setupUi(self)
        self.showMaximized()
        # data setup
        self.t_end = 50 * np.pi
        self.steps = 2000
        self.x = np.sin(np.linspace(0, self.t_end, self.steps))
        self.y = np.sin(np.linspace(0, self.t_end, self.steps))
        # plot setup
        pen = pg.mkPen(color=(0, 0, 0), width=3, style=Qt.SolidLine)
        self.lissajousPlot.setAspectLocked()
        self.lissajousPlot.getAxis("left").tickFont = QFont("Times", 12)
        self.lissajousPlot.getAxis("bottom").tickFont = QFont("Times", 12)
        label_style = {'color': 'black', "font-size": '18pt', "font-style": 'italic'}
        self.lissajousPlot.setLabel("bottom", 'x', **label_style)
        self.lissajousPlot.setLabel("left", 'y', **label_style)

        self.lissajousPlot.showGrid(x=True, y=True)
        self.lissajousPlot.setXRange(-1.1, 1.1, padding=0)
        self.lissajousPlot.setYRange(-1.1, 1.1, padding=0)
        self.myplot = self.lissajousPlot.plot(self.x, self.y, pen=pen)

    def update_parameters_and_compute_xy(self):
        a = self.sldFreq1.value() / 100.0
        b = self.sldFreq2.value() / 100.0
        delta = self.sldPhase.value() / 100.0
        self.lissajousPlot.setTitle(f'a = {a}, b = {b}, δ = {delta}')
        self.x = np.sin(a * np.linspace(0, self.t_end, self.steps) + delta)
        self.y = np.sin(b * np.linspace(0, self.t_end, self.steps))

    def update_freq1(self):
        self.update_parameters_and_compute_xy()
        self.myplot.setData(self.x, self.y)  # Update the data.

    def update_freq2(self):
        self.update_parameters_and_compute_xy()
        self.myplot.setData(self.x, self.y)  # Update the data.

    def update_phase(self):
        self.update_parameters_and_compute_xy()
        self.myplot.setData(self.x, self.y)


if __name__ == '__main__':
    form = MainWindow()
    form.setWindowTitle('Lissajous figure')
    form.show()
    sys.exit(app.exec_())
