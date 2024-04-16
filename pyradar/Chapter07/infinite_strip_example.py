"""
Project: RadarBook
File: infinite_strip_example.py
Created by: Lee A. Harrison
On: 11/21/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter07.ui.InfiniteStrip_ui import Ui_MainWindow
from numpy import log10, linspace
from Libs.rcs.infinite_strip import radar_cross_section
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class InfStrip(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.incident_angle.returnPressed.connect(self._update_canvas)
        self.frequency.returnPressed.connect(self._update_canvas)
        self.width.returnPressed.connect(self._update_canvas)

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
        # Get the parameters from the form
        incident_angle = float(self.incident_angle.text())
        frequency = float(self.frequency.text())
        width = float(self.width.text())

        # Set the observation angles
        observation_angle = linspace(0, 180, 1801)

        # Calculate the radar cross section
        rcs_tm, rcs_te = radar_cross_section(frequency, width, incident_angle, observation_angle)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(observation_angle, 10 * log10(rcs_te + 1e-10), '', label='TE$^z$')
        self.axes1.plot(observation_angle, 10 * log10(rcs_tm + 1e-10), '--', label='TM$^z$')

        # Set the plot title and labels
        self.axes1.set_title('RCS vs Bistatic Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Observation Angle (deg)', size=12)
        self.axes1.set_ylim(min(10 * log10(rcs_te + 1e-4)) - 3, max(10 * log10(rcs_te + 1e-4)) + 3)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = InfStrip(parent)  # Set the form
    form.show()        # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = InfStrip()             # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
