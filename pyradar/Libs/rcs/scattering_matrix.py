"""
Project: RadarBook
File: scattering_matrix.py
Created by: Lee A. Harrison
On: 10/19/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import array, zeros, pi, sin, cos, exp, cross, sum, sqrt, dot, arctan2, arccos, sign
from scipy.constants import c
from scipy.linalg import norm


class ScatteringMatrix(object):
    """
    Calculate the normalized scattering matrix
    """
    def __init__(self, theta_inc=0.0, phi_inc=0.0, theta_obs=0.0, phi_obs=0.0, frequency=array([10.0e9]),
                 vertices=array([[10.0, 10.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 0.0], [10.0, 0.0, 0.0]]),
                 faces=array([[0, 1, 2], [2, 3, 0]])):

        # Incident and observation angles
        self.theta_inc = theta_inc
        self.phi_inc = phi_inc
        self.theta_obs = theta_obs
        self.phi_obs = phi_obs

        # List of frequencies
        self.frequency = frequency

        # Target geometry
        self.vertices = vertices
        self.faces = faces

    def get_scattering_matrix(self):
        """
        Calculates the normalized scattering matrix
        Scattering matrix is calculated in linear polarization [VV, HV, VH, HH]
        If needed, convert to circular [RR, LR, RL, LL] with linear_to_circular.
        """
        # Size the scattering matrix
        scattering_matrix = zeros((4, len(self.frequency)), dtype=complex)

        # Wavelength
        wavelength = c / self.frequency

        # Wavenumber
        k = 2.0 * pi / wavelength

        # Number of vertices and faces
        nv = self.vertices.shape[0]
        nf = self.faces.shape[0]

        # Incident angles and direction cosines
        cpi = cos(self.phi_inc)
        spi = sin(self.phi_inc)
        cti = cos(self.theta_inc)
        sti = sin(self.theta_inc)

        ui = sti * cpi
        vi = sti * spi
        wi = cti

        incident_direction = [ui, vi, wi]

        # Observation angles and direction cosines
        cpo = cos(self.phi_obs)
        spo = sin(self.phi_obs)
        cto = cos(self.theta_obs)
        sto = sin(self.theta_obs)

        uo = sto * cpo
        vo = sto * spo
        wo = cto

        uuo = cto * cpo
        vvo = cto * spo
        wwo = -sto

        # Incident field in global Cartesian
        Ei = 1.0
        Ei_V = [cti * cpi * Ei, cti * spi * Ei, -sti * Ei]
        Ei_H = [-spi * Ei, cpi * Ei, 0.0]

        # Position vectors to vertices
        r = zeros((nv, 3))
        for i_vert in range(nv):
            r[i_vert] = [self.vertices[i_vert][0], self.vertices[i_vert][1], self.vertices[i_vert][2]]

        # Edge vectors and normals
        # Loop over faces
        for i_face in range(nf):
            A = r[self.faces[i_face][1]] - r[self.faces[i_face][0]]
            B = r[self.faces[i_face][2]] - r[self.faces[i_face][1]]
            C = r[self.faces[i_face][0]] - r[self.faces[i_face][2]]

            # Outward directed normals
            normal = cross(A, B) + 0.

            # Edge lengths
            dist = [norm(A), norm(B), norm(C)]

            ss = 0.5 * sum(dist)
            area = sqrt(ss * (ss - dist[0]) * (ss - dist[1]) * (ss - dist[2]))

            # Unit normals
            normal = normal / norm(normal)

            # Just a normal check for illumination
            if dot(normal, incident_direction) >= 0.0:

                # Local angles
                beta = arccos(normal[2])
                alpha = arctan2(normal[1] + 0., normal[0] + 0.)

                # Local direction cosines
                ca = cos(alpha)
                sa = sin(alpha)
                cb = cos(beta)
                sb = sin(beta)

                # Rotation matrices
                rotation1 = array([[ca, sa, 0.0], [-sa, ca, 0.0], [0.0, 0.0, 1.0]])
                rotation2 = array([[cb, 0.0, -sb], [0.0, 1.0, 0.0], [sb, 0.0, cb]])

                # Transform incident direction
                [ui_t, vi_t, wi_t] = rotation2.dot(rotation1.dot(incident_direction))

                sti_t = sqrt(ui_t * ui_t + vi_t * vi_t) * sign(wi_t)
                cti_t = sqrt(1.0 - sti_t * sti_t)
                
                phi_t = arctan2(vi_t + 0., ui_t + 0.)
                cpi_t = cos(phi_t)
                spi_t = sin(phi_t)

                # Phase at the three vertices
                v1, v2, v3 = self.faces[i_face][0], self.faces[i_face][1], self.faces[i_face][2]

                alpha1 = k * ((self.vertices[v1][0]) * (uo + ui) +
                              (self.vertices[v1][1]) * (vo + vi) +
                              (self.vertices[v1][2]) * (wo + wi))

                alpha2 = k * ((self.vertices[v2][0] - self.vertices[v1][0]) * (uo + ui) +
                              (self.vertices[v2][1] - self.vertices[v1][1]) * (vo + vi) +
                              (self.vertices[v2][2] - self.vertices[v1][2]) * (wo + wi)) + alpha1

                alpha3 = k * ((self.vertices[v3][0] - self.vertices[v1][0]) * (uo + ui) +
                              (self.vertices[v3][1] - self.vertices[v1][1]) * (vo + vi) +
                              (self.vertices[v3][2] - self.vertices[v1][2]) * (wo + wi)) + alpha1

                exp1 = exp(1j * alpha1)
                exp2 = exp(1j * alpha2)
                exp3 = exp(1j * alpha3)

                # Incident field in local Cartesian
                Ei_V2 = rotation2.dot(rotation1.dot(Ei_V))
                Ei_H2 = rotation2.dot(rotation1.dot(Ei_H))

                # Incident field in local Spherical
                Et_v = Ei_V2[0] * cti_t * cpi_t + Ei_V2[1] * cti_t * spi_t - Ei_V2[2] * sti_t
                Ep_v = -Ei_V2[0] * spi_t + Ei_V2[1] * cpi_t

                Et_h = Ei_H2[0] * cti_t * cpi_t + Ei_H2[1] * cti_t * spi_t - Ei_H2[2] * sti_t
                Ep_h = -Ei_H2[0] * spi_t + Ei_H2[1] * cpi_t

                # Reflection coefficients
                #Rs = 0.001
                Rs = 0.0
                gamma_perpendicular = -1.0 / (2.0 * Rs * cti_t + 1.0)
                gamma_parallel = 0.0
                if (2.0 * Rs + cti_t) != 0.0:
                    gamma_parallel = -cti_t / (2.0 * Rs + cti_t)

                # Surface currents in local Cartesian
                Jx_v = -Et_v * cpi_t * gamma_parallel + Ep_v * spi_t * cti_t * gamma_perpendicular
                Jy_v = -Et_v * spi_t * gamma_parallel - Ep_v * cpi_t * cti_t * gamma_perpendicular

                Jx_h = -Et_h * cpi_t * gamma_parallel + Ep_h * spi_t * cti_t * gamma_perpendicular
                Jy_h = -Et_h * spi_t * gamma_parallel - Ep_h * cpi_t * cti_t * gamma_perpendicular

                # Now loop over all the frequencies
                for i_freq in range(len(self.frequency)):

                    # Area integral
                    Ic = surface_integral(alpha1[i_freq], alpha2[i_freq], alpha3[i_freq], exp1[i_freq],
                                          exp2[i_freq], exp3[i_freq], area)

                    # Scattered field components in local coordinates
                    Es2_v = [Jx_v * Ic, Jy_v * Ic, 0.0]
                    Es2_h = [Jx_h * Ic, Jy_h * Ic, 0.0]

                    # Transform back to global coordinates
                    Es_v = rotation1.T.dot(rotation2.T.dot(Es2_v))
                    Es_h = rotation1.T.dot(rotation2.T.dot(Es2_h))

                    Ev_v = uuo * Es_v[0] + vvo * Es_v[1] + wwo * Es_v[2]
                    Eh_v = -spo * Es_v[0] + cpo * Es_v[1]

                    Ev_h = uuo * Es_h[0] + vvo * Es_h[1] + wwo * Es_h[2]
                    Eh_h = -spo * Es_h[0] + cpo * Es_h[1]

                    # Set the scattering matrix
                    scattering_matrix[0][i_freq] += Ev_v
                    scattering_matrix[1][i_freq] += Ev_h
                    scattering_matrix[2][i_freq] += Eh_v
                    scattering_matrix[3][i_freq] += Eh_h

        return scattering_matrix * sqrt(4.0 * pi) / wavelength


def surface_integral(alpha1, alpha2, alpha3, exp1, exp2, exp3, area):
    """
    Calculate the surface integral, special cases for each vertex phase term.
    :param alpha1: The phase at vertex 1 (rad).
    :param alpha2: The phase at vertex 2 (rad).
    :param alpha3: The phase at vertex 3 (rad).
    :param exp1: The exponential term (exp(j k alhpa1).
    :param exp2: The exponential term (exp(j k alpha2).
    :param exp3: The exponential term (exp(j k alpha3).
    :param area: The area of the facet (m^2).
    :return: The surface integral calculation.
    """
    eps = 1e-10
    if abs(alpha1 - alpha2) < eps and abs(alpha1 - alpha3) < eps:
        Ic = area * exp1
    elif abs(alpha1 - alpha2) < eps:
        Ic = 2.0 * area / (alpha3 - alpha2) * (1j * exp1 - (exp1 - exp3) / (alpha1 - alpha3))
    elif abs(alpha1 - alpha3) < eps:
        Ic = 2.0 * area / (alpha3 - alpha2) * (-1j * exp1 + (exp1 - exp2) / (alpha1 - alpha2))
    elif abs(alpha2 - alpha3) < eps:
        Ic = 2.0 * area / (alpha1 - alpha2) * (1j * exp3 - (exp1 - exp3) / (alpha1 - alpha3))
    else:
        Ic = 2.0 * area / (alpha3 - alpha2) * ((exp1 - exp2) / (alpha1 - alpha2) - (exp1 - exp3) / (alpha1 - alpha3))
    return Ic
