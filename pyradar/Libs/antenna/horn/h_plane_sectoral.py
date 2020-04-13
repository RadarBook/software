"""
Project: RadarBook
File: h_plane_sectoral.py
Created by: Lee A. Harrison
On: 7/6/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy import exp, sin, cos, sqrt, sinc
from scipy.constants import c, epsilon_0, mu_0, pi
from scipy.special import fresnel


def aperture_fields(horn_width, horn_effective_length, frequency, x, y):
    """
    Calculate the electric field at the aperture of the horn.
    Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
    And that the horn length is large compared to the dimensions of the waveguide.
    :param x: The x coordinate to calculate the field in the aperture (m).
    :param y: The y coordinate to calculate the field in the aperture (m).
    :param horn_width: The width of the horn (m).
    :param horn_effective_length: The effective length of the horn (m).
    :param frequency: The operating frequency (Hz).
    :return: The electric and magnetic fields in the aperture (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the x-component of the electric field
    e_x = 0.0

    # Define the y-component of the electric field
    e_y = cos(pi * x / horn_width) * exp(-1j * k * 0.5 * (x ** 2 / horn_effective_length))

    # Define the z-component of the electric field
    e_z = 0.0

    # Define the x-component of the magnetic field
    h_x = -cos(pi * x / horn_width) / eta * exp(-1j * k * 0.5 * (x ** 2 / horn_effective_length))

    # Define the y-component of the magnetic field
    h_y = 0.0

    # Define the z-component of the magnetic field
    h_z = 0.0

    # Return all six components of the aperture field
    return e_x, e_y, e_z, h_x, h_y, h_z


def far_fields(guide_height, horn_width, horn_effective_length, frequency, r, theta, phi):
    """
    Calculate the electric and magnetic fields in the far field of the horn.
    :param r: The distance to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param guide_height: The height of the waveguide feed (m).
    :param horn_width: The width of the horn (m).
    :param horn_effective_length: The effective length of the horn (m).
    :param frequency: The operating frequency (Hz).
    :return: The electric and magnetic fields radiated by the horn (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the radial-component of the electric field
    e_r = 0.0

    # Define the theta-component of the electric field
    e_theta = sin(phi) * (1.0 + cos(theta)) * sinc(k * guide_height * 0.5 * sin(theta) * sin(phi)) * \
              I(k, r, theta, phi, horn_width, guide_height, horn_effective_length)

    # Define the phi-component of the electric field
    e_phi = cos(phi) * (1.0 + cos(theta)) * sinc(k * guide_height * 0.5 * sin(theta) * sin(phi)) *\
            I(k, r, theta, phi, horn_width, guide_height, horn_effective_length)

    # Define the radial-component of the magnetic field
    h_r = 0.0

    # Define the theta-component of the magnetic field
    h_theta = -cos(phi) / eta * (1.0 + cos(theta)) * sinc(k * guide_height * 0.5 * sin(theta) * sin(phi)) * \
              I(k, r, theta, phi, horn_width, guide_height, horn_effective_length)

    # Define the phi-component of the magnetic field
    h_phi = sin(phi) / eta * (1.0 + cos(theta)) * sinc(k * guide_height * 0.5 * sin(theta) * sin(phi)) * \
            I(k, r, theta, phi, horn_width, guide_height, horn_effective_length)

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi


def directivity(guide_height, horn_width, horn_effective_length, frequency):
    """
    Calculate the directivity for the H-plane horn.
    :param guide_height: The height of the waveguide feed (m).
    :param horn_width: The width of the horn (m).
    :param horn_effective_length: The effective length of the horn (m).
    :param frequency: The operating frequency (Hz).
    :return: The directivity for the H-plane horn.
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Calculate the arguments for the Fresnel integrals
    u = 1.0 / sqrt(2.0) * (sqrt(wavelength * horn_effective_length) / horn_width
                           + horn_width / sqrt(wavelength + horn_effective_length))

    v = 1.0 / sqrt(2.0) * (sqrt(wavelength * horn_effective_length) / horn_width
                           - horn_width / sqrt(wavelength + horn_effective_length))

    # Calculate the Fresnel integrals
    Cu, Su = fresnel(u)
    Cv, Sv = fresnel(v)

    return 4.0 * pi * guide_height * horn_effective_length / (horn_width * wavelength) * \
           ((Cu - Cv) ** 2 + (Su - Sv) ** 2)


def power_radiated(guide_height, horn_width):
    """
    Calculate the normalized power radiated by the H-plane horn.
    :param guide_height: The height of the waveguide feed (m).
    :param horn_width: The width of the horn (m).
    :return: The power radiated by the H-plane horn (normalized by |E0|^2) (W).
    """
    return horn_width * guide_height / (4.0 * sqrt(mu_0 / epsilon_0))


def I(k, r, theta, phi, horn_width, guide_height, horn_effective_length):
    """
    Calculate the integral used in the far field calculation.
    :param k: The wavenumber (rad/m).
    :param r: The distance to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param horn_width: The width of the horn (m).
    :param guide_height: The height of the waveguide feed (m).
    :param horn_effective_length: The effective length of the horn (m).
    :return: The integral used in far field calculations.
    """
    # Calculate the wavenumber prime and double prime terms
    kx_p = k * sin(theta) * cos(phi) + pi / horn_width
    kx_m = k * sin(theta) * cos(phi) - pi / horn_width

    # Phase terms for prime and double prime terms
    f1 = kx_p * kx_p * horn_effective_length / (2.0 * k)
    f2 = kx_m * kx_m * horn_effective_length / (2.0 * k)

    # Arguments of the Fresnel integrals for prime and double prime terms
    t1_p = sqrt(1.0 / (pi * k * horn_effective_length)) * (-k * horn_width * 0.5 - kx_p * horn_effective_length)
    t2_p = sqrt(1.0 / (pi * k * horn_effective_length)) * ( k * horn_width * 0.5 - kx_p * horn_effective_length)

    t1_m = sqrt(1.0 / (pi * k * horn_effective_length)) * (-k * horn_width * 0.5 - kx_m * horn_effective_length)
    t2_m = sqrt(1.0 / (pi * k * horn_effective_length)) * ( k * horn_width * 0.5 - kx_m * horn_effective_length)

    # Calculate the Fresnel sin and cos integrals
    s1p, c1p = fresnel(t1_p)
    s2p, c2p = fresnel(t2_p)

    s1m, c1m = fresnel(t1_m)
    s2m, c2m = fresnel(t2_m)

    return 1j * guide_height * sqrt(k * horn_effective_length / pi) / (8.0 * r) * exp(-1j * k * r) * \
           (((c2p - c1p) - 1j * (s2p - s1p)) * exp(1j * f1) + ((c2m - c1m) - 1j * (s2m - s1m)) * exp(1j * f2))
