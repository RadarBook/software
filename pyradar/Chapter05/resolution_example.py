"""
Project: RadarBook
File: resolution_example.py
Created by: Lee A. Harrison
On: 9/19/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter05.ui.Resolution_ui import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class Resolution(QMainWindow, Ui_MainWindow):
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.number_of_bits.returnPressed.connect(self._update_results)
        self.signal_to_noise.returnPressed.connect(self._update_results)

        # Update for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the result boxes when the user changes an input value.
        :return:
        """
        # Get the parameters from the form
        number_of_bits = float(self.number_of_bits.text())
        signal_to_noise = float(self.signal_to_noise.text())

        # Display the results in the boxes
        self.ideal_snr.setText('{:.2f}'.format(6.02 * number_of_bits + 1.76))
        self.number_of_bits_eff.setText('{:.2f}'.format((signal_to_noise - 1.76) / 6.02))


def start(self):
    form = Resolution(self)  # Set the form
    form.show()              # Show the form


def main():
    app = QApplication(sys.argv)   # A new instance of QApplication
    form = Resolution(None)        # Set the form
    form.show()                    # Show the form
    app.exec_()                    # Execute the app


if __name__ == '__main__':
    main()
