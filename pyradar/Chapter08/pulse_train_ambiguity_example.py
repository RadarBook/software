"""
Project: RadarBook
File: pulse_train_ambiguity_example.py
Created by: Lee A. Harrison
On: 1/24/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter08.ui.AFTrain_ui import Ui_MainWindow
from numpy import linspace, meshgrid, finfo
from Libs.ambiguity.ambiguity_function import pulse_train
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PulseTrain(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.pulsewidth.returnPressed.connect(self._update_canvas)
        self.pri.returnPressed.connect(self._update_canvas)
        self.number_of_pulses.returnPressed.connect(self._update_canvas)
        self.plot_type.currentIndexChanged.connect(self._update_canvas)

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
        pulsewidth = float(self.pulsewidth.text())
        pri = float(self.pri.text())
        number_of_pulses = int(self.number_of_pulses.text())
        plot_type = self.plot_type.currentText()

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Create the plots
        if plot_type == 'Zero Doppler Cut':

            # Set the time delay
            time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 1000)

            # Calculate the ambiguity function
            ambiguity = pulse_train(time_delay, finfo(float).eps, pulsewidth, pri, number_of_pulses)

            # Plot the ambiguity function
            self.axes1.plot(time_delay, ambiguity, '')

            # Set the x and y axis labels
            self.axes1.set_xlabel("Time (s)", size=12)
            self.axes1.set_ylabel("Relative Amplitude", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        elif plot_type == 'Zero Range Cut':

            # Set the Doppler mismatch
            doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 1000)

            # Calculate the ambiguity function
            ambiguity = pulse_train(finfo(float).eps, doppler_frequency, pulsewidth, pri, number_of_pulses)

            # Plot the ambiguity function
            self.axes1.plot(doppler_frequency, ambiguity, '')

            # Set the x and y axis labels
            self.axes1.set_xlabel("Doppler (Hz)", size=12)
            self.axes1.set_ylabel("Relative Amplitude", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        elif plot_type == '2D Contour':

            # Set the time delay
            time_delay = linspace(-number_of_pulses * pri, number_of_pulses * pri, 500)

            # Set the Doppler mismatch
            doppler_frequency = linspace(-2.0 / pulsewidth, 2.0 / pulsewidth, 500)

            # Create the grid
            t, f = meshgrid(time_delay, doppler_frequency)

            # Calculate the ambiguity function
            ambiguity = pulse_train(t, f, pulsewidth, pri, number_of_pulses)

            # Plot the ambiguity function
            self.axes1.contour(t, f, ambiguity + finfo('float').eps, 30, cmap='jet', vmin=-0.2, vmax=1.0)

            # Set the x and y axis labels
            self.axes1.set_xlabel("Time (s)", size=12)
            self.axes1.set_ylabel("Doppler (Hz)", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('Pulse Train Ambiguity Function', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = PulseTrain()  # Set the form
    form.show()          # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PulseTrain()           # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
