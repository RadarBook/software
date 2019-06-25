"""
Project: RadarBook
File: kalman_cv_example.py
Created by: Lee A. Harrison
On: 3/17/2019
Created with: PyCharm
"""
import sys
from Chapter09.ui.Kalman_ui import Ui_MainWindow
from scipy import linspace, zeros, zeros_like, eye, random, matmul, sqrt, ones_like
from Libs.tracking import kalman
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Kalman(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.time.returnPressed.connect(self._update_canvas)
        self.initial_position.returnPressed.connect(self._update_canvas)
        self.initial_velocity.returnPressed.connect(self._update_canvas)
        self.measurement_noise_variance.returnPressed.connect(self._update_canvas)
        self.process_noise_variance.returnPressed.connect(self._update_canvas)
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

        # Initial position
        p_xyz = self.initial_position.text().split(',')
        px = float(p_xyz[0])
        py = float(p_xyz[1])
        pz = float(p_xyz[2])

        # Initial velocity
        v_xyz = self.initial_velocity.text().split(',')
        vx = float(v_xyz[0])
        vy = float(v_xyz[1])
        vz = float(v_xyz[2])

        # Measurement and process noise variance
        measurement_noise_variance = float(self.measurement_noise_variance.text())
        process_noise_variance = float(self.process_noise_variance.text())

        # Create target trajectory
        x_true = zeros([6, number_of_updates])

        x = px + vx * t
        y = py + vy * t
        z = pz + vz * t

        x_true[0] = x
        x_true[1] = vx
        x_true[2] = y
        x_true[3] = vy
        x_true[4] = z
        x_true[5] = vz

        # Measurement noise
        v = sqrt(measurement_noise_variance) * (random.rand(number_of_updates) - 0.5)

        # Initialize state and input control vector
        x = zeros(6)
        u = zeros_like(x)

        # Initialize the covariance and control matrix
        P = 1.0e3 * eye(6)
        B = zeros_like(P)

        # Initialize measurement and process noise variance
        R = measurement_noise_variance * eye(3)
        Q = process_noise_variance * eye(6)

        # State transition and measurement transition
        A = eye(6)
        A[0, 1] = dt
        A[2, 3] = dt
        A[4, 5] = dt

        # Measurement transition matrix
        H = zeros([3, 6])
        H[0, 0] = 1
        H[1, 2] = 1
        H[2, 4] = 1

        # Initialize the Kalman filter
        kf = kalman.Kalman(x, u, P, A, B, Q, H, R)

        # Generate the measurements
        z = [matmul(H, x_true[:, i]) + v[i] for i in range(number_of_updates)]

        # Update the filter for each measurement
        kf.filter(z)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Get the selected plot from the form
        plot_type = self.plot_type.currentText()

        # Display the results
        if plot_type == 'Position - X':
            self.axes1.plot(t, x_true[0, :], '', label='True')
            self.axes1.plot(t, [z[0] for z in z], ':', label='Measurement')
            self.axes1.plot(t, [x[0] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Position - X (m)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Position - Y':
            self.axes1.plot(t, x_true[2, :], '', label='True')
            self.axes1.plot(t, [z[1] for z in z], ':', label='Measurement')
            self.axes1.plot(t, [x[2] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Position - Y (m)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Position - Z':
            self.axes1.plot(t, x_true[4, :], '', label='True')
            self.axes1.plot(t, [z[2] for z in z], ':', label='Measurement')
            self.axes1.plot(t, [x[4] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Position - Z (m)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Velocity - X':
            self.axes1.plot(t, x_true[1, :], '', label='True')
            self.axes1.plot(t, [x[1] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Velocity - X (m/s)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Velocity - Y':
            self.axes1.plot(t, x_true[3, :], '', label='True')
            self.axes1.plot(t, [x[3] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Velocity - Y (m/s)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Velocity - Z':
            self.axes1.plot(t, x_true[5, :], '', label='True')
            self.axes1.plot(t, [x[5] for x in kf.state], '--', label='Filtered')
            self.axes1.set_ylabel('Velocity - Z (m/s)', size=12)
            self.axes1.legend(loc='best', prop={'size': 10})
        elif plot_type == 'Residual':
            self.axes1.plot(t, kf.residual, '')
            self.axes1.set_ylabel('Residual (m)', size=12)

        # Set the plot title and labels
        self.axes1.set_title('Kalman Filter', size=14)
        self.axes1.set_xlabel('Time (s)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = Kalman()  # Set the form
    form.show()      # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = Kalman()               # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
