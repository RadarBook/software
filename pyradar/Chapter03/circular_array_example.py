"""
Project: RadarBook
File: circular_array_example.py
Created by: Lee A. Harrison
On: 8/1/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter03.ui.CircularArray_ui import Ui_MainWindow
from Libs.antenna.array import circular_uniform
from scipy import linspace, radians, degrees, log10, sin, cos, meshgrid
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class CircularArray(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.number_of_elements.returnPressed.connect(self._update_canvas)
        self.scan_angle_theta.returnPressed.connect(self._update_canvas)
        self.scan_angle_phi.returnPressed.connect(self._update_canvas)
        self.radius.returnPressed.connect(self._update_canvas)
        self.plot_type.currentIndexChanged.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.fig = fig
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
        # Get the parameters from the form
        frequency = float(self.frequency.text())
        number_of_elements = int(self.number_of_elements.text())
        scan_angle_theta = float(self.scan_angle_theta.text())
        scan_angle_phi = float(self.scan_angle_phi.text())
        radius = float(self.radius.text())

        # Set up the theta and phi arrays
        n = 360
        m = int(n / 8)
        theta, phi = meshgrid(linspace(0.0 * pi, 0.5 * pi, n), linspace(0.0, 2.0 * pi, n))

        # Set up the args
        kwargs = {'number_of_elements': number_of_elements,
                  'scan_angle_theta': radians(scan_angle_theta),
                  'scan_angle_phi': radians(scan_angle_phi),
                  'radius': radius,
                  'frequency': frequency,
                  'theta': theta,
                  'phi': phi}

        # Get the array factor
        af = circular_uniform.array_factor(**kwargs)

        # Remove the color bar
        try:
            self.cbar.remove()
        except:
            # Initial plot
            pass

        # Clear the axes for the updated plot
        self.axes1.clear()

        # U-V coordinates for plotting the antenna pattern
        uu = sin(theta) * cos(phi)
        vv = sin(theta) * sin(phi)

        if self.plot_type.currentIndex() == 0:

            # Display the results
            im = self.axes1.pcolor(uu, vv, abs(af), cmap="jet")
            self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
            self.cbar.set_label("Normalized Electric Field (V/m)", size=10)

            # Set the x- and y-axis labels
            self.axes1.set_xlabel("U (sines)", size=12)
            self.axes1.set_ylabel("V (sines)", size=12)

        elif self.plot_type.currentIndex() == 1:

            # Create the contour plot
            self.axes1.contour(uu, vv, abs(af), 20, cmap="jet", vmin=-0.2, vmax=1.0)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Set the x- and y-axis labels
            self.axes1.set_xlabel("U (sines)", size=12)
            self.axes1.set_ylabel("V (sines)", size=12)

        else:

            # Create the line plot
            self.axes1.plot(degrees(theta[0]), 20.0 * log10(abs(af[m])), '', label='E Plane')
            self.axes1.plot(degrees(theta[0]), 20.0 * log10(abs(af[0])), '--', label='H Plane')

            # Set the y axis limit
            self.axes1.set_ylim(-60, 5)

            # Set the x and y axis labels
            self.axes1.set_xlabel("Theta (degrees)", size=12)
            self.axes1.set_ylabel("Array Factor (dB)", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Place the legend
            self.axes1.legend(loc='upper right', prop={'size': 10})

        # Set the plot title and labels
        self.axes1.set_title('Circular Array - Array Factor', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = CircularArray()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = CircularArray()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
