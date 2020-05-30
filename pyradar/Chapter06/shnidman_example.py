"""
Project: RadarBook
File: shnidman_example.py
Created by: Lee A. Harrison
On: 10/12/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter06.ui.Shnidman_ui import Ui_MainWindow
from numpy import linspace, log10
from Libs.detection.shnidman import signal_to_noise
from Libs.detection.non_coherent_integration import single_pulse_snr
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Shnidman(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.probability_of_detection.returnPressed.connect(self._update_canvas)
        self.probability_of_false_alarm.returnPressed.connect(self._update_canvas)
        self.number_of_pulses.returnPressed.connect(self._update_canvas)
        self.target_type.currentIndexChanged.connect(self._update_canvas)

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
        # Get the parameters from the form
        pd = self.probability_of_detection.text().split(',')
        pd_all = linspace(float(pd[0]), float(pd[1]), 200)
        pfa = float(self.probability_of_false_alarm.text())
        number_of_pulses = int(self.number_of_pulses.text())

        # Get the selected target type from the form
        target_type = self.target_type.currentText()

        # Calculate the error in the Shnidman approximation of signal to noise
        error = [10.0 * log10(single_pulse_snr(p, pfa, number_of_pulses, target_type))
                 - signal_to_noise(p, pfa, number_of_pulses, target_type) for p in pd_all]

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(pd_all, error, '')

        # Set the plot title and labels
        self.axes1.set_title('Shnidman\'s Approximation', size=14)
        self.axes1.set_xlabel('Probability of Detection', size=12)
        self.axes1.set_ylabel('Signal to Noise Error (dB)', size=12)
        self.axes1.set_ylim(-1, 1)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Shnidman()  # Set the form
    form.show()        # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Shnidman()             # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
