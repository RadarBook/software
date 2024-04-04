"""
Project: RadarBook
File: apparent_elevation_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.ApparentElevation_ui import Ui_MainWindow
from Libs.wave_propagation import refraction
from numpy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApparentElevation(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.true_elevation.returnPressed.connect(self._update_canvas)
        self.height.returnPressed.connect(self._update_canvas)

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
        Update the figure when the user changes an input value
        :return:
        """
        # Get the height in km from the form and create an array of 100 values
        height = linspace(0, float(self.height.text()), 100)

        # Calculate the apparent elevation for each height value
        apparent_elevation = [refraction.apparent_elevation(float(self.true_elevation.text()), h) for h in height]

        # If using the approximate calculation uncomment these lines
        #kwargs = {'theta_true': float(self.true_elevation.text()), 'height': float(self.height.text())}
        #apparent_elevation_approximate = refraction.apparent_elevation_approximate(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(height, apparent_elevation)

        # Set the plot title and labels
        self.axes1.set_title('Apparent Elevation due to Refraction', size=14)
        self.axes1.set_xlabel('Height (km)', size=12)
        self.axes1.set_ylabel('Apparent Elevation Angle (degrees)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = ApparentElevation(parent)     # Set the form
    form.show()                    # Show the form


def main():
    app = QApplication(sys.argv)    # A new instance of QApplication
    form = ApparentElevation()      # Set the form
    form.show()                     # Show the form
    app.exec_()                     # Execute the app


if __name__ == '__main__':
    main()
