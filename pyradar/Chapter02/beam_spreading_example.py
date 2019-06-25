"""
Project: RadarBook
File: beam_spreading_example.py
Created by: Lee A. Harrison
On: 2/17/2018
Created with: PyCharm
"""
import sys
from Chapter02.ui.BeamSpreading_ui import Ui_MainWindow
from scipy import linspace, meshgrid, log10
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class BeamSpreading(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.elevation_angle.returnPressed.connect(self._update_canvas)
        self.height.returnPressed.connect(self._update_canvas)

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

        # Set up the elevation and height arrays
        theta, height = meshgrid(linspace(0.0, float(self.elevation_angle.text()), 200),
                                 linspace(0.0, float(self.height.text()), 200))

        # Calculate the beam spreading loss
        b = 1. - (0.5411 + 0.07446 * theta + (0.06272 + 0.0276 * theta) * height + 0.008288 * height ** 2) / \
            (1.728 + 0.5411 * theta + (0.1815 + 0.06272 * theta + 0.0138 * theta ** 2) * height +
             (0.01727 + 0.008288 * theta) * height ** 2) ** 2

        beam_spreading_loss = -10. * log10(b)

        # Remove the color bar
        try:
            self.cbar.remove()
        except:
            # Initial plot
            pass

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        im = self.axes1.pcolor(theta, height, beam_spreading_loss, cmap="jet")
        self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
        self.cbar.set_label("(dB)")

        # Set the plot title and labels
        self.axes1.set_title('Beam Spreading Loss', size=14)
        self.axes1.set_xlabel('Elevation Angle (degrees)', size=12)
        self.axes1.set_ylabel('Height (km)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = BeamSpreading()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = BeamSpreading()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
