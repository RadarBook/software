"""
Project: PythonRadarBook
File: noise_figure_example.py
Created by: Lee A. Harrison
On: 9/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter05.ui.NoiseFigure_ui import Ui_MainWindow
from Libs.receivers import noise_figure
from PyQt5.QtWidgets import QApplication, QMainWindow


class NoiseFigure(QMainWindow, Ui_MainWindow):
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.gain.returnPressed.connect(self._update_results)
        self.noise_figure.returnPressed.connect(self._update_results)

        # Update for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the result boxes when the user changes an input value.
        :return:
        """
        # Set up the key word args for the inputs
        gain = self.gain.text().split(',')
        noise_figure_f = self.noise_figure.text().split(',')

        gain_db = [float(g) for g in gain]
        noise_figure_db = [float(nf) for nf in noise_figure_f]

        # Calculate the total noise figure
        total_noise_figure = noise_figure.total_noise_figure(gain_db, noise_figure_db)

        # Display the results in the boxes
        self.total_noise_figure.setText('{:.4f}'.format(total_noise_figure))


def start(self):
    form = NoiseFigure(self)  # Set the form
    form.show()                 # Show the form


def main():
    app = QApplication(sys.argv)        # A new instance of QApplication
    form = NoiseFIgure(None)            # Set the form
    form.show()                         # Show the form
    app.exec_()                         # Execute the app


if __name__ == '__main__':
    main()