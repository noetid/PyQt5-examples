#!/usr/bin/env python3
# coding=utf-8
# @author: https://github.com/pitelf

import ctypes
import sys

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUiType
from scipy.integrate import solve_ivp

# show icon on taskbar https://stackoverflow.com/questions/1551605/
myappid = 'Van der Pol oscillator'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pg.setConfigOption('foreground', 'k')
pg.setConfigOption('background', 'w')
pg.setConfigOptions(antialias=True)

app = QApplication(sys.argv)
app.setApplicationName('Van der Pol oscillator')
form_class, base_class = loadUiType('Van_der_Pol_Form.ui')


class MainWindow(QMainWindow, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setWindowIcon(QIcon('Van_der_Pol_Main.ico'))
        self.setupUi(self)
        #self.statusbar.showMessage('Message in statusbar.')
        self.lblEquation.setPixmap(QPixmap('vdp.bmp'))
        self.actionTrajectory_plot.setChecked(True)
        self.actionPhase_plot.setChecked(False)
        self.showMaximized()
        # data setup
        self.t_end = 25.0
        self.mu = 0.0
        self.t = np.linspace(0, self.t_end, 500)
        sol = solve_ivp(self.vdp, (0.0, self.t_end), (2.0, 0.0), args=(self.mu,), dense_output=True)

        # plot setup
        pen = pg.mkPen(color=(255, 0, 0), width=3, style=Qt.SolidLine)
        self.vdpPlot.setAspectLocked(lock=False)
        self.vdpPlot.getAxis("left").tickFont = QFont("Times", 12)
        self.vdpPlot.getAxis("bottom").tickFont = QFont("Times", 12)
        self.label_style = {'color': 'black', "font-size": '18pt', "font-style": 'italic'}
        self.vdpPlot.setLabel("bottom", 't', **self.label_style)
        self.vdpPlot.setLabel("left", 'x(t)', **self.label_style)
        self.vdpPlot.showGrid(x=True, y=True)
        self.vdpPlot.setXRange(0, self.t_end, padding=0)
        # initial solution plot for mu = 0.0
        self.myplot = self.vdpPlot.plot(self.t, sol.sol(self.t)[0], pen=pen)

    @staticmethod
    def vdp(t, u, mu):
        return [u[1], mu * (1 - u[0] ** 2) * u[1] - u[0]]

    def trajectoryplot_click(self):
        self.actionTrajectory_plot.setChecked(True)
        self.actionPhase_plot.setChecked(False)
        self.vdpPlot.setAspectLocked(lock=False)
        self.vdpPlot.setLabel("left", "x(t)", **self.label_style)
        self.vdpPlot.setLabel("bottom", 't', **self.label_style)
        self.update_mu()

    def phaseplot_click(self):
        self.actionTrajectory_plot.setChecked(False)
        self.actionPhase_plot.setChecked(True)
        self.vdpPlot.setAspectLocked(lock=True)
        self.vdpPlot.setLabel("left", "x'(t)", **self.label_style)
        self.vdpPlot.setLabel("bottom", 'x(t)', **self.label_style)
        self.update_mu()

    def update_mu(self):
        self.mu = self.sldMu.value() / 10.0
        self.vdpPlot.setTitle(f'Van der Pol oscillator ODE solution for μ = {self.mu}')
        sol = solve_ivp(self.vdp, (0.0, self.t_end), (2.0, 0.0), args=(self.mu,), dense_output=True)
        if self.actionTrajectory_plot.isChecked():
            self.myplot.setData(self.t, sol.sol(self.t)[0])
        else:
            self.myplot.setData(sol.sol(self.t)[0], sol.sol(self.t)[1])
        self.vdpPlot.autoRange()

    def export(self):
        # https://github.com/pyqtgraph/pyqtgraph/issues/464
        exporter = pg.exporters.ImageExporter(self.vdpPlot.plotItem)
        exporter.parameters()['width'] = int(self.vdpPlot.frameGeometry().width())
        exporter.export(f'VdP plot mu = {self.mu}.png')


if __name__ == '__main__':
    form = MainWindow()
    form.setWindowTitle('PyQt5 Example. Van der Pol oscillator solution.')
    form.show()
    sys.exit(app.exec_())
