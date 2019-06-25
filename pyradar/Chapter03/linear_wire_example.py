"""
Project: RadarBook
File: linear_wire_example.py
Created by: Lee A. Harrison
On: 7/28/2018
Created with: PyCharm
"""
import sys
from Chapter03.ui.LinearWire_ui import Ui_MainWindow
from Libs.antenna.linear_wire import finite_length_dipole, infinitesimal_dipole, small_dipole
from scipy import linspace, finfo
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class LinearWire(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.current.returnPressed.connect(self._update_canvas)
        self.length.returnPressed.connect(self._update_canvas)
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
        length = float(self.length.text())
        current = float(self.current.text())

        # Get the selected antenna from the form
        antenna_type = self.antenna_type.currentIndex()

        # Set the range and angular span
        r = 1.0e9
        theta = linspace(finfo(float).eps, 2.0 * pi, 1000)

        # Get the antenna parameters and antenna pattern for the selected antenna
        if antenna_type == 0:
            total_power_radiated = infinitesimal_dipole.radiated_power(frequency, length, current)
            radiation_resistance = infinitesimal_dipole.radiation_resistance(frequency, length)
            beamwidth = infinitesimal_dipole.beamwidth()
            directivity = infinitesimal_dipole.directivity()
            maximum_effective_aperture = infinitesimal_dipole.maximum_effective_aperture(frequency)
            _, et, _, _, _, _ = infinitesimal_dipole.far_field(frequency, length, current, r, theta)
        elif antenna_type == 1:
            total_power_radiated = small_dipole.radiated_power(frequency, length, current)
            radiation_resistance = small_dipole.radiation_resistance(frequency, length)
            beamwidth = small_dipole.beamwidth()
            directivity = small_dipole.directivity()
            maximum_effective_aperture = small_dipole.maximum_effective_aperture(frequency)
            _, et, _, _, _, _ = small_dipole.far_field(frequency, length, current, r, theta)
        else:
            total_power_radiated = finite_length_dipole.radiated_power(frequency, length, current)
            radiation_resistance = finite_length_dipole.radiation_resistance(frequency, length)
            beamwidth = finite_length_dipole.beamwidth(frequency, length)
            directivity = finite_length_dipole.directivity(frequency, length, current)
            maximum_effective_aperture = finite_length_dipole.maximum_effective_aperture(frequency, length, current)
            _, et, _, _, _, _ = finite_length_dipole.far_field(frequency, length, current, r, theta)

        # Populate the form with the correct values
        self.total_radiated_power.setText('{:.2f}'.format(total_power_radiated))
        self.radiation_resistance.setText('{:.2f}'.format(radiation_resistance))
        self.beamwidth.setText('{:.2f}'.format(beamwidth))
        self.directivity.setText('{:.2f}'.format(directivity))
        self.maximum_effective_aperture.setText('{:.2f}'.format(maximum_effective_aperture))

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(theta, abs(et), '')

        # Set the plot title and labels
        self.axes1.set_title('Linear Wire Antenna Pattern', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = LinearWire()  # Set the form
    form.show()          # Show the form


def main():
    app = QApplication(sys.argv)        # A new instance of QApplication
    form = LinearWire()                 # Set the form
    form.show()                         # Show the form
    app.exec_()                         # Execute the app


if __name__ == '__main__':
    main()
