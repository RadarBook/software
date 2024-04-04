"""
Project: RadarBook
File: plane_waves_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.PlaneWaves_ui import Ui_MainWindow
from Libs.wave_propagation import plane_waves
from numpy import linspace, exp, real
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PlaneWaves(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_results)
        self.relative_permittivity.returnPressed.connect(self._update_results)
        self.relative_permeability.returnPressed.connect(self._update_results)
        self.conductivity.returnPressed.connect(self._update_results)
        self.time.valueChanged.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.axes1 = fig.add_subplot(111)
        self.axes2 = self.axes1.twinx()
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the results when the user changes an input value.
        :return:
        """
        # Set up the key word args for the inputs
        kwargs = {'frequency':              float(self.frequency.text()),
                  'relative_permittivity':  float(self.relative_permittivity.text()),
                  'relative_permeability':  float(self.relative_permeability.text()),
                  'conductivity':           float(self.conductivity.text())}

        # Get the plane wave parameters
        propagation_constant, phase_constant, attenuation_constant, wave_impedance, skin_depth, wavelength, \
            phase_velocity = plane_waves.parameters(**kwargs)

        # Update the form with the results
        self.propagation_constant.setText('{:.3e}'.format(propagation_constant))
        self.phase_constant.setText('{:.3e}'.format(phase_constant))
        self.attenuation_constant.setText('{:.3e}'.format(attenuation_constant))
        self.wave_impedance.setText('{:.3e}'.format(wave_impedance))
        self.skin_depth.setText('{:.3e}'.format(skin_depth))
        self.wavelength.setText('{:.3e}'.format(wavelength))
        self.phase_velocity.setText('{:.3e}'.format(phase_velocity))

        # Update the figure
        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        # Determine 2 lambda distance for plotting
        wavelength = float(self.wavelength.text())
        z = linspace(0, 2.0 * wavelength, 1000)

        # Retrieve the parameters from the form
        gamma = complex(''.join(self.propagation_constant.text().split()))
        eta = complex(''.join(self.wave_impedance.text().split()))

        # Set up the angular frequency
        omega = 2.0 * pi * float(self.frequency.text())

        # Set up the time
        time = float(self.time.value()) / omega * 0.1

        # Calculate the electric and magnetic fields
        exp_term = exp(-gamma * z) * exp(1j * omega * time)
        Ex = real(exp_term)
        Hy = real(exp_term / eta)

        # Clear the axes for the updated plot
        self.axes1.clear()
        self.axes2.clear()

        # Display the fields
        self.axes1.plot(z, Ex, label='Electric Field')
        self.axes2.plot(z, Hy, 'r--', label='Magnetic Field')

        # Set the plot title and labels
        self.axes1.set_title('Uniform Plane Wave', size=14)
        self.axes1.set_xlabel('Distance (meters)', size=12)
        self.axes1.set_ylabel('Electric Field (V/m)', size=12)
        self.axes2.set_ylabel('Magnetic Field (A/m)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)
        self.axes2.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})
        self.axes2.legend(loc='upper right', bbox_to_anchor=(1.0, 0.925), prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = PlaneWaves(parent)  # Set the form
    form.show()          # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PlaneWaves()           # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
