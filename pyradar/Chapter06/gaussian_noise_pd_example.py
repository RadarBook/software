"""
Project: RadarBook
File: gaussian_noise_pd_example.py
Created by: Lee A. Harrison
On: 10/10/2018
Created with: PyCharm
"""
import sys
from Chapter06.ui.GaussianNoisePd_ui import Ui_MainWindow
from scipy import linspace, log10
from Libs.detection.single_pulse import pd_gaussian
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class GaussianNoisePd(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.signal_to_noise.returnPressed.connect(self._update_canvas)
        self.probability_of_false_alarm.returnPressed.connect(self._update_canvas)

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
        snr_db = self.signal_to_noise.text().split(',')
        snr = 10.0 ** (linspace(float(snr_db[0]), float(snr_db[1]), 200) / 10.0)
        pfa = float(self.probability_of_false_alarm.text())

        # Calculate the probability of detection
        pd = pd_gaussian(snr, pfa)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(10.0 * log10(snr), pd, '')

        # Set the plot title and labels
        self.axes1.set_title('Pd - Gaussian Noise', size=14)
        self.axes1.set_xlabel('Signal to Noise (dB)', size=12)
        self.axes1.set_ylabel('Probability of Detection', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = GaussianNoisePd()  # Set the form
    form.show()               # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = GaussianNoisePd()      # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
