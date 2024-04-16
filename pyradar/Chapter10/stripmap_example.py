"""
Project: RadarBook
File: stripmap_example.py
Created by: Lee A. Harrison
On: 3/24/2020
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter10.ui.Stripmap_ui import Ui_MainWindow
from numpy import linspace, meshgrid, log10, sqrt, ceil, arctan, cos, tan, zeros_like, zeros, exp, amax, ones, radians, \
    outer, finfo
from scipy.fftpack import next_fast_len
from scipy.constants import c, pi
from scipy.signal.windows import hann, hamming
from Libs.sar import backprojection
from Libs.antenna.array.linear_array_un import array_factor
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Stripmap(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.range_center.returnPressed.connect(self._update_canvas)
        self.squint_angle.returnPressed.connect(self._update_canvas)
        self.x_target.returnPressed.connect(self._update_canvas)
        self.y_target.returnPressed.connect(self._update_canvas)
        self.rcs.returnPressed.connect(self._update_canvas)
        self.x_span.returnPressed.connect(self._update_canvas)
        self.y_span.returnPressed.connect(self._update_canvas)
        self.nx_ny.returnPressed.connect(self._update_canvas)
        self.start_frequency.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.aperture_length.returnPressed.connect(self._update_canvas)
        self.antenna_width.returnPressed.connect(self._update_canvas)
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
        squint_angle = radians(float(self.squint_angle.text()))

        x_center = float(self.range_center.text())
        y_center = x_center * tan(squint_angle)

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

        aperture_length = float(self.aperture_length.text())

        antenna_width = float(self.antenna_width.text())

        # Set up the image space
        self.xi = linspace(-0.5 * x_span + x_center, 0.5 * x_span + x_center, nx)
        self.yi = linspace(-0.5 * y_span + y_center, 0.5 * y_span + y_center, ny)

        x_image, y_image = meshgrid(self.xi, self.yi)
        z_image = zeros_like(x_image)

        # Calculate the wavelength at the start frequency (m)
        wavelength = c / start_frequency

        # Calculate the number of frequencies
        df = c / (2.0 * sqrt(x_span ** 2 + y_span ** 2))
        number_of_frequencies = int(ceil(bandwidth / df))

        # Set up the frequency space
        frequency = linspace(start_frequency, start_frequency + bandwidth, number_of_frequencies)

        # Set the length of the FFT
        fft_length = next_fast_len(4 * number_of_frequencies)

        # Calculate the element spacing (m)
        element_spacing = wavelength / 4.0

        # Calculate the number of elements
        number_of_elements = int(ceil(antenna_width / element_spacing + 1))

        # Calculate the spacing on the synthetic aperture (m)
        aperture_spacing = tan(c / (2 * y_span * start_frequency)) * x_center  # Based on y_span

        # Calculate the number of samples (pulses) on the aperture
        number_of_samples = int(ceil(aperture_length / aperture_spacing + 1))

        # Create the aperture
        synthetic_aperture = linspace(-0.5 * aperture_length, 0.5 * aperture_length, number_of_samples)

        # Calculate the sensor location
        sensor_x = zeros_like(synthetic_aperture)
        sensor_y = synthetic_aperture
        sensor_z = zeros_like(synthetic_aperture)

        # Calculate the signal (k space)
        # Initialize the signal
        signal = zeros([number_of_frequencies, number_of_samples], dtype=complex)

        # Initialize the range center (m)
        range_center = zeros_like(synthetic_aperture)

        # Phase term for the range phase (rad)
        phase_term = -1j * 4.0 * pi * frequency / c

        index = 0
        for sa in synthetic_aperture:
            range_center[index] = sqrt(x_center ** 2 + (y_center - sa) ** 2)

            for x, y, r in zip(xt, yt, rt):
                # Antenna pattern at each target
                target_range = sqrt((x_center + x) ** 2 + (y_center + y - sa) ** 2) - range_center[index]
                target_azimuth = arctan((y_center + y - sa) / (x_center + x))
                antenna_pattern = array_factor(number_of_elements, 0.5 * pi - squint_angle, element_spacing,
                                               start_frequency, 0.5 * pi - target_azimuth, 'Uniform', 0) * cos(squint_angle)

                signal[:, index] += r * antenna_pattern ** 2 * exp(phase_term * target_range)

            index += 1

        # Get the selected window
        window_type = self.window_type.currentText()

        if window_type == 'Hanning':
            h1 = hann(number_of_frequencies, True)
            h2 = hann(number_of_samples, True)
            coefficients = sqrt(outer(h1, h2))
        elif window_type == 'Hamming':
            h1 = hamming(number_of_frequencies, True)
            h2 = hamming(number_of_samples, True)
            coefficients = sqrt(outer(h1, h2))
        elif window_type == 'Rectangular':
            coefficients = ones([number_of_frequencies, number_of_samples])

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
        im = self.axes1.pcolor(self.xi, self.yi, 20.0 * log10(bpi + finfo(float).eps), cmap='jet', vmin=-dynamic_range, vmax=0, shading = 'auto')
        self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
        self.cbar.set_label("(dB)", size=10)

        # Set the plot title and labels
        self.axes1.set_title('Stripmap SAR', size=14)
        self.axes1.set_xlabel('Range (m)', size=12)
        self.axes1.set_ylabel('Cross Range (m)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start(parent=None):
    form = Stripmap(parent)       # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Stripmap()       # Set the form
    form.show()             # Show the form
    app.exec_()             # Execute the app


if __name__ == '__main__':
    main()
