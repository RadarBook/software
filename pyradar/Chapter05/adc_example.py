"""
Project: RadarBook
File: adc_example.py
Created by: Lee A. Harrison
On: 9/19/2018
Created with: PyCharm
"""
import sys
from Chapter05.ui.ADC_ui import Ui_MainWindow
from Libs.receivers import quantization
from scipy import arange, sin, pi, linspace
from scipy.signal import chirp
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ADC(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.number_of_bits.returnPressed.connect(self._update_canvas)
        self.sampling_frequency.returnPressed.connect(self._update_canvas)
        self.start_frequency.returnPressed.connect(self._update_canvas)
        self.end_frequency.returnPressed.connect(self._update_canvas)
        self.am_amplitude.returnPressed.connect(self._update_canvas)
        self.am_frequency.returnPressed.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure() 
        self.axes1 = fig.add_subplot(211)
        self.axes2 = fig.add_subplot(212)
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
        number_of_bits = int(self.number_of_bits.text())
        sampling_frequency = float(self.sampling_frequency.text())
        start_frequency = float(self.start_frequency.text())
        end_frequency = float(self.end_frequency.text())
        am_amplitude = float(self.am_amplitude.text())
        am_frequency = float(self.am_frequency.text())

        # Analog signal for plotting
        t = linspace(0.0, 1.0, 4196)
        a_signal = chirp(t, start_frequency, t[-1], end_frequency)
        a_signal *= (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * t))

        # Set up the waveform
        time = arange(sampling_frequency + 1) / sampling_frequency
        if_signal = chirp(time, start_frequency, time[-1], end_frequency)
        if_signal *= (1.0 + am_amplitude * sin(2.0 * pi * am_frequency * time))

        # Calculate the envelope
        quantized_signal, error_signal = quantization.quantize(if_signal, number_of_bits)

        # Clear the axes for the updated plot
        self.axes1.clear()
        self.axes2.clear()

        # Display the results
        self.axes1.plot(t, a_signal, '', label='Analog Signal')
        self.axes1.plot(time, quantized_signal, '-.', label='Digital Signal')
        self.axes2.plot(time, error_signal, '', label='Quadrature')

        # Set the plot title and labels
        self.axes1.set_title('Analog to Digital Conversion', size=14)
        self.axes2.set_xlabel('Time (s)', size=12)
        self.axes1.set_ylabel('Amplitude (V)', size=12)
        self.axes2.set_ylabel('Error (V)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)
        self.axes2.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)
        self.axes2.grid(linestyle=':', linewidth=0.5)

        # Show the legend
        self.axes1.legend(loc='lower left', prop={'size': 10})

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = ADC()  # Set the form
    form.show()   # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ADC()                  # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
