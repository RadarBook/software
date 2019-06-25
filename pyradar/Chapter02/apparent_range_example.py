"""
Project: RadarBook
File: apparent_range_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm
"""
import sys
from Chapter02.ui.ApparentRange_ui import Ui_MainWindow
from Libs.wave_propagation import refraction
from scipy import array
from PyQt5.QtWidgets import QApplication, QMainWindow


class ApparentRange(QMainWindow, Ui_MainWindow):
    def __init__(self, parent):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.radar_lla.returnPressed.connect(self._update_results)
        self.target_lla.returnPressed.connect(self._update_results)

        # Update for the first display
        self._update_results()

    def _update_results(self):
        """
        Update the result boxes when the user changes an input value.
        :return:
        """
        # Set up the key word args for the inputs
        radar = self.radar_lla.text().split(',')
        target = self.target_lla.text().split(',')

        radar_lla = array([float(radar[0]),  float(radar[1]),  float(radar[2])])
        target_lla = array([float(target[0]), float(target[1]), float(target[2])])

        kwargs = {'radar_lla': radar_lla, 'target_lla': target_lla}

        # Calculate the true and apparent ranges
        true_range, apparent_range = refraction.apparent_range(**kwargs)

        # Display the results in the boxes
        self.true_range.setText('{:.4f}'.format(true_range/1.e3))
        self.apparent_range.setText('{:.4f}'.format(apparent_range/1.e3))


def start(self):
    form = ApparentRange(self)  # Set the form
    form.show()                 # Show the form


def main():
    app = QApplication(sys.argv)    # A new instance of QApplication
    form = ApparentRange(None)      # Set the form
    form.show()                     # Show the form
    app.exec_()                     # Execute the app


if __name__ == '__main__':
    main()
