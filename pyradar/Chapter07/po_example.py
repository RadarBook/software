"""
Project: RadarBook
File: po_example.py
Created by: Lee A. Harrison
On: 11/21/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter07.ui.PO_ui import Ui_MainWindow
from numpy import log10, linspace, radians, degrees, array
from Libs.rcs import scattering_matrix, display_facet_model
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PO(QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(self.__class__, self).__init__()

        self.setupUi(self)

        self.a = scattering_matrix
        self.d = display_facet_model

        # Default model load and settings
        self.model, self.vertices, self.faces = self.d.read_facet_model('plate.facet')

        # Connect to the input boxes, when the user presses enter the form updates
        self.select_target.currentIndexChanged.connect(self._select_target)
        self.view_target.clicked.connect(self._view_target)

        # Set up a figure for the plotting canvas
        fig = Figure() 
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for display
        self.run_po.clicked.connect(self._update_canvas)

    def _select_target(self):
        # Read the target geometry
        target = self.select_target.currentText()

        if target == 'Rectangular Plate':
            self.model, self.vertices, self.faces = self.d.read_facet_model('plate.facet')
        elif target == 'Circular Cone':
            self.model, self.vertices, self.faces = self.d.read_facet_model('cone.facet')
        elif target == 'Frustum':
            self.model, self.vertices, self.faces = self.d.read_facet_model('frustum.facet')
        elif target == 'Double Ogive':
            self.model, self.vertices, self.faces = self.d.read_facet_model('double_ogive.facet')

    def _view_target(self):
        # Display the target geometry

        # Normals
        n = False
        if self.normals.currentText() == 'On':
            n = True

        self.d.display_facet(self.model, self.vertices, self.faces, self.facet_type.currentText(), n)

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        frequency = float(self.frequency.text())
        theta_inc = float(self.theta_inc.text())
        phi_inc = float(self.phi_inc.text())
        phi_obs = float(self.phi_obs.text())

        # Set the scattering angles
        theta = self.theta_obs.text().split(',')
        theta_obs = linspace(radians(float(theta[0])), radians(float(theta[1])), 721)

        # Monostatic or bistatic
        mb = self.type.currentText()

        rcs_theta = []
        rcs_phi = []

        kwargs = {'frequency': array([frequency]),
                  'vertices':  self.vertices,
                  'faces':     self.faces,
                  'phi_inc':   radians(phi_inc),
                  'phi_obs':   radians(phi_obs)}

        b = scattering_matrix.ScatteringMatrix(**kwargs)

        if mb == 'Monostatic':

            for to in theta_obs:

                b.theta_inc = to
                b.theta_obs = to

                sm = b.get_scattering_matrix()

                rcs_theta.append(20.0 * log10(abs(sm[0]) + 1e-10))
                rcs_phi.append(20.0 * log10(abs(sm[3]) + 1e-10))

        else:

            b.theta_inc = radians(theta_inc)

            for to in theta_obs:

                b.theta_obs = to

                sm = b.get_scattering_matrix()

                rcs_theta.append(20.0 * log10(abs(sm[0]) + 1e-10))
                rcs_phi.append(20.0 * log10(abs(sm[3]) + 1e-10))

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(degrees(theta_obs), rcs_phi, '', label='TE$^z$')
        self.axes1.plot(degrees(theta_obs), rcs_theta, '--', label='TM$^z$')

        # Set the plot title and labels
        self.axes1.set_title('Physical Optics RCS vs Observation Angle', size=14)
        self.axes1.set_ylabel('RCS (dBsm)', size=12)
        self.axes1.set_xlabel('Observation Angle (deg)', size=12)
        self.axes1.set_ylim(-40, max(rcs_theta) + 3)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Set the legend
        self.axes1.legend(loc='best', prop={'size': 10})

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start():
    form = PO()  # Set the form
    form.show()  # Show the form


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = PO()                   # Set the form
    form.show()                   # Show the form
    app.exec_()                   # Execute the app


if __name__ == '__main__':
    main()
