"""
Project: RadarBook
File: power_density_example.py
Created by: Lee A. Harrison
On: 6/30/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.PowerDensity_ui import Ui_MainWindow
from Libs.radar_range import radar_range
from scipy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PowerDensity(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.target_min_range.returnPressed.connect(self._update_canvas)
        self.target_max_range.returnPressed.connect(self._update_canvas)
        self.antenna_gain.returnPressed.connect(self._update_canvas)

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
        # Get the range from the form
        target_min_range = float(self.target_min_range.text())
        target_max_range = float(self.target_max_range.text())

        # Set up the range array
        target_range = linspace(target_min_range, target_max_range, 2000)

        # Convert the antenna gain to linear units
        antenna_gain = 10.0 ** (float(self.antenna_gain.text()) / 10.0)

        # Set up the input args
        kwargs = {'target_range': target_range,
                  'peak_power': float(self.peak_power.text()),
                  'antenna_gain': antenna_gain}

        # Calculate the power density at the target
        power_density = radar_range.power_density(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(target_range / 1.0e3, power_density, '')

        # Set the plot title and labels
        self.axes1.set_title('Power Density at the Target', size=14)
        self.axes1.set_xlabel('Target Range (km)', size=12)
        self.axes1.set_ylabel('Power Density (W/m$^2$)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = PowerDensity()  # Set the form
    form.show()            # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PowerDensity()         # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
