"""
Project: RadarBook
File: ducting_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.Ducting_ui import Ui_MainWindow
from Libs.wave_propagation import ducting
from numpy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Ducting(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.duct_thickness.returnPressed.connect(self._update_canvas)

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

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Set up the duct thickness
        duct_thickness = self.duct_thickness.text().split(',')
        dts = [float(x) for x in duct_thickness]

        # Set up the refractivity gradient
        refractivity_gradient = linspace(-500., -150., 1000)

        line_style = ['-', '--', '-.', ':', '-', '--', '-.', ':']

        # Calculate the critical angle for ducting
        i = 0
        for dt in dts:
            critical_angle = ducting.critical_angle(refractivity_gradient, dt)
            i += 1

            # Display the results
            self.axes1.plot(refractivity_gradient, critical_angle * 1e3, line_style[i-1], label="Thickness {} (m)".format(dt))

        # Set the plot title and labels
        self.axes1.set_title('Ducting over a Spherical Earth', size=14)
        self.axes1.set_xlabel('Refractivity Gradient (N/km)', size=12)
        self.axes1.set_ylabel('Critical Angle (mrad)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='best', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = Ducting(parent)  # Set the form
    form.show()       # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = Ducting()               # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
