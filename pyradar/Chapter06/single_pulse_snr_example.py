"""
Project: RadarBook
File: single_pulse_snr_example.py
Created by: Lee A. Harrison
On: 10/10/2018
Created with: PyCharm
"""
import sys
from Chapter06.ui.SinglePulseSNR_ui import Ui_MainWindow
from scipy import log10, arange
from Libs.detection.single_pulse import snr_reduction, snr_gain, single_pulse_snr
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class SinglePulseSNR(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.probability_of_false_alarm.returnPressed.connect(self._update_canvas)
        self.probability_of_detection.returnPressed.connect(self._update_canvas)
        self.number_of_pulses.returnPressed.connect(self._update_canvas)

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
        pfa = float(self.probability_of_false_alarm.text())
        pd = float(self.probability_of_detection.text())
        number_of_pulses = int(self.number_of_pulses.text())
        np = arange(1, number_of_pulses + 1)

        # Find the required signal to noise for the pd & pfa
        required_snr = single_pulse_snr(pd, pfa)

        # Calculate the single pulse signal to noise (Curry)
        signal_to_noise_reduction = snr_reduction(np, required_snr)

        # Calculate the single pulse signal to noise (Peebles)
        signal_to_noise_gain = snr_gain(pd, pfa, np, required_snr)

        # Calculate the single pulse signal to noise for coherent integration
        signal_to_noise_coherent = 10.0 * log10(required_snr / np)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(np, signal_to_noise_coherent, '', label='Coherent Integration')
        self.axes1.plot(np, signal_to_noise_gain, '--', label='Noncoherent Integration (6.22)')
        self.axes1.plot(np, signal_to_noise_reduction, '-.', label='Noncoherent Integration (6.21)')

        # Set the plot title and labels
        self.axes1.set_title('Single Pulse Signal to Noise', size=14)
        self.axes1.set_xlabel('Number of Pulses', size=12)
        self.axes1.set_ylabel('Signal to Noise (dB)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Turn on the legend
        self.axes1.legend(loc='best', prop={'size': 10})

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = SinglePulseSNR()  # Set the form
    form.show()              # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = SinglePulseSNR()       # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
