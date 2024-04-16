"""
Project: RadarBook
File: rectangular_plate_example.py
Created by: Lee A. Harrison
On: 11/23/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter07.ui.RectangularPlate_ui import Ui_MainWindow
from numpy import log10, linspace
from Libs.rcs.rectangular_plate import radar_cross_section
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class RectPlate(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.width.returnPressed.connect(self._update_canvas)
        self.length.returnPressed.connect(self._update_canvas)
        self.incident_theta.returnPressed.connect(self._update_canvas)
        self.observation_phi.returnPressed.connect(self._update_canvas)

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
        width = float(self.width.text())
        length = float(self.length.text())
        incident_theta = float(self.incident_theta.text())
        observation_phi = float(self.observation_phi.text())

        # Set the observation angles
        observation_theta = linspace(-90, 90, 1801)

        # Calculate the radar cross section
        rcs_tm, rcs_te = radar_cross_section(frequency, width, length, incident_theta, observation_theta,
                                             observation_phi)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(observation_theta, 10.0 * log10(rcs_te + 1e-10), '', label='TE$^x$')
        self.axes1.plot(observation_theta, 10.0 * log10(rcs_tm + 1e-10), '--', label='TM$^x$')

        # Set the plot title and labels
        self.axes1.set_title('RCS vs Bistatic Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Observation Angle (deg)', size=12)
        self.axes1.set_ylim(min(10.0 * log10(rcs_te + 1e-4)) - 3, max(10.0 * log10(rcs_te + 1e-4)) + 3)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = RectPlate(parent)  # Set the form
    form.show()         # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = RectPlate()            # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
