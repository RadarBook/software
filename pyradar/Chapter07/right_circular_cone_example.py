"""
Project: RadarBook
File: right_circular_cone_example.py
Created by: Lee A. Harrison
On: 11/24/2018
Created with: PyCharm
"""
import sys
from Chapter07.ui.RightCircularCone_ui import Ui_MainWindow
from scipy import log10, linspace, array, degrees, radians, pi
from Libs.rcs.right_circular_cone import radar_cross_section
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class RightCone(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.cone_half_angle.returnPressed.connect(self._update_canvas)
        self.base_radius.returnPressed.connect(self._update_canvas)

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
        cone_half_angle = radians(float(self.cone_half_angle.text()))
        base_radius = float(self.base_radius.text())

        # Set the incident angles
        incident_angle = linspace(0, pi, 1801)

        # Calculate the radar cross section
        rcs = array([radar_cross_section(frequency, cone_half_angle, base_radius, ia) for ia in incident_angle])

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(degrees(incident_angle), 10 * log10(rcs[:, 0]), '', label='VV')
        self.axes1.plot(degrees(incident_angle), 10 * log10(rcs[:, 1]), '--', label='HH')

        # Set the plot title and labels
        self.axes1.set_title('RCS vs Incident Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Incident Angle (deg)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = RightCone()  # Set the form
    form.show()         # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = RightCone()            # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
