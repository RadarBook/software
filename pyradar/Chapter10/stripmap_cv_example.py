"""
Project: RadarBook
File: stripmap_cv_example.py
Created by: Lee A. Harrison
On: 3/25/2020
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter10.ui.StripmapCV_ui import Ui_MainWindow
from numpy import linspace, meshgrid, log10, sqrt, radians, zeros_like, amax, ones, squeeze, tan, ceil, zeros, arctan, \
    cos, degrees, outer
from scipy.constants import speed_of_light as c, pi
from scipy.io import loadmat
from scipy.fftpack import next_fast_len
from scipy.signal.windows import hann, hamming
from pathlib import Path
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
        self.x_span.returnPressed.connect(self._update_canvas)
        self.y_span.returnPressed.connect(self._update_canvas)
        self.nx_ny.returnPressed.connect(self._update_canvas)
        self.aperture_length.returnPressed.connect(self._update_canvas)
        self.antenna_width.returnPressed.connect(self._update_canvas)
        self.dynamic_range.returnPressed.connect(self._update_image_only)
        self.window_type.currentIndexChanged.connect(self._update_canvas)
        self.target.currentIndexChanged.connect(self._update_canvas)
        self.polarization.currentIndexChanged.connect(self._update_canvas)

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

        x_span = float(self.x_span.text())
        y_span = float(self.y_span.text())

        nx_ny = self.nx_ny.text().split(',')
        nx = int(nx_ny[0])
        ny = int(nx_ny[1])

        aperture_length = float(self.aperture_length.text())

        antenna_width = float(self.antenna_width.text())

        # Load the selected target
        target = self.target.currentText()

        base_path = Path(__file__).parent

        if target == 'Backhoe Elevation 0':
            b = loadmat(base_path / "backhoe_0.mat")
        elif target == 'Backhoe Elevation 30':
            b = loadmat(base_path / "backhoe_30.mat")
        elif target == 'Camry Elevation 30':
            b = loadmat(base_path / "Camry_el30.0000.mat")
        elif target == 'Camry Elevation 40':
            b = loadmat(base_path / "Camry_el40.0000.mat")
        elif target == 'Camry Elevation 50':
            b = loadmat(base_path / "Camry_el50.0000.mat")
        elif target == 'Camry Elevation 60':
            b = loadmat(base_path / "Camry_el60.0000.mat")
        elif target == 'Tacoma Elevation 30':
            b = loadmat(base_path / "ToyotaTacoma_el30.0000.mat")
        elif target == 'Tacoma Elevation 40':
            b = loadmat(base_path / "ToyotaTacoma_el40.0000.mat")
        elif target == 'Tacoma Elevation 50':
            b = loadmat(base_path / "ToyotaTacoma_el50.0000.mat")
        elif target == 'Tacoma Elevation 60':
            b = loadmat(base_path / "ToyotaTacoma_el60.0000.mat")
        elif target == 'Jeep Elevation 30':
            b = loadmat(base_path / "Jeep99_el30.0000.mat")
        elif target == 'Jeep Elevation 40':
            b = loadmat(base_path / "Jeep99_el40.0000.mat")
        elif target == 'Jeep Elevation 50':
            b = loadmat(base_path / "Jeep99_el50.0000.mat")
        elif target == 'Jeep Elevation 60':
            b = loadmat(base_path / "eep99_el60.0000.mat")

        # Build a list of keys and values for each entry in the structure
        vals = b['data'][0, 0]
        keys = b['data'][0, 0].dtype.descr

        # Assemble the keys / values into variables with the same name as used in MATLAB
        for i in range(len(keys)):
            key = keys[i][0]
            val = squeeze(vals[key])
            exec(key + '=val', locals(), globals())

        # Set the data from the file
        polarization = self.polarization.currentText()
        if polarization == 'VV':
            signal = vv
        elif polarization == 'HH':
            signal = hh
        else:
            signal = hv

        # Frequency (Hz)
        frequency = FGHz * 1e9

        # Set up the image space
        self.xi = linspace(-0.5 * x_span + x_center, 0.5 * x_span + x_center, nx)
        self.yi = linspace(-0.5 * y_span + y_center, 0.5 * y_span + y_center, ny)

        x_image, y_image = meshgrid(self.xi, self.yi)
        z_image = zeros_like(x_image)

        # Calculate the wavelength at the start frequency (m)
        wavelength = c / frequency[0]

        # Calculate the number of frequencies
        bandwidth = frequency[-1] - frequency[0]
        number_of_frequencies = len(frequency)

        # Set the length of the FFT
        fft_length = next_fast_len(4 * number_of_frequencies)

        # Calculate the element spacing (m)
        element_spacing = wavelength / 4.0

        # Calculate the number of elements
        number_of_elements = int(ceil(antenna_width / element_spacing + 1))

        # Calculate the spacing on the synthetic aperture (m)
        aperture_spacing = tan(c / (2 * y_span * frequency[0])) * x_center  # Based on y_span

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
        signal1 = zeros([number_of_frequencies, number_of_samples], dtype=complex)

        # Initialize the range center (m)
        range_center = zeros_like(synthetic_aperture)

        # For calculating sensor height
        te = tan(radians(elev))

        index = 0
        for sa in synthetic_aperture:
            # Calculate the sensor z location
            sensor_z[index] = sqrt(x_center ** 2 + (y_center - sa) ** 2) * te

            # Calculate the range to the center of the scene
            range_center[index] = sqrt(x_center ** 2 + (y_center - sa) ** 2 + sensor_z[index] ** 2)

            # Calculate the target azimuth (rad)
            target_azimuth = arctan((y_center - sa) / x_center)
            target_azimuth = target_azimuth % (2 * pi)

            # Find the antenna pattern at the target azimuth
            antenna_pattern = array_factor(number_of_elements, 0.5 * pi - squint_angle, element_spacing,
                                           frequency[0], target_azimuth, 'Uniform', 0) * cos(squint_angle)

            # Calculate the return signal
            signal1[:, index] = antenna_pattern ** 2 * signal[:, (abs(degrees(target_azimuth) - azim)).argmin()]

            index += 1

        # Get the selected window from the form
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
        signal1 *= coefficients

        # Reconstruct the image
        self.bp_image = backprojection.reconstruct(signal1, sensor_x, sensor_y, sensor_z, range_center,
                                                   x_image, y_image, z_image, frequency, fft_length)

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
        im = self.axes1.pcolor(self.xi, self.yi, 20.0 * log10(bpi), cmap='jet', vmin=-dynamic_range, vmax=0, shading = 'auto')
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


def start(parent):
    form = Stripmap(parent)       # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Stripmap()             # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
