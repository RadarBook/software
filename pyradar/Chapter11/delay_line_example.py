"""
Project: RadarBook
File: delay_line_example.py
Created by: Lee A. Harrison
On: 5/24/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter11.ui.DelayLine_ui import Ui_MainWindow
from numpy import linspace, log10, finfo
from Libs.ecm import countermeasures
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class DelayLine(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.prf_stagger.returnPressed.connect(self._update_canvas)
        self.prf_type.currentIndexChanged.connect(self._update_canvas)

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
        prf_stagger = float(self.prf_stagger.text())

        # Get the PRF type
        prf_type = self.prf_type.currentText()

        # Set up the normalized frequency space
        frequency = linspace(0, 4, 1000)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Calculate response based on PRF type
        if prf_type == 'Single':
            response = countermeasures.delay_line(frequency) / 4.0

            # Display the results
            self.axes1.plot(frequency, 10 * log10(response + finfo(float).eps), '')

        elif prf_type == 'Stagger':
            response_prf1 = countermeasures.delay_line(frequency) / 4.0
            response_prf2 = countermeasures.delay_line(prf_stagger * frequency) / 4.0
            response = 0.5 * (response_prf1 + response_prf2)

            # Display the results
            self.axes1.plot(frequency, 10 * log10(response_prf1 + finfo(float).eps), '', label='PRF 1')
            self.axes1.plot(frequency, 10 * log10(response_prf2 + finfo(float).eps), '--', label='PRF 2')
            self.axes1.plot(frequency, 10 * log10(response + finfo(float).eps), ':', label='PRF Staggered')

            # Place the legend
            self.axes1.legend(loc='lower left', prop={'size': 10})

        # Set the plot title and labels
        self.axes1.set_title('Delay Line Response', size=14)
        self.axes1.set_xlabel('Normalized Frequency (f / PRF)', size=12)
        self.axes1.set_ylabel('Amplitude (dB)', size=12)

        # Set the y-axis lim
        self.axes1.set_ylim([-30, 1])

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = DelayLine(parent)  # Set the form
    form.show()         # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = DelayLine()            # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
