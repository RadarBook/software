"""
Project: RadarBook
File: pyramidal.py
Created by: Lee A. Harrison
On: 7/6/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from scipy.constants import c, mu_0, epsilon_0, pi
from numpy import sqrt, sin, cos, exp
from scipy.special import fresnel


def aperture_fields(horn_width, eplane_effective_length, hplane_effective_length, frequency, x, y):
    """
    Calculate the electric field at the aperture of the horn.
    Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
    And that the horn length is large compare to the dimensions of the waveguide.
    :param x: The x coordinate to calculate the field in the aperture (m).
    :param y: The y coordinate to calculate the field in the aperture (m).
    :param horn_width: The width of the horn (m).
    :param eplane_effective_length: The horn effective length in the E-plane (m).
    :param hplane_effective_length: The horn effective length in the H-plane (m).
    :param frequency: The operating frequency (Hz).
    :return: The electric and magnetic fields at the horn aperture (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the x-component of the electric field
    e_x = 0.0

    # Define the y-component of the electric field
    e_y = cos(pi * x / horn_width) * exp(-1j * k * 0.5 * (x ** 2 / hplane_effective_length +
                                                          y ** 2 / eplane_effective_length))

    # Define the z-component of the electric field
    e_z = 0.0

    # Define the x-component of the magnetic field
    h_x = -cos(pi * x / horn_width) / eta * exp(-1j * k * 0.5 * (x ** 2 / hplane_effective_length +
                                                                 y ** 2 / eplane_effective_length))

    # Define the y-component of the magnetic field
    h_y = 0.0

    # Define the z-component of the magnetic field
    h_z = 0.0

    # Return all six components of the aperture field
    return e_x, e_y, e_z, h_x, h_y, h_z


def far_fields(horn_width, horn_height, eplane_effective_length, hplane_effective_length, frequency, r, theta, phi):
    """
    Calculate the electric and magnetic fields in the far field of the horn.
    :param r: The distance to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param horn_width: The width of the horn (m).
    :param horn_height: The height of the horn (m).
    :param eplane_effective_length: The horn effective length in the E-plane (m).
    :param hplane_effective_length: The horn effective length in the H-plane (m).
    :param frequency: The operating frequency (Hz).
    :return: THe electric and magnetic fields radiated by the horn (V/m), (A/m).
    """
    # Calculate the wavenumber
    k = 2.0 * pi * frequency / c

    # Calculate the wave impedance
    eta = sqrt(mu_0 / epsilon_0)

    # Define the radial-component of the electric field
    e_r = 0.0

    # Define the theta-component of the electric field
    e_theta = 1j * k / (4.0 * pi * r) * exp(-1j * k * r) * sin(phi) * (1.0 + cos(theta)) * \
              I1(k, horn_width, hplane_effective_length, theta, phi) * \
              I2(k, horn_height, eplane_effective_length, theta, phi)

    # Define the phi-component of the electric field
    e_phi = 1j * k / (4.0 * pi * r) * exp(-1j * k * r) * cos(phi) * (1.0 + cos(theta)) * \
              I1(k, horn_width, hplane_effective_length, theta, phi) * \
              I2(k, horn_height, eplane_effective_length, theta, phi)

    # Define the radial-component of the magnetic field
    h_r = 0.0

    # Define the theta-component of the magnetic field
    h_theta = 1j * k / (4.0 * pi * r) * exp(-1j * k * r) * -cos(phi) * (1.0 + cos(theta)) / eta * \
              I1(k, horn_width, hplane_effective_length, theta, phi) * \
              I2(k, horn_height, eplane_effective_length, theta, phi)

    # Define the phi-component of the magnetic field
    h_phi = 1j * k / (4.0 * pi * r) * exp(-1j * k * r) * sin(phi) * (1.0 + cos(theta)) / eta * \
            I1(k, horn_width, hplane_effective_length, theta, phi) * \
            I2(k, horn_height, eplane_effective_length, theta, phi)

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi


def directivity(horn_width, horn_height, eplane_effective_length, hplane_effective_length, frequency):
    """
    Calculate the directivity for a pyramidal horn.
    :param horn_width: The width of the horn (m).
    :param horn_height: The height of the horn (m).
    :param eplane_effective_length: The horn effective length in the E-plane (m).
    :param hplane_effective_length: The horn effective length in the H-plane (m).
    :param frequency: The operating frequency (Hz).
    :return: The directivity of the pyramidal horn.
    """
    # Calculate the wavelength
    wavelength = c / frequency
    
    # Calculate the arguments for the Fresnel integrals
    u = 1.0 / sqrt(2.0) * (sqrt(wavelength * hplane_effective_length) / horn_width + 
                           horn_width / sqrt(wavelength * hplane_effective_length))

    v = 1.0 / sqrt(2.0) * (sqrt(wavelength * hplane_effective_length) / horn_width - horn_width /
                           sqrt(wavelength * hplane_effective_length))

    # Calculate the Fresnel sin and cos integrals
    Su, Cu = fresnel(u)
    Sv, Cv = fresnel(v)

    arg = horn_height / sqrt(2.0 * wavelength * eplane_effective_length)

    S2, C2 = fresnel(arg)

    S2 *= S2
    C2 *= C2

    return 8.0 * pi * eplane_effective_length * hplane_effective_length / (horn_width * horn_height) * \
           ((Cu - Cv) ** 2 + (Su - Sv) ** 2) * (C2 + S2)


def power_radiated(horn_width, horn_height):
    """
    Calculate the normalized power radiated by the pyramidal horn.
    :param horn_width: The width of the horn (m).
    :param horn_height: The height of the horn (m).
    :return: The power radiated by the pyramidal horn (normalized by |E0|^2) (W).
    """
    # Calculate the normalized power radiated
    return horn_width * horn_height / (4.0 * 120.0 * pi)


def I1(k, horn_width, hplane_effective_length, theta, phi):
    """
    Calculate the integral used for far field calculations.
    :param k: The wavenumber (rad/m).
    :param horn_width: The width of the horn (m).
    :param hplane_effective_length: The horn effective length in the H-plane (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :return: The integral used for far field calculations.
    """
    # Calculate the x-component of the wavenumber primed
    kx_p = k * sin(theta) * cos(phi) + pi / horn_width
    kx_m = k * sin(theta) * cos(phi) - pi / horn_width

    # Calculate the arguments of the Fresnel integrals
    t1_p = sqrt(1.0 / (pi * k * hplane_effective_length)) * (-k * horn_width / 2.0 - kx_p * hplane_effective_length)
    t2_p = sqrt(1.0 / (pi * k * hplane_effective_length)) * ( k * horn_width / 2.0 - kx_p * hplane_effective_length)

    t1_m = sqrt(1.0 / (pi * k * hplane_effective_length)) * (-k * horn_width / 2.0 - kx_m * hplane_effective_length)
    t2_m = sqrt(1.0 / (pi * k * hplane_effective_length)) * ( k * horn_width / 2.0 - kx_m * hplane_effective_length)

    # Calculate the Fresnel integrals
    s1p, c1p = fresnel(t1_p)
    s2p, c2p = fresnel(t2_p)

    s1m, c1m = fresnel(t1_m)
    s2m, c2m = fresnel(t2_m)

    # Build the terms from the Fresnel integrals
    fresnel_term1 = (c2p - c1p) + 1j * (s1p - s2p)
    fresnel_term2 = (c2m - c1m) + 1j * (s1m - s2m)

    # Calculate the phase terms
    phase_term1 = exp(1j * kx_p ** 2 * hplane_effective_length / (2.0 * k))
    phase_term2 = exp(1j * kx_m ** 2 * hplane_effective_length / (2.0 * k))

    return 0.5 * sqrt(pi * hplane_effective_length / k) * (phase_term1 * fresnel_term1 + phase_term2 * fresnel_term2)


def I2(k, horn_height, eplane_effective_length, theta, phi):
    """
    Calculate the integral used for far field calculations.
    :param k: The wavenumber (rad/m).
    :param horn_height: The height of the horn (m).
    :param eplane_effective_length: The horn effective length in the E-plane (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :return: The integral used for far field calculations.
    """
    # Calculate the y-component of the wavenumber
    ky = k * sin(theta) * sin(phi)

    # Calculate the arguments for the Fresnel integrals
    t1 = sqrt(1.0 / (pi * k * eplane_effective_length)) * (-k * horn_height / 2.0 - ky * eplane_effective_length)
    t2 = sqrt(1.0 / (pi * k * eplane_effective_length)) * ( k * horn_height / 2.0 - ky * eplane_effective_length)

    # Calculate the Fresnel integrals
    s1, c1 = fresnel(t1)
    s2, c2 = fresnel(t2)

    return sqrt(pi * eplane_effective_length / k) * exp(1j * ky ** 2 * eplane_effective_length / (2.0 * k)) * \
           ((c2 - c1) + 1j * (s1 - s2))
