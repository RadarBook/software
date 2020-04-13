"""
Project: RadarBook
File: atmosphere_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter02.ui.Atmosphere_ui import Ui_MainWindow
from Libs.wave_propagation import atmosphere
from scipy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class AtmosphericAttenuation(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequencyStartGHz.returnPressed.connect(self._update_canvas)
        self.frequencyEndGHz.returnPressed.connect(self._update_canvas)
        self.temperature.returnPressed.connect(self._update_canvas)
        self.dry_air_pressure.returnPressed.connect(self._update_canvas)
        self.water_vapor_density.returnPressed.connect(self._update_canvas)

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
        Update the figure when the user changes an input value
        :return:
        """

        # Get the start and end frequency from the form
        frequency_start = float(self.frequencyStartGHz.text())
        frequency_end = float(self.frequencyEndGHz.text())

        # Set up the frequency array
        frequency = linspace(frequency_start, frequency_end, 1000)

        # Set up the input args
        kwargs = {'frequency': frequency,
                  'temperature': float(self.temperature.text()),
                  'dry_air_pressure': float(self.dry_air_pressure.text()),
                  'water_vapor_density': float(self.water_vapor_density.text())}

        # Calculate the attenuation
        gamma = atmosphere.attenuation(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.semilogy(frequency, gamma)

        # Set the plot title and labels
        self.axes1.set_title('Atmospheric Attenuation', size=14)
        self.axes1.set_xlabel('Frequency (GHz)', size=12)
        self.axes1.set_ylabel('Specific Attenuation (dB/km)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = AtmosphericAttenuation()  # Set the form
    form.show()                      # Show the form


def main():
    app = QApplication(sys.argv)        # A new instance of QApplication
    form = AtmosphericAttenuation()     # Set the form
    form.show()                         # Show the form
    app.exec_()                         # Execute the app


if __name__ == '__main__':
    main()
