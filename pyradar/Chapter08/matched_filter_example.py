"""
Project: RadarBook
File: matched_filter_example.py
Created by: Lee A. Harrison
On: 1/23/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter08.ui.MatchedFilter_ui import Ui_MainWindow
from numpy import linspace, log10, zeros, exp, sqrt, finfo, conj, ones
from scipy.fftpack import ifft, fft, fftshift
from scipy.constants import pi, c
from scipy.signal.windows import hanning, hamming, blackmanharris, kaiser
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MatchedFilter(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.pulsewidth.returnPressed.connect(self._update_canvas)
        self.target_range.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)
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
        bandwidth = float(self.bandwidth.text())
        pulsewidth = float(self.pulsewidth.text())
        target_range = self.target_range.text().split(',')
        target_rcs = self.target_rcs.text().split(',')

        t_range = [float(r) for r in target_range]
        t_rcs = [float(r) for r in target_rcs]

        # Get the selected window from the form
        window_type = self.window_type.currentText()

        # Number of samples
        N = int(2 * bandwidth * pulsewidth) * 8

        if window_type == 'Kaiser':
            coefficients = kaiser(N, 6, True)
        elif window_type == 'Blackman-Harris':
            coefficients = blackmanharris(N, True)
        elif window_type == 'Hanning':
            coefficients = hanning(N, True)
        elif window_type == 'Hamming':
            coefficients = hamming(N, True)
        elif window_type == 'Rectangular':
            coefficients = ones(N)

        # Set up the time vector
        t = linspace(-0.5 * pulsewidth, 0.5 * pulsewidth, N)

        # Calculate the baseband return signal
        s = zeros(N, dtype=complex)

        # Chirp slope
        alpha = 0.5 * bandwidth / pulsewidth

        for r, rcs in zip(t_range, t_rcs):
            s += sqrt(rcs) * exp(1j * 2.0 * pi * alpha * (t - 2.0 * r / c) ** 2)

        # Transmit signal
        st = exp(1j * 2 * pi * alpha * t ** 2)

        # Impulse response and matched filtering
        Hf = fft(conj(st * coefficients))
        Si = fft(s)
        so = fftshift(ifft(Si * Hf))

        # Range window
        range_window = linspace(-0.25 * c * pulsewidth, 0.25 * c * pulsewidth, N)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Create the line plot
        self.axes1.plot(range_window, 20.0 * log10(abs(so) / N + finfo(float).eps), '')
        self.axes1.set_xlim(0, max(t_range) + 100)
        self.axes1.set_ylim(-60, max( 20.0 * log10(abs(so) / N)) + 10)

        # Set the x and y axis labels
        self.axes1.set_xlabel("Range (m)", size=12)
        self.axes1.set_ylabel("Amplitude (dBsm)", size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('Matched Filter Range Profile', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = MatchedFilter()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = MatchedFilter()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
