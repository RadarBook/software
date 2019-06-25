"""
Project: RadarBook
File: back_projection_cv_example.py
Created by: Lee A. Harrison
On: 2/12/2019
Created with: PyCharm
"""
import sys
from Chapter10.ui.BackProjectionCV_ui import Ui_MainWindow
from scipy import linspace, meshgrid, log10, sqrt, radians, zeros_like, amax, ones, squeeze
from scipy import outer
from scipy.io import loadmat
from scipy.fftpack import next_fast_len
from scipy.signal.windows import hanning, hamming
from pathlib import Path
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
        self.x_span.returnPressed.connect(self._update_canvas)
        self.y_span.returnPressed.connect(self._update_canvas)
        self.nx_ny.returnPressed.connect(self._update_canvas)
        self.az_start_end.returnPressed.connect(self._update_canvas)
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
        x_span = float(self.x_span.text())
        y_span = float(self.y_span.text())

        nx_ny = self.nx_ny.text().split(',')
        nx = int(nx_ny[0])
        ny = int(nx_ny[1])

        az_start_end = self.az_start_end.text().split(',')
        az_start = float(az_start_end[0])
        az_end = float(az_start_end[1])

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

        # Set up the image space
        self.xi = linspace(-0.5 * x_span, 0.5 * x_span, nx)
        self.yi = linspace(-0.5 * y_span, 0.5 * y_span, ny)
        x_image, y_image = meshgrid(self.xi, self.yi)
        z_image = zeros_like(x_image)

        # Set the data from the file
        polarization = self.polarization.currentText()
        if polarization == 'VV':
            signal = vv
        elif polarization == 'HH':
            signal = hh
        else:
            signal = hv

        # Choose the pulses in the azimuth range
        sensor_az = []
        index = []

        i = 0
        for az in azim:
            if az_start <= az <= az_end:
                sensor_az.append(radians(az))
                index.append(i)
            i += 1

        signal1 = signal[:, index]

        sensor_el = radians(elev) * ones(len(sensor_az))
        frequency = FGHz * 1e9

        nf = len(frequency)
        na = len(sensor_az)

        fft_length = 4 * next_fast_len(len(frequency))

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
        signal1 *= coefficients

        # Reconstruct the image
        self.bp_image = backprojection.reconstruct2(signal1, sensor_az, sensor_el, x_image, y_image, z_image, frequency, fft_length)

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
