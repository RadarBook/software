"""
Project: RadarBook
File: hertzian_dipole_example.py
Created by: Lee A. Harrison
On: 6/29/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.HertzianDipole_ui import Ui_MainWindow
from Libs.radar_range import hertzian_dipole
from scipy import linspace, pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class HertzianDipole(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.relative_permittivity.returnPressed.connect(self._update_canvas)
        self.relative_permeability.returnPressed.connect(self._update_canvas)
        self.frequency.returnPressed.connect(self._update_canvas)
        self.current.returnPressed.connect(self._update_canvas)
        self.length.returnPressed.connect(self._update_canvas)
        self.r.returnPressed.connect(self._update_canvas)
        self.electric_field_button.clicked.connect(self._update_canvas)
        self.magnetic_field_button.clicked.connect(self._update_canvas)
        self.power_density_button.clicked.connect(self._update_canvas)
        self.radiation_intensity_button.clicked.connect(self._update_canvas)
        self.directivity_button.clicked.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.axes1 = fig.add_subplot(111, projection='polar')
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
        # Set the angle to be from 0 to 2 pi
        theta = linspace(0, 2.0 * pi, 256)

        # For the electric field
        if self.electric_field_button.isChecked():

            # Set up the key word args for the inputs
            kwargs = {'relative_permittivity': float(self.relative_permittivity.text()),
                      'relative_permeability': float(self.relative_permeability.text()),
                      'frequency': float(self.frequency.text()),
                      'current': float(self.current.text()),
                      'length': float(self.length.text()),
                      'r': float(self.r.text()),
                      'theta': theta}

            # Get the electric field
            electric_field = hertzian_dipole.electric_field(**kwargs)

            # Clear the axes for the updated plot
            self.axes1.clear()

            # Display the results
            self.axes1.plot(theta, abs(electric_field), '')

            # Set the plot title and labels
            self.axes1.set_title('Hertzian Dipole Electric Field (V/m)', size=14)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Update the canvas
            self.my_canvas.draw()

        # For the magnetic field
        elif self.magnetic_field_button.isChecked():
            # Set up the key word args for the inputs
            kwargs = {'frequency': float(self.frequency.text()),
                      'current': float(self.current.text()),
                      'length': float(self.length.text()),
                      'r': float(self.r.text()),
                      'theta': theta}

            # Get the magnetic field
            magnetic_field = hertzian_dipole.magnetic_field(**kwargs)

            # Clear the axes for the updated plot
            self.axes1.clear()

            # Display the results
            self.axes1.plot(theta, abs(magnetic_field), '')

            # Set the plot title and labels
            self.axes1.set_title('Hertzian Dipole Magnetic Field (A/m)', size=14)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Update the canvas
            self.my_canvas.draw()

        # For the power density
        elif self.power_density_button.isChecked():
            # Set up the key word args for the inputs
            kwargs = {'relative_permittivity': float(self.relative_permittivity.text()),
                      'relative_permeability': float(self.relative_permeability.text()),
                      'frequency': float(self.frequency.text()),
                      'current': float(self.current.text()),
                      'length': float(self.length.text()),
                      'r': float(self.r.text()),
                      'theta': theta}

            # Get the power density
            power_density = hertzian_dipole.power_density(**kwargs)

            # Clear the axes for the updated plot
            self.axes1.clear()

            # Display the results
            self.axes1.plot(theta, power_density, '')

            # Set the plot title and labels
            self.axes1.set_title('Hertzian Dipole Power Density (W/m$^2$)', size=14)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Update the canvas
            self.my_canvas.draw()

        # For the radiation intensity
        elif self.radiation_intensity_button.isChecked():
            # Set up the key word args for the inputs
            kwargs = {'relative_permittivity': float(self.relative_permittivity.text()),
                      'relative_permeability': float(self.relative_permeability.text()),
                      'frequency': float(self.frequency.text()),
                      'current': float(self.current.text()),
                      'length': float(self.length.text()),
                      'theta': theta}

            # Get the radiation intensity
            radiation_intensity = hertzian_dipole.radiation_intensity(**kwargs)

            # Clear the axes for the updated plot
            self.axes1.clear()

            # Display the results
            self.axes1.plot(theta, radiation_intensity, '')

            # Set the plot title and labels
            self.axes1.set_title('Hertzian Dipole Radiation Intensity', size=14)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Update the canvas
            self.my_canvas.draw()

        # For the directivity
        elif self.directivity_button.isChecked():
            # Set up the key word args for the inputs
            kwargs = {'relative_permittivity': float(self.relative_permittivity.text()),
                      'relative_permeability': float(self.relative_permeability.text()),
                      'frequency': float(self.frequency.text()),
                      'current': float(self.current.text()),
                      'length': float(self.length.text()),
                      'theta': theta}

            # Get the directivity
            directivity = hertzian_dipole.directivity(**kwargs)

            # Clear the axes for the updated plot
            self.axes1.clear()

            # Display the results
            self.axes1.plot(theta, directivity, '')

            # Set the plot title and labels
            self.axes1.set_title('Hertzian Dipole Directivity', size=14)

            # Set the tick label size
            self.axes1.tick_params(labelsize=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Update the canvas
            self.my_canvas.draw()

        # Update the total radiated power
        # Set up the key word args for the inputs
        kwargs = {'relative_permittivity': float(self.relative_permittivity.text()),
                  'relative_permeability': float(self.relative_permeability.text()),
                  'frequency': float(self.frequency.text()),
                  'current': float(self.current.text()),
                  'length': float(self.length.text())}

        total_radiated_power = hertzian_dipole.total_radiated_power(**kwargs)
        self.total_radiated_power.setText('{:.3e}'.format(total_radiated_power))


def start():
    form = HertzianDipole()        # Set the form
    form.show()                    # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = HertzianDipole()        # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
