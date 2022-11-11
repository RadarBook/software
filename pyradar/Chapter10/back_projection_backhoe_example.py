"""
Project: RadarBook
File: back_projection_backhoe_example.py
Created by: Lee A. Harrison
On: 2/20/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter10.ui.BackProjectionBH_ui import Ui_MainWindow
from numpy import linspace, meshgrid, array, radians, amax, ones, squeeze, max, min
from scipy.signal.windows import hann, hamming
from Libs.sar import backprojection
from scipy.io import loadmat
from mpl_toolkits.mplot3d import Axes3D
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
        self.z_span.returnPressed.connect(self._update_canvas)
        self.nx_ny_nz.returnPressed.connect(self._update_canvas)
        self.az_start_end.returnPressed.connect(self._update_canvas)
        self.el_start_end.returnPressed.connect(self._update_canvas)
        self.dynamic_range.returnPressed.connect(self._update_image_only)
        self.polarization.currentIndexChanged.connect(self._update_canvas)
        self.window_type.currentIndexChanged.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.fig = fig
        self.axes1 = fig.add_subplot(111, projection='3d', facecolor='white')
        self.my_canvas = FigureCanvas(fig)
        self.axes1.mouse_init()

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
        z_span = float(self.z_span.text())

        nx_ny_nz = self.nx_ny_nz.text().split(',')
        self.nx = int(nx_ny_nz[0])
        self.ny = int(nx_ny_nz[1])
        self.nz = int(nx_ny_nz[2])

        az_start_end = self.az_start_end.text().split(',')
        az_start = int(az_start_end[0])
        az_end = int(az_start_end[1])

        el_start_end = self.el_start_end.text().split(',')
        el_start = int(el_start_end[0])
        el_end = int(el_start_end[1])

        # Get the selected window from the form
        window_type = self.window_type.currentText()

        # Get the polarization from the form
        polarization = self.polarization.currentText()

        x = linspace(-0.5 * x_span, 0.5 * x_span, self.nx)
        y = linspace(-0.5 * y_span, 0.5 * y_span, self.ny)
        z = linspace(-0.5 * z_span, 0.5 * z_span, self.nz)
        self.x_image, self.y_image, self.z_image = meshgrid(x, y, z, indexing='ij')

        fft_length = 8192

        # el 18 - 43 (-1)
        # az 66 - 115 (-1)

        # Initialize the image
        self.bp = 0

        # Loop over the azimuth and elevation angles
        for el in range(el_start, el_end + 1):
            for az in range(az_start, az_end + 1):
                print('El {0:d} Az {1:d}'.format(el, az))
                filename = '../../Backhoe_CP/3D_Challenge_Problem/3D_K_Space_Data/backhoe_el{0:03d}_az{1:03d}.mat'.format(el, az)
                b = loadmat(filename)

                # build a list of keys and values for each entry in the structure
                vals = b['data'][0, 0]  # <-- set the array you want to access.
                keys = b['data'][0, 0].dtype.descr

                # Assemble the keys and values into variables with the same name as that used in MATLAB
                for i in range(len(keys)):
                    key = keys[i][0]
                    val = squeeze(vals[key])
                    exec(key + '=val', locals(), globals())

                # Select the polarization
                if polarization == 'VV':
                    signal = vv
                elif polarization == 'HH':
                    signal = hh
                else:
                    signal = vhhv
                sensor_az = radians(azim)
                sensor_el = radians(elev)
                frequency = FGHz * 1e9

                nf = len(frequency)
                na = len(sensor_az)
                ne = len(sensor_el)

                coefficients = ones([nf, ne, na])

                # Get the window
                if window_type == 'Hanning':
                    h1 = hann(nf, True)
                    h2 = hann(na, True)
                    h3 = hann(ne, True)

                    for i in range(nf):
                        for j in range(ne):
                            for k in range(na):
                                coefficients[i, j, k] = (h1[i] * h2[k] * h3[j]) ** (1.0 / 3.0)

                elif window_type == 'Hamming':
                    h1 = hamming(nf, True)
                    h2 = hamming(na, True)
                    h3 = hamming(ne, True)

                    for i in range(nf):
                        for j in range(ne):
                            for k in range(na):
                                coefficients[i, j, k] = (h1[i] * h2[k] * h3[j]) ** (1.0 / 3.0)

                # Apply the window coefficients
                signal *= coefficients

                # Reconstruct the image
                self.bp += backprojection.reconstruct3(signal, sensor_az, sensor_el, self.x_image, self.y_image,
                                                       self.z_image, frequency, fft_length)

        # Update the image
        self._update_image_only()

    def _update_image_only(self):
        # Get the dynamic range from the form
        dynamic_range = float(self.dynamic_range.text())

        # Normalize the image
        a = abs(self.bp) / amax(abs(self.bp))

        xs = []
        ys = []
        zs = []
        rs = []

        # Find the points above the dynamic range
        for ix in range(self.nx):
            for iy in range(self.ny):
                for iz in range(self.nz):
                    if a[ix, iy, iz] > 10.0 ** (-dynamic_range / 20.0):
                        xs.append(self.x_image[ix, iy, iz])
                        ys.append(self.y_image[ix, iy, iz])
                        zs.append(self.z_image[ix, iy, iz])
                        rs.append(a[ix, iy, iz] * 10)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.scatter3D(xs, ys, zs, s=rs, cmap='Greys')
        self.axes1.grid(False)
        self.axes1.axis('off')
        #self.axes1.set_aspect('equal')
        set_equal(self.axes1)

        # Update the canvas
        self.my_canvas.draw()


def set_equal(ax):
    scaling = array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    ax.auto_scale_xyz(*[[min(scaling), max(scaling)]]*3)


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
