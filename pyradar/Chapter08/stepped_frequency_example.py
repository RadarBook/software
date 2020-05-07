"""
Project: RadarBook
File: stepped_frequency_example.py
Created by: Lee A. Harrison
On: 1/23/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter08.ui.SteppedFrequency_ui import Ui_MainWindow
from numpy import linspace, log10, zeros, exp, sqrt, finfo, ones
from scipy.fftpack import ifft, next_fast_len
from scipy.constants import pi, c
from scipy.signal.windows import hanning, hamming, blackmanharris, kaiser
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class SteppedFrequency(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.number_of_steps.returnPressed.connect(self._update_canvas)
        self.frequency_step.returnPressed.connect(self._update_canvas)
        self.prf.returnPressed.connect(self._update_canvas)
        self.target_range.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)
        self.target_velocity.returnPressed.connect(self._update_canvas)
        self.window_type.currentIndexChanged.connect(self._update_canvas)

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
        number_of_steps = int(self.number_of_steps.text())
        frequency_step = float(self.frequency_step.text())
        prf = float(self.prf.text())
        target_range = self.target_range.text().split(',')
        target_rcs = self.target_rcs.text().split(',')
        target_velocity = self.target_velocity.text().split(',')

        t_range = [float(r) for r in target_range]
        t_rcs = [float(r) for r in target_rcs]
        t_velocity = [float(v) for v in target_velocity]

        # Get the selected window from the form
        window_type = self.window_type.currentText()

        if window_type == 'Kaiser':
            coefficients = kaiser(number_of_steps, 6, True)
        elif window_type == 'Blackman-Harris':
            coefficients = blackmanharris(number_of_steps, True)
        elif window_type == 'Hanning':
            coefficients = hanning(number_of_steps, True)
        elif window_type == 'Hamming':
            coefficients = hamming(number_of_steps, True)
        elif window_type == 'Rectangular':
            coefficients = ones(number_of_steps)

        # Calculate the base band return signal
        s = zeros(number_of_steps, dtype=complex)

        for rng, rcs, v in zip(t_range, t_rcs, t_velocity):
            s += [sqrt(rcs) * exp(-1j * 4.0 * pi / c * (i * frequency_step) * (rng - v * (i / prf)))
                  for i in range(number_of_steps)]

            n = next_fast_len(10 * number_of_steps)
            sf = ifft(s * coefficients, n) * float(n) / float(number_of_steps)

        # range_resolution = c / (2.0 * number_of_steps * frequency_step)
        range_unambiguous = c / (2.0 * frequency_step)

        range_window = linspace(0, range_unambiguous, n)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Create the line plot
        self.axes1.plot(range_window, 20.0 * log10(abs(sf) + finfo(float).eps), '')

        # Set the x and y axis labels
        self.axes1.set_xlabel("Range (m)", size=12)
        self.axes1.set_ylabel("Amplitude (dBsm)", size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('Stepped Frequency Range Profile', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = SteppedFrequency()  # Set the form
    form.show()                # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = SteppedFrequency()     # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
