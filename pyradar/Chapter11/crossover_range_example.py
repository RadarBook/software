"""
Project: RadarBook
File: crossover_range_example.py
Created by: Lee A. Harrison
On: 5/21/2019
Created with: PyCharm
"""
import sys
from Chapter11.ui.Crossover_ui import Ui_MainWindow
from scipy import linspace
from Libs.ecm import countermeasures
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Crossover(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.radar_transmit_power.returnPressed.connect(self._update_canvas)
        self.radar_antenna_gain.returnPressed.connect(self._update_canvas)
        self.radar_antenna_sidelobe.returnPressed.connect(self._update_canvas)
        self.radar_bandwidth.returnPressed.connect(self._update_canvas)
        self.radar_losses.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)
        self.jammer_bandwidth.returnPressed.connect(self._update_canvas)
        self.jammer_erp.returnPressed.connect(self._update_canvas)
        self.jammer_range.returnPressed.connect(self._update_canvas)
        self.jammer_type.currentIndexChanged.connect(self._update_canvas)

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
        Update the figure when the user changes and input value.
        :return:
        """
        # Get the parameters from the form
        jammer_erp = self.jammer_erp.text().split(',')
        jammer_erp_vector = linspace(float(jammer_erp[0]), float(jammer_erp[1]), 1000)

        # Load the selected target
        jammer_type = self.jammer_type.currentText()

        # Set up the input args based on jammer type
        if jammer_type == 'Self Screening':
            kwargs = {'peak_power': float(self.radar_transmit_power.text()),
                      'antenna_gain': 10 ** (float(self.radar_antenna_gain.text()) / 10.0),
                      'target_rcs': 10 ** (float(self.target_rcs.text()) / 10.0),
                      'jammer_bandwidth': float(self.jammer_bandwidth.text()),
                      'effective_radiated_power': 10 ** (jammer_erp_vector / 10.0),
                      'radar_bandwidth': float(self.radar_bandwidth.text()),
                      'losses': 10 ** (float(self.radar_losses.text()) / 10.0)}

            # Calculate the jammer to signal ratio
            crossover_range = countermeasures.crossover_range_selfscreen(**kwargs)

        elif jammer_type == 'Escort':
            kwargs = {'peak_power': float(self.radar_transmit_power.text()),
                      'antenna_gain': 10 ** (float(self.radar_antenna_gain.text()) / 10.0),
                      'target_rcs': 10 ** (float(self.target_rcs.text()) / 10.0),
                      'jammer_range': float(self.jammer_range.text()) * 1e3,
                      'jammer_bandwidth': float(self.jammer_bandwidth.text()),
                      'effective_radiated_power': 10 ** (jammer_erp_vector / 10.0),
                      'radar_bandwidth': float(self.radar_bandwidth.text()),
                      'losses': 10 ** (float(self.radar_losses.text()) / 10.0),
                      'antenna_gain_jammer_direction': 10 ** (float(self.radar_antenna_sidelobe.text()) / 10.0)}

            # Calculate the jammer to signal ratio
            crossover_range = countermeasures.crossover_range_escort(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(jammer_erp_vector, crossover_range, '')

        # Set the plot title and labels
        self.axes1.set_title('Crossover Range', size=14)
        self.axes1.set_xlabel('Jammer ERP (dBW)', size=12)
        self.axes1.set_ylabel('Crossover Range (m)', size=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Crossover()  # Set the form
    form.show()         # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Crossover()            # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
