"""
Project: RadarBook
File: output_signal_to_noise_bistatic_example.py
Created by: Lee A. Harrison
On: 7/1/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.OutputSNRBistatic_ui import Ui_MainWindow
from Libs.radar_range import bistatic_radar_range
from numpy import linspace, log10
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class OutputSNRBistatic(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.range_product_max.returnPressed.connect(self._update_canvas)
        self.range_product_min.returnPressed.connect(self._update_canvas)
        self.system_temperature.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.noise_figure.returnPressed.connect(self._update_canvas)
        self.transmit_losses.returnPressed.connect(self._update_canvas)
        self.receive_losses.returnPressed.connect(self._update_canvas)
        self.peak_power.returnPressed.connect(self._update_canvas)
        self.transmit_antenna_gain.returnPressed.connect(self._update_canvas)
        self.receive_antenna_gain.returnPressed.connect(self._update_canvas)
        self.frequency.returnPressed.connect(self._update_canvas)
        self.bistatic_target_rcs.returnPressed.connect(self._update_canvas)

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
        # Get the range product from the form
        range_product_min = float(self.range_product_min.text())
        range_product_max = float(self.range_product_max.text())

        # Set up the range array
        range_product = linspace(range_product_min, range_product_max, 2000)

        # Convert the noise figure to noise factor
        noise_figure = float(self.noise_figure.text())
        noise_factor = 10.0 ** (noise_figure / 10.0)

        # Convert the losses, antenna gain and target rcs to linear units
        transmit_losses = 10.0 ** (float(self.transmit_losses.text()) / 10.0)
        receive_losses = 10.0 ** (float(self.receive_losses.text()) / 10.0)
        transmit_antenna_gain = 10.0 ** (float(self.transmit_antenna_gain.text()) / 10.0)
        receive_antenna_gain = 10.0 ** (float(self.receive_antenna_gain.text()) / 10.0)
        bistatic_target_rcs = 10.0 ** (float(self.bistatic_target_rcs.text()) / 10.0)

        # Set up the input args
        kwargs = {'transmit_target_range': 1.0,
                  'receive_target_range': range_product,
                  'system_temperature': float(self.system_temperature.text()),
                  'bandwidth': float(self.bandwidth.text()),
                  'noise_factor': noise_factor,
                  'transmit_losses': transmit_losses,
                  'receive_losses': receive_losses,
                  'peak_power': float(self.peak_power.text()),
                  'transmit_antenna_gain': transmit_antenna_gain,
                  'receive_antenna_gain': receive_antenna_gain,
                  'frequency': float(self.frequency.text()),
                  'bistatic_target_rcs': bistatic_target_rcs}

        # Calculate the bistatic output signal to noise ratio
        output_snr = bistatic_radar_range.output_snr(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(range_product / 1.0e6, 10.0 * log10(output_snr), '')

        # Set the plot title and labels
        self.axes1.set_title('Bistatic Output Signal to Noise Ratio', size=14)
        self.axes1.set_xlabel('Range Product (km$^2$)', size=12)
        self.axes1.set_ylabel('Output Signal to Noise Ratio (dB)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = OutputSNRBistatic()  # Set the form
    form.show()                 # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = OutputSNRBistatic()    # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
