"""
Project: RadarBook
File: sensitivity_time_control_example.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter05.ui.STC_ui import Ui_MainWindow
from scipy import log10, array
from Libs.receivers import sensitivity_time_control
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class STC(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.pulse_repetition_frequency.returnPressed.connect(self._update_canvas)
        self.pulsewidth.returnPressed.connect(self._update_canvas)

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
        # Get the waveform values from the form
        pulse_repetition_frequency = float(self.pulse_repetition_frequency.text())
        pulsewidth = float(self.pulsewidth.text())

        receive_range, atten = sensitivity_time_control.attenuation(pulse_repetition_frequency, pulsewidth)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(receive_range, 10.0 * log10(array(atten) / max(atten)), '')

        # Set the plot title and labels
        self.axes1.set_title('Sensitivity Time Control', size=14)
        self.axes1.set_xlabel('Range (m)', size=12)
        self.axes1.set_ylabel('Normalized Attenuation (dB)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = STC()  # Set the form
    form.show()   # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = STC()                  # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
