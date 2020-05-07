"""
Project: RadarBook
File: low_pass_filter_example.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter05.ui.LowPassFilter_ui import Ui_MainWindow
from numpy import log10
from scipy import signal
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class LowPassFilter(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.filter_order.returnPressed.connect(self._update_canvas)
        self.critical_frequency.returnPressed.connect(self._update_canvas)
        self.maximum_ripple.returnPressed.connect(self._update_canvas)
        self.minimum_attenuation.returnPressed.connect(self._update_canvas)
        self.filter_type.currentIndexChanged.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.fig = fig
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for the first display
        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value
        :return:
        """
        # Get the parameters from the form
        filter_order = int(self.filter_order.text())
        critical_frequency = int(self.critical_frequency.text())
        maximum_ripple = float(self.maximum_ripple.text())
        minimum_attenuation = float(self.minimum_attenuation.text())

        # Get the selected filter from the form
        filter_type = self.filter_type.currentText()

        if filter_type == 'Butterworth':
            b, a = signal.butter(filter_order, critical_frequency, 'low', analog=True)
        elif filter_type == 'Chebyshev':
            b, a = signal.cheby1(filter_order, maximum_ripple, critical_frequency, 'low', analog=True)
        elif filter_type == 'Bessel':
            b, a = signal.bessel(filter_order, critical_frequency, 'low', analog=True, norm='phase')
        elif filter_type == 'Elliptic':
            b, a = signal.ellip(filter_order, maximum_ripple, minimum_attenuation, critical_frequency, 'low', analog=True)

        w, h = signal.freqs(b, a)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Create the line plot
        self.axes1.semilogx(w, 20 * log10(abs(h)))

        # Set the y axis limit
        self.axes1.set_ylim(-80, 5)

        # Set the x and y axis labels
        self.axes1.set_xlabel("Frequency (Hz)", size=12)
        self.axes1.set_ylabel("Amplitude (dB)", size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('Filter Response', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = LowPassFilter()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = LowPassFilter()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
