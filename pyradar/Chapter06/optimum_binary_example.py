"""
Project: RadarBook
File: optimum_binary_example.py
Created by: Lee A. Harrison
On: 10/11/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter06.ui.OptimumBinary_ui import Ui_MainWindow
from numpy import arange, ceil
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class OptimumBinary(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.number_of_pulses.returnPressed.connect(self._update_canvas)
        self.target_type.currentIndexChanged.connect(self._update_canvas)

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
        number_of_pulses = int(self.number_of_pulses.text())

        # Get the selected target type from the form
        target_type = self.target_type.currentText()

        if target_type == 'Swerling 0':
            alpha = 0.8
            beta = -0.02
        elif target_type == 'Swerling 1':
            alpha = 0.8
            beta = -0.02
        elif target_type == 'Swerling 2':
            alpha = 0.91
            beta = -0.38
        elif target_type == 'Swerling 3':
            alpha = 0.8
            beta = -0.02
        elif target_type == 'Swerling 4':
            alpha = 0.873
            beta = -0.27

        # Calculate the optimum choice for M
        np = arange(1, number_of_pulses+1)
        m_optimum = [ceil(10.0 ** beta * n ** alpha) for n in np]

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(np, m_optimum, '')

        # Set the plot title and labels
        self.axes1.set_title('Optimum M for Binary Integration', size=14)
        self.axes1.set_xlabel('Number of Pulses', size=12)
        self.axes1.set_ylabel('M', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = OptimumBinary()  # Set the form
    form.show()             # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = OptimumBinary()        # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
