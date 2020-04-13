"""
Project: RadarBook
File: fdtd_example.py
Created by: Lee A. Harrison
On: 10/24/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter07.ui.FDTD_ui import Ui_MainWindow
from scipy import sqrt, sin, cos, radians, zeros, log, exp, linspace, meshgrid
from scipy.constants import c, epsilon_0, mu_0
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class FDTD(QMainWindow, Ui_MainWindow):
    """
    FDTD object.
    """
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        # Connect to the button
        self.start_fdtd.clicked.connect(self._start_fdtd)

        # Set up a figure for the plotting canvas
        fig = Figure()
        self.fig = fig
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # TE or TM
        self.mode = None

        # Angle of the incident field (degrees)
        self.incident_angle = None

        # Number of time steps
        self.number_of_time_steps = None

        # Geometry file to use
        self.geometry_file = None

        # Width of the Gaussian pulse in time steps
        self.gaussian_pulse_width = None

        # Amplitude of the Gaussian pulse
        self.gaussian_pulse_amplitude = None

        # Number of PML layers
        self.number_of_pml = None

        # Others that will be set during initialization
        self.nx = None
        self.ny = None

        self.dx = None
        self.dy = None

        self.dt = None

        self.mu_r = None
        self.eps_r = None
        self.sigma = None

        self.exi = None
        self.eyi = None
        self.dexi = None
        self.deyi = None
        self.exs = None
        self.eys = None
        self.hzs = None
        self.dhzi = None

        self.hxs = None
        self.hys = None
        self.dhxi = None
        self.dhyi = None
        self.ezs = None
        self.ezi = None
        self.dezi = None

        self.esctc = None
        self.eincc = None
        self.edevcn = None
        self.ecrlx = None
        self.ecrly = None
        self.dtmdx = None
        self.dtmdy = None
        self.hdhvcn = None

        self.amplitude_y = None
        self.amplitude_x = None

        self.geometry_file = '../Libs/rcs/fdtd.cell'

    def _start_fdtd(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        # Get the parameters from the form
        self.mode = self._mode.currentText()
        self.incident_angle = float(self._incident_angle.text())
        self.number_of_time_steps = int(self._number_of_time_steps.text())
        self.gaussian_pulse_width = int(self._gaussian_pulse_width.text())
        self.gaussian_pulse_amplitude = float(self._gaussian_pulse_amplitude.text())
        self.number_of_pml = int(self._number_of_pml.text())

        # Read the geometry file and calculate material parameters
        self.initialize()

    def initialize(self):
        """
        Initialize the variables for FDTD calculations.
        :return:
        """
        # Read the geometry file
        self.read_geometry_file()

        # Initialize the fields
        if self.mode == 'TE':
            self.exi = zeros([self.nx, self.ny])
            self.eyi = zeros([self.nx, self.ny])
            self.dexi = zeros([self.nx, self.ny])
            self.deyi = zeros([self.nx, self.ny])
            self.exs = zeros([self.nx, self.ny])
            self.eys = zeros([self.nx, self.ny])
            self.hzs = zeros([self.nx, self.ny])
            self.dhzi = zeros([self.nx, self.ny])
        else:
            self.hxs = zeros([self.nx, self.ny])
            self.hys = zeros([self.nx, self.ny])
            self.dhxi = zeros([self.nx, self.ny])
            self.dhyi = zeros([self.nx, self.ny])
            self.ezs = zeros([self.nx, self.ny])
            self.ezi = zeros([self.nx, self.ny])
            self.dezi = zeros([self.nx, self.ny])

        # Initialize the other values
        self.esctc = zeros([self.nx, self.ny])
        self.eincc = zeros([self.nx, self.ny])
        self.edevcn = zeros([self.nx, self.ny])
        self.ecrlx = zeros([self.nx, self.ny])
        self.ecrly = zeros([self.nx, self.ny])
        self.dtmdx = zeros([self.nx, self.ny])
        self.dtmdy = zeros([self.nx, self.ny])
        self.hdhvcn = zeros([self.nx, self.ny])

        # Calculate the maximum time step allowed by the Courant stability condition
        self.dt = 1.0 / (c * (sqrt(1.0 / (self.dx ** 2) + 1.0 / (self.dy ** 2))))

        for i in range(self.nx):
            for j in range(self.ny):
                eps = epsilon_0 * self.eps_r[i][j]
                mu = mu_0 * self.mu_r[i][j]
                self.esctc[i][j] = eps / (eps + self.sigma[i][j] * self.dt)
                self.eincc[i][j] = self.sigma[i][j] * self.dt / (eps + self.sigma[i][j] * self.dt)
                self.edevcn[i][j] = self.dt * (eps - epsilon_0) / (eps + self.sigma[i][j] * self.dt)
                self.ecrlx[i][j] = self.dt / ((eps + self.sigma[i][j] * self.dt) * self.dx)
                self.ecrly[i][j] = self.dt / ((eps + self.sigma[i][j] * self.dt) * self.dy)
                self.dtmdx[i][j] = self.dt / (mu * self.dx)
                self.dtmdy[i][j] = self.dt / (mu * self.dy)
                self.hdhvcn[i][j] = self.dt * (mu - mu_0) / mu

        # Amplitude of incident field components
        self.amplitude_x = -self.gaussian_pulse_amplitude * sin(radians(self.incident_angle))
        self.amplitude_y = self.gaussian_pulse_amplitude * cos(radians(self.incident_angle))

        # Run the selected mode
        if self.mode == 'TE':
            self.te()
        else:
            self.tm()

    def read_geometry_file(self):
        """
        Read the FDTD geometry file.
        :return:
        """

        # Get the base path for the file
        base_path = Path(__file__).parent

        with open((base_path / self.geometry_file).resolve(), 'r') as file:

            # Header Line 1: Comment
            _ = file.readline()

            # Header Line 2: nx ny
            line = file.readline()
            line_list = line.split()
            self.nx = int(line_list[0])
            self.ny = int(line_list[1])

            # Header Line 3: Comment
            _ = file.readline()

            # Header Line 4: dx dy
            line = file.readline()
            line_list = line.split()
            self.dx = float(line_list[0])
            self.dy = float(line_list[1])

            # Set up the PML areas first
            self.nx += 2 * self.number_of_pml
            self.ny += 2 * self.number_of_pml

            self.mu_r = zeros([self.nx, self.ny])
            self.eps_r = zeros([self.nx, self.ny])
            self.sigma = zeros([self.nx, self.ny])

            # Set up the maximum conductivities
            sigma_max_x = -3.0 * epsilon_0 * c * log(1e-5) / (2.0 * self.dx * self.number_of_pml)
            sigma_max_y = -3.0 * epsilon_0 * c * log(1e-5) / (2.0 * self.dy * self.number_of_pml)

            # Create the conductivity profile
            sigma_v = [((m + 0.5) / (self.number_of_pml + 0.5)) ** 2 for m in range(self.number_of_pml)]

            # Back region
            for i in range(self.nx):
                for j in range(self.number_of_pml):
                    self.mu_r[i][j] = 1.0
                    self.eps_r[i][j] = 1.0
                    self.sigma[i][j] = sigma_max_y * sigma_v[self.number_of_pml - 1 - j]

            # Front region
            for i in range(self.nx):
                for j in range(self.ny - self.number_of_pml, self.ny):
                    self.mu_r[i][j] = 1.0
                    self.eps_r[i][j] = 1.0
                    self.sigma[i][j] = sigma_max_y * sigma_v[j - (self.ny - self.number_of_pml)]

            # Left region
            for i in range(self.number_of_pml):
                for j in range(self.ny):
                    self.mu_r[i][j] = 1.0
                    self.eps_r[i][j] = 1.0
                    self.sigma[i][j] += sigma_max_x * sigma_v[self.number_of_pml - 1 - i]

            # Right region
            for i in range(self.nx - self.number_of_pml, self.nx):
                for j in range(self.ny):
                    self.mu_r[i][j] = 1.0
                    self.eps_r[i][j] = 1.0
                    self.sigma[i][j] += sigma_max_x * sigma_v[i - (self.nx - self.number_of_pml)]

            # Read the geometry
            for i in range(self.number_of_pml, self.nx - self.number_of_pml):
                for j in range(self.number_of_pml, self.ny - self.number_of_pml):

                    line = file.readline()

                    line_list = line.split()

                    # Relative permeability first
                    self.mu_r[i][j] = float(line_list[0])

                    # Relative permittivity next
                    self.eps_r[i][j] = float(line_list[1])

                    # Finally the conductivity
                    self.sigma[i][j] = float(line_list[2])
        file.close()

    def te(self):
        """
        TE mode.
        :return:
        """
        # Start at time = 0
        t = 0.0

        # Loop over the time steps
        for n in range(self.number_of_time_steps):

            # Update the scattered electric field
            self.escattered_te(t)

            # Advance the time by 1/2 time step
            t += 0.5 * self.dt

            # Update the scattered magnetic field
            self.hscattered_te(t)

            # Advance the time by 1/2 time step
            t += 0.5 * self.dt

            # Update the canvas
            self._update_canvas()

            # Progress
            print('{} of {} time steps'.format(n + 1, self.number_of_time_steps))

    def tm(self):
        """
        TM mode.
        :return:
        """
        # Start at time = 0
        t = 0.0

        # Loop over the time steps
        for n in range(self.number_of_time_steps):

            # Update the scattered electric field
            self.escattered_tm(t)

            # Advance the time by 1/2 time step
            t += 0.5 * self.dt

            # Update the scattered magnetic field
            self.hscattered_tm(t)

            # Advance the time by 1/2 time step
            t += 0.5 * self.dt

            # Update the canvas
            self._update_canvas()

            # Progress
            print('{} of {} time steps'.format(n + 1, self.number_of_time_steps))

    def eincident_te(self, t):
        """
        Calculate the incident electric field for TE mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident electric field and derivative
        delay = 0

        # Calculate the decay rate determined by Gaussian pulse width
        alpha = (1.0 / (self.dt * self.gaussian_pulse_width / 4.0)) ** 2

        # Calculate the period
        period = 2.0 * self.dt * self.gaussian_pulse_width

        # Spatial delay of each cell
        x_disp = -cos(radians(self.incident_angle))
        y_disp = -sin(radians(self.incident_angle))

        if x_disp < 0:
            delay -= x_disp * (self.nx - 2.0) * self.dx

        if y_disp < 0:
            delay -= y_disp * (self.ny - 2.0) * self.dy

        for i in range(self.number_of_pml, self.nx - self.number_of_pml):
            for j in range(self.number_of_pml, self.ny - self.number_of_pml):
                distance = i * self.dx * x_disp + j * self.dy * y_disp + delay
                a = 0
                a_prime = 0
                tau = t - distance / c

                if 0 <= tau <= period:
                    a = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2)
                    a_prime = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2) \
                              * (-2.0 * alpha * (tau - self.gaussian_pulse_width * self.dt))

                self.exi[i][j] = self.amplitude_x * a
                self.dexi[i][j] = self.amplitude_x * a_prime

                self.eyi[i][j] = self.amplitude_y * a
                self.deyi[i][j] = self.amplitude_y * a_prime

    def escattered_te(self, t):
        """
        Calculate the scattered electric field for TE mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident electric field
        self.eincident_te(t)

        # Update the x-component electric scattered field
        for i in range(self.nx - 1):
            for j in range(self.ny - 1):
                self.exs[i][j] = self.exs[i][j] * self.esctc[i][j] - self.eincc[i][j] * self.exi[i][j] \
                                 - self.edevcn[i][j] * self.dexi[i][j] + (self.hzs[i][j] - self.hzs[i][j - 1]) \
                                 * self.ecrly[i][j]

        # Update the y-component electric scattered field
        for i in range(1, self.nx - 1):
            for j in range(self.ny - 1):
                self.eys[i][j] = self.eys[i][j] * self.esctc[i][j] - self.eincc[i][j] * self.eyi[i][j] \
                                 - self.edevcn[i][j] * self.deyi[i][j] - (self.hzs[i][j] - self.hzs[i - 1][j]) \
                                 * self.ecrlx[i][j]

    def hincident_te(self, t):
        """
        Calculate the incident magnetic field for TE mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident magnetic field and time derivative
        delay = 0.0
        eta = sqrt(mu_0 / epsilon_0)

        # Calculate the decay rate determined by Gaussian pulse width
        alpha = (1.0 / (self.gaussian_pulse_width * self.dt / 4.0)) ** 2

        # Calculate the period
        period = 2.0 * self.gaussian_pulse_width * self.dt

        # Spatial delay of each cell
        x_disp = -cos(radians(self.incident_angle))
        y_disp = -sin(radians(self.incident_angle))

        if x_disp < 0:
            delay -= x_disp * (self.nx - 2.0) * self.dx

        if y_disp < 0:
            delay -= y_disp * (self.ny - 2.0) * self.dy

        for i in range(self.number_of_pml, self.nx - self.number_of_pml):
            for j in range(self.number_of_pml, self.ny - self.number_of_pml):
                distance = i * self.dx * x_disp + j * self.dy * y_disp + delay
                a_prime = 0
                tau = t - distance / c

                if 0 <= tau <= period:
                    a_prime = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2) \
                              * (-2.0 * alpha * (tau - self.gaussian_pulse_width * self.dt))

                self.dhzi[i][j] = self.gaussian_pulse_amplitude * a_prime / eta

    def hscattered_te(self, t):
        """
        Calculate the scattered magnetic field for TE mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident magnetic field
        self.hincident_te(t)

        # Update the scattered magnetic field
        for i in range(self.nx - 1):
            for j in range(self.ny - 1):
                self.hzs[i][j] = self.hzs[i][j] - (self.eys[i + 1][j] - self.eys[i][j]) * self.dtmdx[i][j] \
                                + (self.exs[i][j + 1] - self.exs[i][j]) * self.dtmdy[i][j] - self.hdhvcn[i][j] \
                                * self.dhzi[i][j]

    def eincident_tm(self, t):
        """
        Calculate the incident electric field for TM mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident electric field and derivative
        delay = 0

        # Calculate the decay rate determined by Gaussian pulse width
        alpha = (1.0 / (self.dt * self.gaussian_pulse_width / 4.0)) ** 2

        # Calculate the period
        period = 2.0 * self.dt * self.gaussian_pulse_width

        # Spatial delay of each cell
        x_disp = -cos(radians(self.incident_angle))
        y_disp = -sin(radians(self.incident_angle))

        if x_disp < 0:
            delay -= x_disp * (self.nx - 2.0) * self.dx

        if y_disp < 0:
            delay -= y_disp * (self.ny - 2.0) * self.dy

        for i in range(self.number_of_pml, self.nx - self.number_of_pml):
            for j in range(self.number_of_pml, self.ny - self.number_of_pml):
                distance = i * self.dx * x_disp + j * self.dy * y_disp + delay
                a = 0
                a_prime = 0
                tau = t - distance / c

                if 0 <= tau <= period:
                    a = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2)
                    a_prime = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2) \
                              * (-2.0 * alpha * (tau - self.gaussian_pulse_width * self.dt))

                self.ezi[i][j] = self.gaussian_pulse_amplitude * a
                self.dezi[i][j] = self.gaussian_pulse_amplitude * a_prime

    def escattered_tm(self, t):
        """
        Calculate the scattered electric field for TM mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident electric field
        self.eincident_tm(t)

        # Update the z-component electric scattered field
        for i in range(1, self.nx - 1):
            for j in range(1, self.ny - 1):
                self.ezs[i][j] = self.ezs[i][j] * self.esctc[i][j] - self.eincc[i][j] * self.ezi[i][j] \
                                 - self.edevcn[i][j] * self.dezi[i][j] + (self.hys[i][j] - self.hys[i - 1][j]) \
                                 * self.ecrlx[i][j] - (self.hxs[i][j] - self.hxs[i][j - 1]) * self.ecrly[i][j]

    def hincident_tm(self, t):
        """
        Calculate the incident magnetic field for TM mode.
        :param t: Time (s).
        :return:
        """
        # Calculate the incident magnetic field and derivative
        delay = 0
        eta = sqrt(mu_0 / epsilon_0)

        # Calculate the decay rate determined by Gaussian pulse width
        alpha = (1.0 / (self.dt * self.gaussian_pulse_width / 4.0)) ** 2

        # Calculate the period
        period = 2.0 * self.dt * self.gaussian_pulse_width

        # Spatial delay of each cell
        x_disp = -cos(radians(self.incident_angle))
        y_disp = -sin(radians(self.incident_angle))

        if x_disp < 0:
            delay -= x_disp * (self.nx - 2.0) * self.dx

        if y_disp < 0:
            delay -= y_disp * (self.ny - 2.0) * self.dy

        for i in range(self.number_of_pml, self.nx - self.number_of_pml):
            for j in range(self.number_of_pml, self.ny - self.number_of_pml):
                distance = i * self.dx * x_disp + j * self.dy * y_disp + delay
                a = 0
                a_prime = 0
                tau = t - distance / c

                if 0 <= tau <= period:
                    a = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2)
                    a_prime = exp(-alpha * (tau - self.gaussian_pulse_width * self.dt) ** 2) \
                              * (-2.0 * alpha * (tau - self.gaussian_pulse_width * self.dt))

                self.dhxi[i][j] = self.gaussian_pulse_amplitude * a_prime / eta
                self.dhyi[i][j] = self.gaussian_pulse_amplitude * a_prime / eta

    def hscattered_tm(self, t):
        """
        Calculate the scattered magnetic field for TM mode.
        :param t:
        :return:
        """
        # Calculate the incident magnetic field
        self.hincident_tm(t)

        # Update the X component of the magnetic scattered field
        for i in range(1, self.nx - 1):
            for j in range(self.ny - 1):
                self.hxs[i][j] = self.hxs[i][j] - (self.ezs[i][j + 1] - self.ezs[i][j]) * self.dtmdx[i][j]

        for i in range(self.nx - 1):
            for j in range(1, self.ny - 1):
                self.hys[i][j] = self.hys[i][j] + (self.ezs[i + 1][j] - self.ezs[i][j]) * self.dtmdx[i][j]

    def _update_canvas(self):
        # Remove the color bar
        try:
            self.cbar.remove()
        except:
            print('Initial Plot')

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Calculate the total field for plotting
        etotal = zeros([self.nx, self.ny])

        if self.mode == 'TM':
            for i in range(self.nx):
                for j in range(self.ny):
                    etotal[i][j] = self.ezi[i][j] + self.ezs[i][j]
        else:
            for i in range(self.nx):
                for j in range(self.ny):
                    extotal = self.exi[i][j] + self.exs[i][j]
                    eytotal = self.eyi[i][j] + self.eys[i][j]
                    etotal[i][j] = sqrt(extotal ** 2 + eytotal ** 2)

        # x and y grid for plotting
        x = linspace(0, self.nx * self.dx, self.nx)
        y = linspace(0, self.ny * self.dy, self.ny)

        x_grid, y_grid = meshgrid(x, y)

        # Display the results
        im = self.axes1.pcolor(x_grid, y_grid, abs(etotal), cmap="jet", vmin=0, vmax=self.gaussian_pulse_amplitude)
        self.cbar = self.fig.colorbar(im, ax=self.axes1, orientation='vertical')
        self.cbar.set_label('Electric Field (V/m)', size=10)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Update the canvas
        self.my_canvas.draw()
        self.my_canvas.flush_events()


def start():
    form = FDTD()  # Set the form
    form.show()    # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = FDTD()                 # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
