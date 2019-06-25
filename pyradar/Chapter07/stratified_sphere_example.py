"""
Project: RadarBook
File: stratified_sphere_example.py
Created by: Lee A. Harrison
On: 11/23/2018
Created with: PyCharm
"""
import sys
from Chapter07.ui.StratifiedSphere_ui import Ui_MainWindow
from scipy import log10, linspace, ones, pi, degrees, array
from Libs.rcs.stratified_sphere import coefficients, radar_cross_section
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class StratSphere(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.frequency.returnPressed.connect(self._update_canvas)
        self.radius.returnPressed.connect(self._update_canvas)
        self.mu_r.returnPressed.connect(self._update_canvas)
        self.eps_r.returnPressed.connect(self._update_canvas)
        self.number_of_modes.returnPressed.connect(self._update_canvas)
        self.pec.currentIndexChanged.connect(self._update_canvas)

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
        frequency = float(self.frequency.text())
        radius = self.radius.text().split(',')
        mu_r = self.mu_r.text().split(',')
        eps_r = self.eps_r.text().split(',')
        number_of_modes = int(self.number_of_modes.text())

        # To put the parameters in order
        nr = len(radius)

        mu = ones(nr + 1)
        eps = ones(nr + 1)
        ra = ones(nr)

        # Set up the parameters in the correct order
        i = 0
        for r in radius:
            ra[nr - 1 - i] = float(r)
            i += 1

        i = 0
        for m, e in zip(mu_r, eps_r):
            mu[nr - i] = float(m)
            eps[nr - i] = float(e)
            i += 1

        # Flag for PEC core
        pec = self.pec.currentText()

        pec_b = False
        if pec == 'True':
            pec_b = True

        # Set the observation angles
        observation_angle = linspace(0, pi, 721)

        An, Bn = coefficients(frequency, eps, mu, ra, number_of_modes, pec_b)

        et = array([radar_cross_section(frequency, oa, 0, An, Bn) for oa in observation_angle])
        ep = array([radar_cross_section(frequency, oa, 90, An, Bn) for oa in observation_angle])

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(degrees(observation_angle), 20.0 * log10(abs(ep[:, 1])), '', label='TE')
        self.axes1.plot(degrees(observation_angle), 20.0 * log10(abs(et[:, 0])), '--', label='TM')

        # Set the plot title and labels
        self.axes1.set_title('RCS vs Bistatic Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Observation Angle (deg)', size=12)
        self.axes1.set_ylim(min(20.0 * log10(abs(et[:,0]))) - 3, max(20.0 * log10(abs(et[:,0]))) + 3)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='upper left', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = StratSphere()  # Set the form
    form.show()           # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = StratSphere()          # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
