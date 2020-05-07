"""
Project: RadarBook
File: power_aperture_example.py
Created by: Lee A. Harrison
On: 6/30/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.PowerAperture_ui import Ui_MainWindow
from Libs.radar_range import search_radar_range
from numpy import linspace, log10
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PowerAperture(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.target_min_range.returnPressed.connect(self._update_canvas)
        self.target_max_range.returnPressed.connect(self._update_canvas)
        self.system_temperature.returnPressed.connect(self._update_canvas)
        self.search_volume.returnPressed.connect(self._update_canvas)
        self.noise_figure.returnPressed.connect(self._update_canvas)
        self.losses.returnPressed.connect(self._update_canvas)
        self.signal_to_noise.returnPressed.connect(self._update_canvas)
        self.scan_time.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)

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
        # Get the range from the form
        target_min_range = float(self.target_min_range.text())
        target_max_range = float(self.target_max_range.text())

        # Set up the range array
        target_range = linspace(target_min_range, target_max_range, 2000)

        # Convert the noise figure to noise factor
        noise_figure = float(self.noise_figure.text())
        noise_factor = 10.0 ** (noise_figure / 10.0)

        # Convert the losses, snr and target rcs to linear units
        losses = 10.0 ** (float(self.losses.text()) / 10.0)
        target_rcs = 10.0 ** (float(self.target_rcs.text()) / 10.0)
        signal_to_noise = 10.0 ** (float(self.signal_to_noise.text()) / 10.0)

        # Set up the input args
        kwargs = {'target_range': target_range,
                  'system_temperature': float(self.system_temperature.text()),
                  'search_volume': float(self.search_volume.text()),
                  'noise_factor': noise_factor,
                  'losses': losses,
                  'signal_to_noise': signal_to_noise,
                  'scan_time': float(self.scan_time.text()),
                  'target_rcs': target_rcs}

        # Calculate the power aperture product
        power_aperture = search_radar_range.power_aperture(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(target_range / 1.0e3, 10.0 * log10(power_aperture), '')

        # Set the plot title and labels
        self.axes1.set_title('Power Aperture Product', size=14)
        self.axes1.set_xlabel('Target Range (km)', size=14)
        self.axes1.set_ylabel('Power Aperture (dB)', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = PowerAperture()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PowerAperture()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
