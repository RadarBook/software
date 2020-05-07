"""
Project: RadarBook
File: horn_example.py
Created by: Lee A. Harrison
On: 7/30/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter03.ui.Horn_ui import Ui_MainWindow
from Libs.antenna.horn import e_plane_sectoral, h_plane_sectoral, pyramidal
from numpy import linspace, meshgrid, log10, sin, cos, amax, sqrt, degrees
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Horn(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.guide_width.returnPressed.connect(self._update_canvas)
        self.guide_height.returnPressed.connect(self._update_canvas)
        self.horn_width.returnPressed.connect(self._update_canvas)
        self.horn_height.returnPressed.connect(self._update_canvas)
        self.eplane_effective_length.returnPressed.connect(self._update_canvas)
        self.hplane_effective_length.returnPressed.connect(self._update_canvas)
        self.antenna_type.currentIndexChanged.connect(self._update_canvas)
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
        guide_width = float(self.guide_width.text())
        guide_height = float(self.guide_height.text())
        horn_width = float(self.horn_width.text())
        horn_height = float(self.horn_height.text())
        eplane_effective_length = float(self.eplane_effective_length.text())
        hplane_effective_length = float(self.hplane_effective_length.text())

        # Get the selected antenna from the form
        antenna_type = self.antenna_type.currentIndex()

        # Set the range and angular span
        r = 1.0e9

        # Set up the theta and phi arrays
        n = 400
        m = int(n/4)
        theta, phi = meshgrid(linspace(0.0, 0.5 * pi, n), linspace(0.0, 2.0 * pi, n))

        # Get the antenna parameters and antenna pattern for the selected antenna
        if antenna_type == 0:
            total_power_radiated = e_plane_sectoral.power_radiated(guide_width, horn_height)
            directivity = e_plane_sectoral.directivity(guide_width, horn_height, eplane_effective_length, frequency)
            _, et, ep, _, _, _ = e_plane_sectoral.far_fields(guide_width, horn_height, eplane_effective_length,
                                                             frequency, r, theta, phi)
        elif antenna_type == 1:
            total_power_radiated = h_plane_sectoral.power_radiated(guide_height, horn_width)
            directivity = h_plane_sectoral.directivity(guide_height, horn_width, hplane_effective_length, frequency)
            _, et, ep, _, _, _ = h_plane_sectoral.far_fields(guide_height, horn_width, hplane_effective_length,
                                                             frequency, r, theta, phi)
        else:
            total_power_radiated = pyramidal.power_radiated(horn_width, horn_height)
            directivity = pyramidal.directivity(horn_width, horn_height, eplane_effective_length,
                                                hplane_effective_length, frequency)
            _, et, ep, _, _, _ = pyramidal.far_fields(horn_width, horn_height, eplane_effective_length,
                                                      hplane_effective_length, frequency, r, theta, phi)

        # Populate the form with the correct values
        self.total_radiated_power.setText('{:.2e}'.format(total_power_radiated))
        self.directivity.setText('{:.2f}'.format(directivity))

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

        # Normalized electric field magnitude for plotting
        e_mag = sqrt(abs(et * et + ep * ep))
        e_mag /= amax(e_mag)

        if self.plot_type.currentIndex() == 0:

            # Display the results
            im = self.axes1.pcolor(uu, vv, e_mag, cmap="jet")
            self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
            self.cbar.set_label("Normalized Electric Field(V/m)", size=10)

            # Set the x- and y-axis labels
            self.axes1.set_xlabel("U (sines)", size=12)
            self.axes1.set_ylabel("V (sines)", size=12)

        elif self.plot_type.currentIndex() == 1:

            # Create the contour plot
            self.axes1.contour(uu, vv, e_mag, 20, cmap="jet", vmin=-0.2, vmax=1.0)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Set the x- and y-axis labels
            self.axes1.set_xlabel("U (sines)", size=12)
            self.axes1.set_ylabel("V (sines)", size=12)

        else:

            # Create the line plot
            self.axes1.plot(degrees(theta[0]), 20.0 * log10(e_mag[m]), '', label='E Plane')
            self.axes1.plot(degrees(theta[0]), 20.0 * log10(e_mag[0]), '--', label='H Plane')

            # Set the y axis limit
            self.axes1.set_ylim(-40, 5)

            # Set the x and y axis labels
            self.axes1.set_xlabel("Theta (degrees)", size=12)
            self.axes1.set_ylabel("Normalized |E| (dB)", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

            # Place the legend
            self.axes1.legend(loc='upper right', prop={'size': 10})

        # Set the plot title and labels
        self.axes1.set_title('Horn Antenna Pattern', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Horn()  # Set the form
    form.show()    # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Horn()                 # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
