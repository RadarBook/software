"""
Project: RadarBook
File: probability_distributions_example.py
Created by: Lee A. Harrison
On: 10/10/2018
Created with: PyCharm
"""
import sys
from Chapter06.ui.Distributions_ui import Ui_MainWindow
from scipy.stats import norm, weibull_min, rayleigh, rice, chi2
from scipy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Distributions(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.loc.returnPressed.connect(self._update_canvas)
        self.scale.returnPressed.connect(self._update_canvas)
        self.shape_factor.returnPressed.connect(self._update_canvas)
        self.distribution_type.currentIndexChanged.connect(self._update_canvas)

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
        loc = float(self.loc.text())
        scale = float(self.scale.text())
        shape_factor = float(self.shape_factor.text())

        # Get the selected distribution from the form
        distribution_type = self.distribution_type.currentText()

        if distribution_type == 'Gaussian':
            x = linspace(norm.ppf(0.001, loc, scale),  norm.ppf(0.999, loc, scale), 200)
            y = norm.pdf(x, loc, scale)
        elif distribution_type == 'Weibull':
            x = linspace(weibull_min.ppf(0.001, shape_factor), weibull_min.ppf(0.999, shape_factor), 200)
            y = weibull_min.pdf(x, shape_factor, loc, scale)
        elif distribution_type == 'Rayleigh':
            x = linspace(rayleigh.ppf(0.001, loc, scale), rayleigh.ppf(0.999, loc, scale), 200)
            y = rayleigh.pdf(x, loc, scale)
        elif distribution_type == 'Rice':
            x = linspace(rice.ppf(0.001, shape_factor), rice.ppf(0.999, shape_factor), 200)
            y = rice.pdf(x, shape_factor, loc, scale)
        elif distribution_type == 'Chi Squared':
            x = linspace(chi2.ppf(0.001, shape_factor), chi2.ppf(0.999, shape_factor), 200)
            y = chi2.pdf(x, shape_factor, loc, scale)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(x, y, '')

        # Set the plot title and labels
        self.axes1.set_title('Probability Density Function', size=14)
        self.axes1.set_xlabel('x', size=12)
        self.axes1.set_ylabel('Probability p(x)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Distributions()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Distributions()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
