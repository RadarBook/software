"""
Project: RadarBook
File: loop_example.py
Created by: Lee A. Harrison
On: 7/28/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter03.ui.Loop_ui import Ui_MainWindow
from Libs.antenna.loop import small_loop, circular_loop
from numpy import linspace
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Loop(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.current.returnPressed.connect(self._update_canvas)
        self.radius.returnPressed.connect(self._update_canvas)
        self.antenna_type.currentIndexChanged.connect(self._update_canvas)

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
        Update the figure when the user changes an input value
        :return:
        """
        # Get the parameters from the form
        frequency = float(self.frequency.text())
        radius = float(self.radius.text())
        current = float(self.current.text())

        # Get the selected antenna from the form
        antenna_type = self.antenna_type.currentIndex()

        # Set the range and angular span
        r = 1.0e9
        theta = linspace(0.0, 2.0 * pi, 1000)

        # Get the antenna parameters and antenna pattern for the selected antenna
        if antenna_type == 0:
            total_power_radiated = small_loop.radiated_power(frequency, radius, current)
            radiation_resistance = small_loop.radiation_resistance(frequency, radius)
            beamwidth = small_loop.beamwidth()
            directivity = small_loop.directivity()
            maximum_effective_aperture = small_loop.maximum_effective_aperture(frequency)
            _, _, ep, _, _, _ = small_loop.far_field(frequency, radius, current, r, theta)
        else:
            total_power_radiated = circular_loop.radiated_power(frequency, radius, current)
            radiation_resistance = circular_loop.radiation_resistance(frequency, radius)
            beamwidth = circular_loop.beamwidth(frequency, radius)
            directivity = circular_loop.directivity(frequency, radius)
            maximum_effective_aperture = circular_loop.maximum_effective_aperture(frequency, radius)
            _, _, ep, _, _, _ = circular_loop.far_field(frequency, radius, current, r, theta)

        # Populate the form with the correct values
        self.total_radiated_power.setText('{:.2f}'.format(total_power_radiated))
        self.radiation_resistance.setText('{:.2f}'.format(radiation_resistance))
        self.beamwidth.setText('{:.2f}'.format(beamwidth))
        self.directivity.setText('{:.2f}'.format(directivity))
        self.maximum_effective_aperture.setText('{:.2e}'.format(maximum_effective_aperture))

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(theta, abs(ep), '')

        # Set the plot title and labels
        self.axes1.set_title('Loop Antenna Pattern', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = Loop(parent)  # Set the form
    form.show()    # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = Loop()                  # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
