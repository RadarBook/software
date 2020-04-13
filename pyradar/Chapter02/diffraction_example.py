"""
Project: RadarBook
File: diffraction_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.Diffraction_ui import Ui_MainWindow
from Libs.wave_propagation import diffraction
from scipy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Diffraction(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency_start.returnPressed.connect(self._update_canvas)
        self.frequency_end.returnPressed.connect(self._update_canvas)
        self.relative_permittivity.returnPressed.connect(self._update_canvas)
        self.conductivity.returnPressed.connect(self._update_canvas)
        self.radar_lla.returnPressed.connect(self._update_canvas)
        self.target_lla.returnPressed.connect(self._update_canvas)

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

        # Get the radar and target LLA positions
        radar_lla = self.radar_lla.text().split(',')
        target_lla = self.target_lla.text().split(',')

        radar = {'lat': float(radar_lla[0]), 'lon': float(radar_lla[1]), 'alt': float(radar_lla[2]) * 1e3}
        target = {'lat': float(target_lla[0]), 'lon': float(target_lla[1]), 'alt': float(target_lla[2]) * 1e3}

        # Set up the frequencies to be used
        frequency_start = float(self.frequency_start.text())
        frequency_end = float(self.frequency_end.text())
        frequency = linspace(frequency_start, frequency_end, 1000)

        # Get the material parameters
        relative_permittivity = float(self.relative_permittivity.text())
        conductivity = float(self.conductivity.text())

        # Calculate the diffraction pattern
        gamma = [diffraction.attenuation(radar, target, f, relative_permittivity, conductivity) for f in frequency]

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(frequency, gamma)

        # Set the plot title and labels
        self.axes1.set_title('Diffraction', size=14)
        self.axes1.set_xlabel('Frequency (Hz)', size=12)
        self.axes1.set_ylabel('Diffraction Loss (dB)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Diffraction()  # Set the form
    form.show()           # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = Diffraction()           # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
