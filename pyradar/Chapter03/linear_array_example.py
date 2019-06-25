"""
Project: RadarBook
File: linear_array_example.py
Created by: Lee A. Harrison
On: 7/31/2018
Created with: PyCharm
"""
import sys
from Chapter03.ui.LinearArray_ui import Ui_MainWindow
from Libs.antenna.array import linear_array
from scipy import linspace, radians, degrees, log10, finfo
from scipy.constants import pi
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class LinearArray(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.number_of_elements.returnPressed.connect(self._update_canvas)
        self.scan_angle.returnPressed.connect(self._update_canvas)
        self.element_spacing.returnPressed.connect(self._update_canvas)
        self.side_lobe_level.returnPressed.connect(self._update_canvas)
        self.antenna_type.currentIndexChanged.connect(self._update_canvas)

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
        scan_angle = float(self.scan_angle.text())
        element_spacing = float(self.element_spacing.text())
        side_lobe_level = float(self.side_lobe_level.text())

        # Get the selected antenna from the form
        antenna_type = self.antenna_type.currentText()

        # Set the angular span
        theta = linspace(0.0, pi, 1000)

        # Set up the args
        kwargs = {'number_of_elements': number_of_elements,
                  'scan_angle': radians(scan_angle),
                  'element_spacing': element_spacing,
                  'frequency': frequency,
                  'theta': theta,
                  'window_type': antenna_type,
                  'side_lobe_level': side_lobe_level}

        # Get the array factor
        af = linear_array.array_factor(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Create the line plot
        self.axes1.plot(degrees(theta), 20.0 * log10(abs(af) + finfo(float).eps), '')

        # Set the y axis limit
        self.axes1.set_ylim(-80, 5)

        # Set the x and y axis labels
        self.axes1.set_xlabel("Theta (degrees)", size=12)
        self.axes1.set_ylabel("Array Factor (dB)", size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('Linear Array Antenna Pattern', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = LinearArray()  # Set the form
    form.show()           # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = LinearArray()          # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
