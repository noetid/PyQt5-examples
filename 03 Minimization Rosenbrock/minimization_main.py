#!/usr/bin/env python3
# coding=utf-8
# @author: https://github.com/pitelf

import ctypes
import sys
import warnings

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUiType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.optimize import minimize

# show icon on taskbar https://stackoverflow.com/questions/1551605/
myappid = 'Rosenbrock'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)
app.setApplicationName('Rosenbrock')
form_class, base_class = loadUiType('minimization_form.ui')
# disable scipy warning e.g. RuntimeWarning: Method Nelder-Mead does not use gradient information (jac)
warnings.filterwarnings("ignore", category=RuntimeWarning)


class MainWindow(QMainWindow, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setWindowIcon(QIcon('rosen.ico'))
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.showMaximized()

        # data setup
        self.methods = ['Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG',
                        'L-BFGS-B', 'TNC', 'SLSQP', 'trust-constr',
                        'dogleg', 'trust-ncg', 'trust-krylov', 'trust-exact']
        self.cmbMethods.addItems(self.methods)
        self.cmbMethods.currentIndex = 0
        self.cur_method = self.methods[0]
        # data setup
        self.x = np.linspace(-4.0, 4.0, 400)
        self.y = np.linspace(-4.0, 4.0, 400)
        X, Y = np.meshgrid(self.x, self.y)
        self.Z = self.rosenbrock([X, Y])
        self.paths = None
        self.iter_points = []
        # plot setup
        layout = QVBoxLayout(self.widgetplot)
        dynamic_canvas = FigureCanvas(Figure())
        layout.addWidget(dynamic_canvas)

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax.set_title('Rosenbrock function minimization.\nDouble click for initial point')
        self._dynamic_ax.set_xlabel('x', fontsize=12)
        self._dynamic_ax.set_ylabel('y', fontsize=12)
        self._dynamic_ax.set_xlim(-4.0, 4.0)
        self._dynamic_ax.set_ylim(-4.0, 4.0)
        self._dynamic_ax.set_aspect('equal')
        self.cont = self._dynamic_ax.contour(X, Y, self.Z, cmap='jet', levels=80)
        self._dynamic_ax.figure.canvas.draw()

        dynamic_canvas.mpl_connect('button_press_event', self.mouseClick)

    def change_method(self, method_num):
        self.cur_method = self.methods[method_num]

    def mouseClick(self, event):
        if event.button.name == 'LEFT' and event.dblclick:
            if self.iter_points:
                self._dynamic_ax.lines.remove(self.iter_points[0])
            x0, y0 = event.xdata, event.ydata
            self.iterations = [[x0, y0]]
            res = minimize(self.rosenbrock, np.array([x0, y0]), method=self.cur_method, jac=self.grad,
                           hess=self.hess, tol=1e-6, callback=self.add_iterations)
            self.statusbar.showMessage(
                f'Method: {self.cur_method}, Xmin = {res.x[0]:2.2f}, Ymin = {res.x[1]:2.2f}, f(x, y) = {res.fun:2.2f}')
            self.iterations = np.array(self.iterations)
            self.iter_points = self._dynamic_ax.plot(self.iterations[:, 0], self.iterations[:, 1], color='red',
                                                     marker='o', markerfacecolor='black')
            self._dynamic_ax.figure.canvas.draw()

    def add_iterations(self, xk, *args):
        self.iterations.append(xk.tolist())

    def rosenbrock(self, X):
        return (1 - X[0]) ** 2 + 100 * (X[1] - X[0] ** 2) ** 2

    def grad(self, X):
        return np.array([-400 * X[0] * X[1] + 400 * X[0] ** 3 + 2 * X[0] - 2, 200 * X[1] - 200 * X[0] ** 2])

    def hess(self, X):
        return np.array([[-400 * X[1] + 1200 * X[0] ** 2.0 + 2.0, -400 * X[0]], [-400 * X[0], 200]])


if __name__ == '__main__':
    form = MainWindow()
    form.setWindowTitle('Rosenbrock function minimization')
    form.show()
    sys.exit(app.exec_())
