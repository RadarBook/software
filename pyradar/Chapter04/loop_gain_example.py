"""
Project: RadarBook
File: loop_gain_example.py
Created by: Lee A. Harrison
On: 6/29/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.LoopGain_ui import Ui_MainWindow
from Libs.radar_range import radar_range
from numpy import log10
from PyQt5.QtWidgets import QApplication, QMainWindow


class LoopGain(QMainWindow, Ui_MainWindow):
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.reference_range.returnPressed.connect(self._update_results)
        self.reference_rcs.returnPressed.connect(self._update_results)
        self.reference_snr.returnPressed.connect(self._update_results)

        # Update for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the result boxes when the user changes an input value.
        :return:
        """
        # Set up the key word args for the inputs
        reference_range = float(self.reference_range.text())
        reference_rcs = float(self.reference_rcs.text())
        reference_snr = float(self.reference_snr.text())

        kwargs = {'reference_range': reference_range,
                  'reference_rcs': 10.0 ** (reference_rcs / 10.0),
                  'reference_snr': 10.0 ** (reference_snr / 10.0)}

        # Calculate the loop gain
        loop_gain = radar_range.loop_gain(**kwargs)

        # Display the results in the boxes
        self.loop_gain.setText('{:.2f}'.format(10.0 * log10(loop_gain)))


def start(self):
    form = LoopGain(self)     # Set the form
    form.show()               # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = LoopGain(None)          # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
