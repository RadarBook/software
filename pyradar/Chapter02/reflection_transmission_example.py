"""
Project: RadarBook
File: reflection_transmission_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.ReflectionTransmission_ui import Ui_MainWindow
from Libs.wave_propagation import plane_waves
from numpy import linspace, array, degrees
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ReflectionTransmission(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_results)
        self.relative_permittivity_1.returnPressed.connect(self._update_results)
        self.relative_permeability_1.returnPressed.connect(self._update_results)
        self.conductivity_1.returnPressed.connect(self._update_results)
        self.relative_permittivity_2.returnPressed.connect(self._update_results)
        self.relative_permeability_2.returnPressed.connect(self._update_results)
        self.conductivity_2.returnPressed.connect(self._update_results)

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
        # Get the parameters from the form
        self.relative_permittivity = array([float(self.relative_permittivity_1.text()),
                                             float(self.relative_permittivity_2.text())])

        self.relative_permeability = array([float(self.relative_permeability_1.text()),
                                       float(self.relative_permeability_2.text())])

        self.conductivity = array([float(self.conductivity_1.text()), float(self.conductivity_2.text())])

        # Set up the key word args for the inputs
        kwargs = {'frequency':              float(self.frequency.text()),
                  'relative_permittivity':  self.relative_permittivity,
                  'relative_permeability':  self.relative_permeability,
                  'conductivity':           self.conductivity}

        # Calculate the critical and Brewster angles
        critical_angle = plane_waves.critical_angle(**kwargs)
        brewster_angle = plane_waves.brewster_angle(**kwargs)

        # Update the form with the results
        self.critical_angle.setText('{:.1f}'.format(critical_angle))
        self.brewster_angle.setText('{:.1f}'.format(brewster_angle))

        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        # Set up the incident angles
        incident_angle = linspace(0., 0.5 * pi, 1000)

        # Set up the keyword args
        kwargs = {'frequency': float(self.frequency.text()),
                  'incident_angle': incident_angle,
                  'relative_permittivity': self.relative_permittivity,
                  'relative_permeability': self.relative_permeability,
                  'conductivity': self.conductivity}

        # Calculate the reflection and transmission coefficients
        reflection_coefficient_te, transmission_coefficient_te, reflection_coefficient_tm, \
        transmission_coefficient_tm = plane_waves.reflection_transmission(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()
        self.axes2.clear()

        # Display the reflection coefficients
        self.axes1.plot(degrees(incident_angle), abs(reflection_coefficient_te), 'b', label='|$\Gamma_{TE}$|')
        self.axes1.plot(degrees(incident_angle), abs(reflection_coefficient_tm), 'b--', label='|$\Gamma_{TM}$|')

        # Display the transmission coefficients
        self.axes2.plot(degrees(incident_angle), abs(transmission_coefficient_te), 'r', label='|$T_{TE}$|')
        self.axes2.plot(degrees(incident_angle), abs(transmission_coefficient_tm), 'r--', label='|$T_{TM}$|')

        # Set the plot title and labels
        self.axes1.set_title('Plane Wave Reflection and Transmission', size=14)
        self.axes1.set_xlabel('Incident Angle (degrees)', size=12)
        self.axes1.set_ylabel('|Reflection Coefficient|', size=12)
        self.axes2.set_ylabel('|Transmission Coefficient|', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)
        self.axes2.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})
        self.axes2.legend(loc='upper left', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = ReflectionTransmission()  # Set the form
    form.show()                      # Show the form


def main():
    app = QApplication(sys.argv)     # A new instance of QApplication
    form = ReflectionTransmission()  # Set the form
    form.show()                      # Show the form
    app.exec_()                      # Execute the app


if __name__ == '__main__':
    main()
