"""
Project: RadarBook
File: cfar_example.py
Created by: Lee A. Harrison
On: 10/12/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter06.ui.CFAR_ui import Ui_MainWindow
from numpy import log10, sqrt, sin, cos, linspace, seterr, random as rnd
from scipy.constants import pi
from scipy import fftpack
from Libs.detection.cfar import cfar
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class CFAR(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.guard_cells.returnPressed.connect(self._update_canvas)
        self.reference_cells.returnPressed.connect(self._update_canvas)
        self.bias.returnPressed.connect(self._update_canvas)
        self.cfar_type.currentIndexChanged.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure() 
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for the first display
        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        seterr(divide='ignore')
        # Generate a sample signal to be used (later used matched filter output)
        number_of_samples = 1000
        i_noise = rnd.normal(0, 0.05, number_of_samples)
        q_noise = rnd.normal(0, 0.05, number_of_samples)

        noise_signal = sqrt(i_noise ** 2 + q_noise ** 2)

        # Create the time array
        t = linspace(0.0, 1.0, number_of_samples)

        # Create example signal for the CFAR process
        s1 = 0.4 * cos(2 * pi * 600 * t) + 1j * 0.4 * sin(2 * pi * 600 * t)
        s2 = 0.1 * cos(2 * pi * 150 * t) + 1j * 0.1 * sin(2 * pi * 150 * t)
        s3 = 0.2 * cos(2 * pi * 100 * t) + 1j * 0.2 * sin(2 * pi * 100 * t)

        # Sum for the example signal
        signal = abs(fftpack.fft(s1 + s2 + s3 + noise_signal))
        signal[0] = 0

        # Get the CFAR type from the form
        cfar_type = self.cfar_type.currentText()

        # Set up the key word args for the inputs
        kwargs = {'signal': signal,
                  'guard_cells': int(self.guard_cells.text()),
                  'reference_cells': int(self.reference_cells.text()),
                  'bias': float(self.bias.text()),
                  'cfar_type': cfar_type}

        # Calculate the CFAR threshold
        cfar_threshold = cfar(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(10.0 * log10(signal), '', label='Signal')
        self.axes1.plot(cfar_threshold, 'r--', label='CFAR Threshold')

        # Set the plot title and labels
        self.axes1.set_title('Constant False Alarm Rate', size=14)
        self.axes1.set_ylabel('Signal Strength (dB)', size=12)
        self.axes1.set_xlabel('Range (m)', size=12)
        self.axes1.set_ylim(-10, 30)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = CFAR(parent)  # Set the form
    form.show()    # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = CFAR()                 # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
