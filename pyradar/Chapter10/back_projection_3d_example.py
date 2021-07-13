"""
Project: RadarBook
File: back_projection_3d_example.py
Created by: Lee A. Harrison
On: 2/18/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter10.ui.BackProjection3pt_ui import Ui_MainWindow
from numpy import linspace, meshgrid, array, sqrt, radians, sin, cos, zeros, dot, exp, amax, ones
from scipy.fftpack import next_fast_len
from scipy.constants import c, pi
from scipy.signal.windows import hanning, hamming
from numpy import max, min
from Libs.sar import backprojection
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
        self.x_target.returnPressed.connect(self._update_canvas)
        self.y_target.returnPressed.connect(self._update_canvas)
        self.z_target.returnPressed.connect(self._update_canvas)
        self.rcs.returnPressed.connect(self._update_canvas)
        self.x_span.returnPressed.connect(self._update_canvas)
        self.y_span.returnPressed.connect(self._update_canvas)
        self.z_span.returnPressed.connect(self._update_canvas)
        self.nx_ny_nz.returnPressed.connect(self._update_canvas)
        self.start_frequency.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.az_start_end.returnPressed.connect(self._update_canvas)
        self.el_start_end.returnPressed.connect(self._update_canvas)
        self.dynamic_range.returnPressed.connect(self._update_image_only)
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
        x_target = self.x_target.text().split(',')
        y_target = self.y_target.text().split(',')
        z_target = self.z_target.text().split(',')
        rcs = self.rcs.text().split(',')
        xt = []
        yt = []
        zt = []
        rt = []
        for x, y, z, r in zip(x_target, y_target, z_target, rcs):
            xt.append(float(x))
            yt.append(float(y))
            zt.append(float(z))
            rt.append(float(r))

        x_span = float(self.x_span.text())
        y_span = float(self.y_span.text())
        z_span = float(self.z_span.text())

        nx_ny_nz = self.nx_ny_nz.text().split(',')
        self.nx = int(nx_ny_nz[0])
        self.ny = int(nx_ny_nz[1])
        self.nz = int(nx_ny_nz[2])

        start_frequency = float(self.start_frequency.text())
        bandwidth = float(self.bandwidth.text())

        az_start_end = self.az_start_end.text().split(',')
        az_start = float(az_start_end[0])
        az_end = float(az_start_end[1])

        el_start_end = self.el_start_end.text().split(',')
        el_start = float(el_start_end[0])
        el_end = float(el_start_end[1])

        # Set up the azimuth space
        r = sqrt(x_span ** 2 + y_span ** 2)
        da = c / (2.0 * r * start_frequency)
        na = int(radians(az_end - az_start) / da)
        az = linspace(az_start, az_end, na)

        # Set up the elevation space
        r = sqrt(x_span ** 2 + z_span ** 2)
        de = c / (2.0 * r * start_frequency)
        ne = int(radians(el_end - el_start) / de)
        el = linspace(el_start, el_end, ne)

        # Set up the angular grid
        az_grid, el_grid = meshgrid(az, el)

        # Set up the frequency space
        df = c / (2.0 * r)
        nf = int(bandwidth / df)
        frequency = linspace(start_frequency, start_frequency + bandwidth, nf)

        # Set the length of the FFT
        fft_length = next_fast_len(4 * nf)

        # Set up the image space
        xi = linspace(-0.5 * x_span, 0.5 * x_span, self.nx)
        yi = linspace(-0.5 * y_span, 0.5 * y_span, self.ny)
        zi = linspace(-0.5 * z_span, 0.5 * z_span, self.nz)
        self.x_image, self.y_image, self.z_image = meshgrid(xi, yi, zi, indexing='ij')

        signal = zeros([nf, ne, na], dtype=complex)

        # Calculate the signal (k space)
        i1 = 0
        for a in az:
            i2 = 0
            for e in el:
                r_los = [cos(radians(e)) * cos(radians(a)), cos(radians(e)) * sin(radians(a)), sin(radians(e))]
                for x, y, z, r in zip(xt, yt, zt, rt):
                    r_target = dot(r_los, [x, y, z])
                    signal[:, i2, i1] += r * exp(-1j * 4.0 * pi * frequency / c * r_target)
                i2 += 1
            i1 += 1

        # Get the selected window from the form
        window_type = self.window_type.currentText()

        coefficients = ones([nf, ne, na])

        if window_type == 'Hanning':
            h1 = hanning(nf, True)
            h2 = hanning(na, True)
            h3 = hanning(ne, True)

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

        # Apply the selected window
        signal *= coefficients

        # Reconstruct the image
        self.bp = backprojection.reconstruct3(signal, radians(az_grid), radians(el_grid),
                                              self.x_image, self.y_image, self.z_image, frequency, fft_length)

        # Update the image
        self._update_image_only()

    def _update_image_only(self):
        dynamic_range = float(self.dynamic_range.text())

        a = abs(self.bp) / amax(abs(self.bp))

        xs = []
        ys = []
        zs = []
        rs = []

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
        self.axes1.scatter(xs, ys, zs, s=rs, cmap='Greys')
        #self.axes1.set_aspect('equal')
        set_equal(self.axes1)

        # Set the plot title and labels
        self.axes1.set_title('Back Projection', size=14)
        self.axes1.set_xlabel('X (m)', size=12)
        self.axes1.set_ylabel('Y (m)', size=12)
        self.axes1.set_zlabel('Z (m)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def set_equal(ax):
    scaling = array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    ax.auto_scale_xyz(*[[min(scaling), max(scaling)]]*3)


def start():
    form = BackProjection()  # Set the form
    form.show()              # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = BackProjection()       # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
