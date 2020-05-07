"""
Project: RadarBook
File: coherent_detector_example.py
Created by: Lee A. Harrison
On: 9/19/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter05.ui.CoherentDetector_ui import Ui_MainWindow
from Libs.receivers import coherent_detector
from numpy import arange, sin, real
from scipy.constants import pi
from scipy.signal import chirp
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class CoherentDetector(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.sampling_frequency.returnPressed.connect(self._update_canvas)
        self.start_frequency.returnPressed.connect(self._update_canvas)
        self.end_frequency.returnPressed.connect(self._update_canvas)
        self.am_amplitude.returnPressed.connect(self._update_canvas)
        self.am_frequency.returnPressed.connect(self._update_canvas)

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
        sampling_frequency = float(self.sampling_frequency.text())
        start_frequency = float(self.start_frequency.text())
        end_frequency = float(self.end_frequency.text())
        am_amplitude = float(self.am_amplitude.text())
        am_frequency = float(self.am_frequency.text())

        # Calculate the bandwidth and center frequency
        bandwidth = end_frequency - start_frequency
        center_frequency = 0.5 * bandwidth + start_frequency

        # Set up the waveform
        time = arange(sampling_frequency) / sampling_frequency
        if_signal = chirp(time, start_frequency, time[-1], end_frequency)
        if_signal *= (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * time))

        # Set up the key word args for the inputs
        kwargs = {'if_signal': if_signal,
                  'center_frequency': center_frequency,
                  'bandwidth': bandwidth,
                  'sample_frequency': sampling_frequency,
                  'time': time}

        # Calculate the baseband I and Q
        i_signal, q_signal = coherent_detector.iq(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(time, real(i_signal), '', label='In Phase')
        self.axes1.plot(time, real(q_signal), '-.', label='Quadrature')

        # Set the plot title and labels
        self.axes1.set_title('Coherent Detector', size=14)
        self.axes1.set_xlabel('Time (s)', size=12)
        self.axes1.set_ylabel('Amplitude (V)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Show the legend
        self.axes1.legend(loc='upper right', prop={'size': 10})

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = CoherentDetector()  # Set the form
    form.show()                # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = CoherentDetector()     # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
