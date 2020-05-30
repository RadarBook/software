"""
Project: RadarBook
File: minimum_detectable_signal_example.py
Created by: Lee A. Harrison
On: 6/29/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.MinimumDetectableSignal_ui import Ui_MainWindow
from Libs.radar_range import radar_range
from PyQt5.QtWidgets import QApplication, QMainWindow


class MinDetSignal(QMainWindow, Ui_MainWindow):
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.system_temperature.returnPressed.connect(self._update_results)
        self.bandwidth.returnPressed.connect(self._update_results)
        self.noise_figure.returnPressed.connect(self._update_results)
        self.losses.returnPressed.connect(self._update_results)
        self.signal_to_noise.returnPressed.connect(self._update_results)

        # Update for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the result boxes when the user changes an input value.
        :return:
        """
        # Set up the key word args for the inputs
        system_temperature = float(self.system_temperature.text())
        bandwidth = float(self.bandwidth.text())
        noise_figure = float(self.noise_figure.text())
        losses = float(self.losses.text())
        signal_to_noise = float(self.signal_to_noise.text())

        kwargs = {'system_temperature': system_temperature,
                  'bandwidth': bandwidth,
                  'noise_factor': 10.0 ** (noise_figure / 10.0),
                  'losses': 10.0 ** (losses / 10.0),
                  'signal_to_noise': 10.0 ** (signal_to_noise / 10.0)}

        # Calculate the minimum detectable signal
        minimum_detectable_signal = radar_range.minimum_detectable_signal(**kwargs)

        # Display the results in the boxes
        self.minimum_detectable_signal.setText('{:.2e}'.format(minimum_detectable_signal))


def start(self):
    form = MinDetSignal(self)  # Set the form
    form.show()                # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = MinDetSignal(None)      # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
