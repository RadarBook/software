"""
Project: RadarBook
File: stratified_sphere.py
Created by: Lee A. Harrison
One: 10/20/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import sqrt, zeros, array, sin, cos, radians
from scipy.constants import pi, c, epsilon_0, mu_0
from scipy.special import spherical_jn, spherical_yn


def radar_cross_section(frequency, theta, phi, An, Bn):
    """
    Calculate the radar cross section for a stratified sphere.
    :param frequency: The frequency of the incident wave (Hz).
    :param theta: The observation angle theta (rad).
    :param phi: The observation angle phi (rad).
    :param An: Scattering coefficient.
    :param Bn:Scattering coefficient.
    :return: The radar cross section for a stratified sphere.
    """
    # Wavelength
    wavelength = c / frequency

    # Wavenumber
    k = 2.0 * pi / wavelength

    st = abs(sin(theta))
    ct = cos(theta)

    # Associated Legendre Polynomial
    p_lm = zeros(len(An) + 1)
    p_lm[0] = -st
    p_lm[1] = -3.0 * st * ct

    s1 = 0
    s2 = 0

    p = p_lm[0]

    for i_mode in range(1, len(An) + 1):
        # Derivative of associated Legendre Polynomial
        if abs(ct) < 0.999999999:
            if i_mode == 1:
                dp = ct * p_lm[0] / sqrt(1.0 - ct ** 2)
            else:
                dp = (i_mode * ct * p_lm[i_mode - 1] - (i_mode + 1.0) * p_lm[i_mode - 2]) / sqrt(1.0 - ct ** 2)

        if st > 1.0e-9:
            t1 = An[i_mode - 1] * p / st
            t2 = Bn[i_mode - 1] * p / st

        if ct > 0.999999999:
            val = 1j ** (i_mode - 1) * (i_mode * (i_mode + 1.0) / 2.0) * (An[i_mode - 1] - 1j * Bn[i_mode - 1])
            s1 += val
            s2 += val
        elif ct < -0.999999999:
            val = (-1j) ** (i_mode - 1) * (i_mode * (i_mode + 1.0) / 2.0) * (An[i_mode - 1] + 1j * Bn[i_mode - 1])
            s1 += val
            s2 -= val
        else:
            s1 += 1j ** (i_mode + 1) * (t1 - 1j * Bn[i_mode - 1] * dp)
            s2 += 1j ** (i_mode + 1) * (An[i_mode - 1] * dp - 1j * t2)

        # Recurrence relationship for nex Associated Legendre Polynomial
        if i_mode > 1:
            p_lm[i_mode] = (2.0 * i_mode + 1.0) * ct * p_lm[i_mode - 1] / i_mode - (i_mode + 1.0) * p_lm[i_mode - 2] / i_mode

        p = p_lm[i_mode]

    rcs_th = s1 * cos(phi) * sqrt(4.0 * pi) / k
    rcs_ph = -s2 * sin(phi) * sqrt(4.0 * pi) / k

    return rcs_th, rcs_ph


def coefficients(frequency, epsilon, mu, radius, number_of_modes, pec):
    """
    Calculate the scattering coefficients for a stratified sphere.
    :param frequency: The frequency of the incident wave (Hz).
    :param epsilon: The relative permittivity of the layers.
    :param mu: The relative permeability of the layers.
    :param radius: The radius of each layer.
    :param number_of_modes: The number of modes to calculate.
    :param pec: True for PEC core.
    :return: The scattering coefficients for a stratified sphere.
    """
    # Wavenumber
    k = 2.0 * pi * frequency / c

    # Free space impedance
    eta_0 = sqrt(mu_0 / epsilon_0)

    # Interfaces
    number_of_interfaces = len(mu)

    An = zeros(number_of_modes, dtype=complex)
    Bn = zeros(number_of_modes, dtype=complex)

    z = zeros([number_of_interfaces, number_of_modes], dtype=complex)
    y = zeros([number_of_interfaces, number_of_modes], dtype=complex)

    modes = range(1, number_of_modes + 1)

    # Loop over the interfaces
    for i_layer in range(number_of_interfaces-2, -1, -1):
        eta_i = sqrt(mu[i_layer + 1] / epsilon[i_layer + 1]) * eta_0
        m = sqrt(mu[i_layer + 1] * epsilon[i_layer + 1])

        if i_layer == number_of_interfaces - 2:

            if not pec:
                za = k * m * radius[i_layer]
                p = [spherical_j(n, za) / spherical_j(n, za, True) for n in modes]

                z[i_layer] = [ip * eta_i for ip in p]
                y[i_layer] = [ip / eta_i for ip in p]

        else:
            z1 = m * k * radius[i_layer]
            z2 = m * k * radius[i_layer + 1]

            j1 = array([spherical_j(n, z1) for n in modes])
            j2 = array([spherical_j(n, z2) for n in modes])

            j1p = array([spherical_j(n, z1, True) for n in modes])
            j2p = array([spherical_j(n, z2, True) for n in modes])

            h1 = array([spherical_h(n, 2, z1) for n in modes])
            h2 = array([spherical_h(n, 2, z2) for n in modes])

            h1p = array([spherical_h(n, 2, z1, True) for n in modes])
            h2p = array([spherical_h(n, 2, z2, True) for n in modes])

            u = (j2p * h1p) / (j1p * h2p)

            v = (j2 * h1) / (j1 * h2)

            p1 = j1 / j1p

            p2 = j2 / j2p

            q2 = h2 / h2p

            if i_layer == number_of_interfaces - 3 and pec:
                z[i_layer] = (eta_i * p1 * (1.0 - v)) / (1.0 - u * p2 / q2)
                y[i_layer] = (p1 / eta_i) * (1.0 - v * q2 / p2) / (1.0 - u)

            else:
                t1 = 1.0 - z[i_layer + 1] / (eta_i * q2)
                t2 = 1.0 - z[i_layer + 1] / (eta_i * p2)
                z[i_layer] = eta_i * p1 * (1.0 - v * t2 / t1)

                t1 = 1.0 - eta_i * q2 / z[i_layer + 1]
                t2 = 1.0 - eta_i * p2 / z[i_layer + 1]
                z[i_layer] /= (1.0 - u * t2 / t1)

                t1 = 1.0 - eta_i * y[i_layer + 1] / q2
                t2 = 1.0 - eta_i * y[i_layer + 1] / p2
                y[i_layer] = (p1 / eta_i) * (1.0 - v * t2 / t1)

                t1 = 1.0 - q2 / (eta_i * y[i_layer + 1])
                t2 = 1.0 - p2 / (eta_i * y[i_layer + 1])
                y[i_layer] /= (1.0 - u * t2 / t1)

    Zn = 1j * z[0] / eta_0
    Yn = 1j * y[0] * eta_0

    z = k * radius[0]

    for n in modes:
        jn = spherical_j(n, z)
        jp = spherical_j(n, z, True)

        hn = spherical_h(n, 2, z)
        hp = spherical_h(n, 2, z, True)

        An[n - 1] = -(1j ** n) * (2.0 * n + 1.0) / (n * (n + 1.0)) * (jn + 1j * Zn[n - 1] * jp) / \
                    (hn + 1j * Zn[n - 1] * hp)

        Bn[n - 1] = 1j ** (n + 1) * (2.0 * n + 1.0) / (n * (n + 1.0)) * (jn + 1j * Yn[n - 1] * jp) / \
                    (hn + 1j * Yn[n - 1] * hp)

    return An, Bn


def spherical_j(mode, z, derivative=False):
    """
    Calculate the spherical Bessel function or derivatives.
    :param mode: The mode.
    :param z: The argument.
    :param derivative: True for derivatives.
    :return: The spherical Bessel function or derivatives.
    """
    if derivative:
        return z * spherical_jn(mode - 1, z) - mode * spherical_jn(mode, z)
    else:
        return z * spherical_jn(mode, z)


def spherical_h(mode, kind, z, derivative=False):
    """
    Calculate the spherical Hankel function or derivatives.
    :param mode: The mode.
    :param kind: First or second kind.
    :param z: The argument.
    :param derivative: True for derivatives.
    :return: The spherical Hankel function or derivative.
    """
    if derivative:
        return spherical_h(mode - 1, kind, z) - mode * spherical_h(mode, kind, z) / z
    else:
        if kind == 1:
            return z * (spherical_jn(mode, z) + 1j * spherical_yn(mode, z))
        else:
            return z * (spherical_jn(mode, z) - 1j * spherical_yn(mode, z))
