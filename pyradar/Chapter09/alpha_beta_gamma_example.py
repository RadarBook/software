"""
Project: RadarBook
File: alpha_beta_gamma_example.py
Created by: Lee A. Harrison
On: 3/17/2019
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter09.ui.AlphaBetaGamma_ui import Ui_MainWindow
from numpy import linspace, random, ones_like, sqrt
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class AlphaBetaGamma(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.time.returnPressed.connect(self._update_canvas)
        self.initial_position.returnPressed.connect(self._update_canvas)
        self.initial_velocity.returnPressed.connect(self._update_canvas)
        self.initial_acceleration.returnPressed.connect(self._update_canvas)
        self.noise.returnPressed.connect(self._update_canvas)
        self.alpha.returnPressed.connect(self._update_canvas)
        self.beta.returnPressed.connect(self._update_canvas)
        self.gamma.returnPressed.connect(self._update_canvas)
        self.plot_type.currentIndexChanged.connect(self._update_canvas)

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
        time = self.time.text().split(',')
        start = float(time[0])
        end = float(time[1])
        step = float(time[2])
        number_of_updates = round((end - start) / step) + 1
        t, dt = linspace(start, end, number_of_updates, retstep=True)

        initial_position = float(self.initial_position.text())
        initial_velocity = float(self.initial_velocity.text())
        initial_acceleration = float(self.initial_acceleration.text())
        noise_variance = float(self.noise.text())
        alpha = float(self.alpha.text())
        beta = float(self.beta.text())
        gamma = float(self.gamma.text())

        # True position and velocity
        v_true = initial_velocity + initial_acceleration * t
        x_true = initial_position + initial_velocity * t + 0.5 * initial_acceleration * t ** 2

        # Measurements (add noise)
        z = x_true + sqrt(noise_variance) * (random.rand(number_of_updates) - 0.5)

        # Initialize
        xk_1 = 0.0
        vk_1 = 0.0
        ak_1 = 0.0

        x_filt = []
        v_filt = []
        a_filt = []
        r_filt = []

        # Loop over all measurements
        for zk in z:
            # Predict the next state
            xk = xk_1 + vk_1 * dt + 0.5 * ak_1 * dt ** 2
            vk = vk_1 + ak_1 * dt
            ak = ak_1

            # Calculate the residual
            rk = zk - xk

            # Correct the predicted state
            xk += alpha * rk
            vk += beta / dt * rk
            ak += 2.0 * gamma / dt ** 2 * rk

            # Set the current state as previous
            xk_1 = xk
            vk_1 = vk
            ak_1 = ak

            x_filt.append(xk)
            v_filt.append(vk)
            a_filt.append(ak)
            r_filt.append(rk)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Get the selected plot from the form
        plot_type = self.plot_type.currentText()

        # Display the results
        if plot_type == 'Position':
            self.axes1.plot(t, x_true, '', label='True')
            self.axes1.plot(t, z, ':', label='Measurement')
            self.axes1.plot(t, x_filt, '--', label='Filtered')
            self.axes1.set_ylabel('Position (m)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Velocity':
            self.axes1.plot(t, v_true, '', label='True')
            self.axes1.plot(t, v_filt, '--', label='Filtered')
            self.axes1.set_ylabel('Velocity (m/s)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Acceleration':
            self.axes1.plot(t, initial_acceleration * ones_like(t), '', label='True')
            self.axes1.plot(t, a_filt, '--', label='Filtered')
            self.axes1.set_ylabel('Acceleration (m/s/s)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Residual':
            self.axes1.plot(t, r_filt, '')
            self.axes1.set_ylabel('Residual (m)', size=12)

        # Set the plot title and labels
        self.axes1.set_title('Alpha-Beta-Gamma Filter', size=14)
        self.axes1.set_xlabel('Time (s)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = AlphaBetaGamma(parent)  # Set the form
    form.show()              # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = AlphaBetaGamma()       # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()