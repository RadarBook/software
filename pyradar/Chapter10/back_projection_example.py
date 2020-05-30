"""
Project: RadarBook
File: back_projection_example.py
Created by: Lee A. Harrison
On: 2/10/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter10.ui.BackProjection_ui import Ui_MainWindow
from numpy import linspace, meshgrid, log10, sqrt, radians, sin, cos, zeros_like, zeros, dot, exp, amax, ones, outer
from scipy.fftpack import next_fast_len
from scipy.constants import c, pi
from scipy.signal.windows import hanning, hamming
from Libs.sar import backprojection
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class BackProjection(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.range_center.returnPressed.connect(self._update_canvas)
        self.x_target.returnPressed.connect(self._update_canvas)
        self.y_target.returnPressed.connect(self._update_canvas)
        self.rcs.returnPressed.connect(self._update_canvas)
        self.x_span.returnPressed.connect(self._update_canvas)
        self.y_span.returnPressed.connect(self._update_canvas)
        self.nx_ny.returnPressed.connect(self._update_canvas)
        self.start_frequency.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.az_start_end.returnPressed.connect(self._update_canvas)
        self.dynamic_range.returnPressed.connect(self._update_image_only)
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
        Update the figure when the user changes and input value.
        :return:
        """
        # Get the parameters from the form
        range_center = float(self.range_center.text())
        x_target = self.x_target.text().split(',')
        y_target = self.y_target.text().split(',')
        rcs = self.rcs.text().split(',')
        xt = []
        yt = []
        rt = []
        for x, y, r in zip(x_target, y_target, rcs):
            xt.append(float(x))
            yt.append(float(y))
            rt.append(float(r))

        x_span = float(self.x_span.text())
        y_span = float(self.y_span.text())

        nx_ny = self.nx_ny.text().split(',')
        nx = int(nx_ny[0])
        ny = int(nx_ny[1])

        start_frequency = float(self.start_frequency.text())
        bandwidth = float(self.bandwidth.text())

        az_start_end = self.az_start_end.text().split(',')
        az_start = float(az_start_end[0])
        az_end = float(az_start_end[1])

        # Set up the azimuth space
        r = sqrt(x_span ** 2 + y_span ** 2)
        da = c / (2.0 * r * start_frequency)
        na = int((az_end - az_start) / da)
        az = linspace(az_start, az_end, na)

        # Set up the frequency space
        df = c / (2.0 * r)
        nf = int(bandwidth / df)
        frequency = linspace(start_frequency, start_frequency + bandwidth, nf)

        # Set the length of the FFT
        fft_length = next_fast_len(4 * nf)

        # Set up the aperture positions
        sensor_x = range_center * cos(radians(az))
        sensor_y = range_center * sin(radians(az))
        sensor_z = zeros_like(sensor_x)

        # Set up the image space
        self.xi = linspace(-0.5 * x_span, 0.5 * x_span, nx)
        self.yi = linspace(-0.5 * y_span, 0.5 * y_span, ny)
        x_image, y_image = meshgrid(self.xi, self.yi)
        z_image = zeros_like(x_image)

        # Calculate the signal (k space)
        signal = zeros([nf, na], dtype=complex)

        index = 0
        for a in az:
            r_los = [cos(radians(a)), sin(radians(a))]

            for x, y, r in zip(xt, yt, rt):
                r_target = -dot(r_los, [x, y])
                signal[:, index] += r * exp(-1j * 4.0 * pi * frequency / c * r_target)
            index += 1

        # Get the selected window from the form
        window_type = self.window_type.currentText()

        if window_type == 'Hanning':
            h1 = hanning(nf, True)
            h2 = hanning(na, True)
            coefficients = sqrt(outer(h1, h2))
        elif window_type == 'Hamming':
            h1 = hamming(nf, True)
            h2 = hamming(na, True)
            coefficients = sqrt(outer(h1, h2))
        elif window_type == 'Rectangular':
            coefficients = ones([nf, na])

        # Apply the selected window
        signal *= coefficients

        # Reconstruct the image
        self.bp_image = backprojection.reconstruct(signal, sensor_x, sensor_y, sensor_z, range_center, x_image, y_image,
                                                   z_image, frequency, fft_length)

        # Update the image
        self._update_image_only()

    def _update_image_only(self):
        dynamic_range = float(self.dynamic_range.text())

        # Remove the color bar
        try:
            self.cbar.remove()
        except:
            print('Initial Plot')

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        bpi = abs(self.bp_image) / amax(abs(self.bp_image))
        im = self.axes1.pcolor(self.xi, self.yi, 20.0 * log10(bpi), cmap='jet', vmin=-dynamic_range, vmax=0)
        self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
        self.cbar.set_label("(dB)", size=10)

        # Set the plot title and labels
        self.axes1.set_title('Back Projection', size=14)
        self.axes1.set_xlabel('Range (m)', size=12)
        self.axes1.set_ylabel('Cross Range (m)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = BackProjection()       # Set the form
    form.show()                   # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = BackProjection()       # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
