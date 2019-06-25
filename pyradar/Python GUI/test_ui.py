import sys

#import numpy as np

import random

from test_window2 import Ui_MainWindow

#from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QMainWindow
#, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton


from matplotlib.backends.qt_compat import QtCore
#, QtWidgets

from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

#import matplotlib.pyplot as plt


class myTest(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Set the window title
        # self.setWindowTitle('Whatever this function does!')

        # Set the window icon
        # self.setWindowIcon(QIcon('python_icon.png'))

        # Connect to the button
        self.pushButton.clicked.connect(self._update_canvas)

        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

    def _update_canvas(self):
        data = [random.random() for i in range(25)]
        ax = self.axes
        ax.clear()
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.my_canvas.draw()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = myTest()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()
