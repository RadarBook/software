"""
Project: RadarBook
File: ovals_of_cassini_example.py
Created by: Lee A. Harrison
On: 7/2/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.OvalsOfCassini_ui import Ui_MainWindow
from numpy import linspace, log10, sqrt, sin, cos, imag, real
from scipy.constants import c, Boltzmann as k, pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class OvalsOfCassini(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.separation_distance.returnPressed.connect(self._update_canvas)
        self.system_temperature.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.noise_figure.returnPressed.connect(self._update_canvas)
        self.transmit_losses.returnPressed.connect(self._update_canvas)
        self.receive_losses.returnPressed.connect(self._update_canvas)
        self.peak_power.returnPressed.connect(self._update_canvas)
        self.transmit_antenna_gain.returnPressed.connect(self._update_canvas)
        self.receive_antenna_gain.returnPressed.connect(self._update_canvas)
        self.frequency.returnPressed.connect(self._update_canvas)
        self.bistatic_target_rcs.returnPressed.connect(self._update_canvas)

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
        # Get the values from the form
        separation_distance = float(self.separation_distance.text())
        system_temperature = float(self.system_temperature.text())
        bandwidth = float(self.bandwidth.text())
        noise_figure = 10 ** (float(self.noise_figure.text()) / 10)
        transmit_losses = 10 ** (float(self.transmit_losses.text()) / 10)
        receive_losses = 10 ** (float(self.receive_losses.text()) / 10)
        peak_power = float(self.peak_power.text())
        transmit_antenna_gain = 10 ** (float(self.transmit_antenna_gain.text()) / 10)
        receive_antenna_gain = 10 ** (float(self.receive_antenna_gain.text()) / 10)
        frequency = float(self.frequency.text())
        bistatic_target_rcs = 10 ** (float(self.bistatic_target_rcs.text()) / 10)

        # Number of points for plotting ovals
        number_of_points = 100000

        # Parameters for the Cassini ovals equation
        # r ^ 4 + a ^ 4 - 2 a ^ 2 r ^ 2(1 + cos(2 theta)) = b ^ 4

        # Parameter "a"
        a = 0.5 * separation_distance

        # Calculate the wavelength (m)
        wavelength = c / frequency

        # Calculate the bistatic radar range factor
        bistatic_range_factor = (peak_power * transmit_antenna_gain * receive_antenna_gain * wavelength ** 2 *
                                 bistatic_target_rcs) / ((4.0 * pi) ** 3 * k * system_temperature * bandwidth *
                                                         noise_figure * transmit_losses * receive_losses)

        # Full angle sweep
        t = linspace(0, 2.0 * pi, number_of_points)

        # Calculate the signal to noise ratio at which a = b
        SNR_0 = 10.0 * log10(16.0 * bistatic_range_factor / separation_distance ** 4)

        # Create the list of signal to noise ratios to plot
        SNR = [SNR_0 - 6, SNR_0 - 3, SNR_0, SNR_0 + 3]

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Loop over all the desired signal to noise ratios
        for s in SNR:

            # Convert to linear units
            snr = 10.0 ** (s / 10.0)

            # Parameter for Cassini ovals
            b = (bistatic_range_factor / snr) ** 0.25

            if a > b:

                # Calculate the +/- curves
                r1 = sqrt(a ** 2 * (cos(2.0 * t) + sqrt(cos(2 * t) ** 2 - 1.0 + (b / a) ** 4)))
                r2 = sqrt(a ** 2 * (cos(2.0 * t) - sqrt(cos(2 * t) ** 2 - 1.0 + (b / a) ** 4)))

                # Find the correct indices for imaginary parts = 0
                i1 = imag(r1) == 0
                i2 = imag(r2) == 0

                r1 = real(r1)
                r2 = real(r2)

                # Plot both parts of the curve
                label_text = "SNR = {:.1f}".format(s)
                self.axes1.plot(r1[i1] * cos(t[i1]) / 1e3, r1[i1] * sin(t[i1]) / 1e3, 'k.', label=label_text)
                self.axes1.plot(r2[i2] * cos(t[i2]) / 1e3, r2[i2] * sin(t[i2]) / 1e3, 'k.')

            else:

                # Calculate the range for the continuous curves
                r = sqrt(a**2 * cos(2 * t) + sqrt(b ** 4 - a ** 4 * sin(2.0 * t) ** 2))

                # Plot the continuous parts
                label_text = "SNR = {:.1f}".format(s)
                self.axes1.plot(r * cos(t) / 1e3, r * sin(t) / 1e3, '.', label=label_text)

            # Add the text for Tx/Rx locations
            self.axes1.text(-a / 1e3, 0, 'Tx')
            self.axes1.text(a / 1e3, 0, 'Rx')

            # Set the plot title and labels
            self.axes1.set_title('Ovals of Cassini', size=14)
            self.axes1.set_xlabel('Range (km)', size=12)
            self.axes1.set_ylabel('Range (km)', size=12)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Add the legend
            self.axes1.legend(loc='upper left', prop={'size': 10})

            # Update the canvas
            self.my_canvas.draw()


def start():
    form = OvalsOfCassini()  # Set the form
    form.show()              # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = OvalsOfCassini()       # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
