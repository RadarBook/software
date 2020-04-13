"""
Project: RadarBook
File: PRN_ambiguity_example.py
Created by: Lee A. Harrison
On: 1/26/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter08.ui.AF_PRN_ui import Ui_MainWindow
from scipy import meshgrid
from Libs.ambiguity.ambiguity_function import phase_coded_wf
from Libs.ambiguity.prn_code import mls
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PRN(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.register_length.returnPressed.connect(self._update_canvas)
        self.chip_width.returnPressed.connect(self._update_canvas)
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
        register_length = int(self.register_length.text())
        chip_width = float(self.chip_width.text())
        plot_type = self.plot_type.currentText()

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Force the register length between 2 and 10
        if register_length < 2:
            register_length = 2

        if register_length > 10:
            register_length = 10

        if register_length == 2:
            feedback_taps = [2, 1]
        elif register_length == 3:
            feedback_taps = [3, 2]
        elif register_length == 4:
            feedback_taps = [4, 3]
        elif register_length == 5:
            feedback_taps = [5, 3]
        elif register_length == 6:
            feedback_taps = [6, 5]
        elif register_length == 7:
            feedback_taps = [7, 6]
        elif register_length == 8:
            feedback_taps = [8, 6, 5, 4]
        elif register_length == 9:
            feedback_taps = [9, 5]
        elif register_length == 10:
            feedback_taps = [10, 7]

        # Generate a maximum length sequence
        code = mls(register_length, feedback_taps)

        # Calculate the ambiguity function
        ambiguity, time_delay, doppler_frequency = phase_coded_wf(code, chip_width)

        # Create the plots
        if plot_type == 'Zero Doppler Cut':

            # Plot the ambiguity function
            self.axes1.plot(time_delay, ambiguity[round(len(doppler_frequency) / 2)], '')

            # Set the time axis limits
            self.axes1.set_xlim(-len(code) * chip_width, len(code) * chip_width)

            # Set the x and y axis labels
            self.axes1.set_xlabel("Time (s)", size=12)
            self.axes1.set_ylabel("Relative Amplitude", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        elif plot_type == 'Zero Range Cut':

            # Plot the ambiguity function
            self.axes1.plot(doppler_frequency,  ambiguity[:, round(len(time_delay) / 2)], '')

            # Set the x and y axis labels
            self.axes1.set_xlabel("Doppler (Hz)", size=12)
            self.axes1.set_ylabel("Relative Amplitude", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        elif plot_type == '2D Contour':

            # Create the grid
            t, f = meshgrid(time_delay, doppler_frequency)

            # Plot the ambiguity function
            self.axes1.contour(t, f, ambiguity, 50, cmap='jet', vmin=-0.2, vmax=1.0)

            # Set the time axis limits
            self.axes1.set_xlim(-len(code) * chip_width, len(code) * chip_width)

            # Set the x and y axis labels
            self.axes1.set_xlabel("Time (s)", size=12)
            self.axes1.set_ylabel("Doppler (Hz)", size=12)

            # Turn on the grid
            self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the plot title and labels
        self.axes1.set_title('PRN Ambiguity Function', size=14)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = PRN()  # Set the form
    form.show()   # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PRN()                  # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
