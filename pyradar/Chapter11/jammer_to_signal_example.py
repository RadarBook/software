"""
Project: RadarBook
File: jammer_to_signal_example.py
Created by: Lee A. Harrison
On: 5/21/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter11.ui.JSR_ui import Ui_MainWindow
from numpy import linspace, log10
from Libs.ecm import countermeasures
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class JSR(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.radar_transmit_power.returnPressed.connect(self._update_canvas)
        self.radar_antenna_gain.returnPressed.connect(self._update_canvas)
        self.radar_antenna_sidelobe.returnPressed.connect(self._update_canvas)
        self.radar_bandwidth.returnPressed.connect(self._update_canvas)
        self.radar_losses.returnPressed.connect(self._update_canvas)
        self.target_range.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)
        self.jammer_bandwidth.returnPressed.connect(self._update_canvas)
        self.jammer_erp.returnPressed.connect(self._update_canvas)
        self.jammer_range.returnPressed.connect(self._update_canvas)
        self.jammer_type.currentIndexChanged.connect(self._update_canvas)

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
        Update the figure when the user changes and input value.
        :return:
        """
        # Get the parameters from the form
        target_range = self.target_range.text().split(',')
        target_range_vector = linspace(float(target_range[0]), float(target_range[1]), 1000) * 1e3

        # Get the jammer type
        jammer_type = self.jammer_type.currentText()

        # Set up the input args based on jammer type
        if jammer_type == 'Self Screening':
            kwargs = {'peak_power': float(self.radar_transmit_power.text()),
                      'antenna_gain': 10 ** (float(self.radar_antenna_gain.text()) / 10.0),
                      'target_rcs': 10 ** (float(self.target_rcs.text()) / 10.0),
                      'jammer_range': target_range_vector,
                      'jammer_bandwidth': float(self.jammer_bandwidth.text()),
                      'effective_radiated_power': 10 ** (float(self.jammer_erp.text()) / 10.0),
                      'target_range': target_range_vector,
                      'radar_bandwidth': float(self.radar_bandwidth.text()),
                      'losses': 10 ** (float(self.radar_losses.text()) / 10.0),
                      'antenna_gain_jammer_direction': 10 ** (float(self.radar_antenna_gain.text()) / 10.0)}
        elif jammer_type == 'Escort':
            kwargs = {'peak_power': float(self.radar_transmit_power.text()),
                      'antenna_gain': 10 ** (float(self.radar_antenna_gain.text()) / 10.0),
                      'target_rcs': 10 ** (float(self.target_rcs.text()) / 10.0),
                      'jammer_range': float(self.jammer_range.text()) * 1e3,
                      'jammer_bandwidth': float(self.jammer_bandwidth.text()),
                      'effective_radiated_power': 10 ** (float(self.jammer_erp.text()) / 10.0),
                      'target_range': target_range_vector,
                      'radar_bandwidth': float(self.radar_bandwidth.text()),
                      'losses': 10 ** (float(self.radar_losses.text()) / 10.0),
                      'antenna_gain_jammer_direction': 10 ** (float(self.radar_antenna_sidelobe.text()) / 10.0)}

        # Calculate the jammer to signal ratio
        jsr = countermeasures.jammer_to_signal(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(target_range_vector / 1e3, 10 * log10(jsr), '')

        # Set the plot title and labels
        self.axes1.set_title('Jammer to Signal Ratio', size=14)
        self.axes1.set_xlabel('Target Range (km)', size=12)
        self.axes1.set_ylabel('Jammer to Signal Ratio (dB)', size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = JSR(parent)  # Set the form
    form.show()   # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = JSR()                  # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
