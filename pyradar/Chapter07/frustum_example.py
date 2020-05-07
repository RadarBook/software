"""
Project: RadarBook
File: frustum_example.py
Created by: Lee A. Harrison
On: 11/24/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter07.ui.Frustum_ui import Ui_MainWindow
from numpy import log10, linspace, array, degrees, pi
from Libs.rcs.frustum import radar_cross_section
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Frustum(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.nose_radius.returnPressed.connect(self._update_canvas)
        self.base_radius.returnPressed.connect(self._update_canvas)
        self.length.returnPressed.connect(self._update_canvas)

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
        frequency = float(self.frequency.text())
        nose_radius = float(self.nose_radius.text())
        base_radius = float(self.base_radius.text())
        length = float(self.length.text())

        # Set the incident angles
        incident_angle = linspace(0, pi, 1801)

        # Calculate the radar cross section
        rcs = array([radar_cross_section(frequency, nose_radius, base_radius, length, ia) for ia in incident_angle])

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(degrees(incident_angle), 10 * log10(rcs), '')

        # Set the plot title and labels
        self.axes1.set_title('RCS vs Incident Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Incident Angle (deg)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Frustum()  # Set the form
    form.show()       # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Frustum()              # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
