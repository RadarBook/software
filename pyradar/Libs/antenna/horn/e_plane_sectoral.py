"""
Project: RadarBook
File: e_plane_sectoral.py
Created by: Lee A. Harrison
On: 7/6/2018
Created with: PyCharm
"""
from scipy import exp, sin, cos, sqrt, ones_like
from scipy.constants import c, epsilon_0, mu_0, pi
from scipy.special import fresnel


def aperture_fields(guide_width, horn_effective_length, frequency, x, y):
    """
    Calculate the electric and magnetic fields at the aperture of the horn.
    Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
    And that the horn length is large compared to the dimensions of the waveguide.
    :param x: The x coordinate to calculate the field in the aperture (m).
    :param y: The y coordinate to calculate the field in the aperture (m).
    :param guide_width: The width of the waveguide feed (m).
    :param horn_effective_length: The effective length of the horn (m).
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
    e_y = cos(pi * x / guide_width) * exp(-1j * k * y ** 2 / (2.0 * horn_effective_length))

    # Define the z-component of the electric field
    e_z = 0.0

    # Define the x-component of the magnetic field
    h_x = -cos(pi * x / guide_width) / eta * exp(-1j * k * y ** 2 / (2.0 * horn_effective_length))

    # Define the y-component of the magnetic field
    h_y = 0.0

    # Define the z-component of the magnetic field
    h_z = 1j * pi / (k * guide_width * eta) * sin(pi * x / guide_width) * \
          exp(-1j * k * y ** 2 / (2.0 * horn_effective_length))

    # Return all six components of the aperture field
    return e_x, e_y, e_z, h_x, h_y, h_z


def far_fields(guide_width, horn_height, horn_effective_length, frequency, r, theta, phi):
    """
    Calculate the electric and magnetic fields in the far field of the horn.
    :param r: The distance to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param guide_width: The width of the waveguide feed (m).
    :param horn_height: The height of the horn (m).
    :param horn_effective_length: The effective length of the horn (m).
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
    e_theta = I(k, r, theta, phi, horn_effective_length, horn_height, guide_width) * sin(phi) * (1.0 + cos(theta))

    # Define the phi-component of the electric field
    e_phi = I(k, r, theta, phi, horn_effective_length, horn_height, guide_width) * cos(phi) * (1.0 + cos(theta))

    # Define the radial-component of the magnetic field
    h_r = 0.0

    # Define the theta-component of the magnetic field
    h_theta = I(k, r, theta, phi, horn_effective_length, horn_height, guide_width) * \
              -cos(phi) / eta * (1.0 + cos(theta))

    # Define the phi-component of the magnetic field
    h_phi = I(k, r, theta, phi, horn_effective_length, horn_height, guide_width) * \
            sin(phi) / eta * (1.0 + cos(theta))

    # Return all six components of the far field
    return e_r, e_theta, e_phi, h_r, h_theta, h_phi


def directivity(guide_width, horn_height, horn_effective_length, frequency):
    """
    Calculate the directivity for the E-plane sectoral horn.
    :param guide_width: The width of the waveguide feed (m).
    :param horn_height: The height of the horn (m).
    :param horn_effective_length: The effective length of the horn (m).
    :param frequency: The operating frequency (Hz).
    :return: The directivity of the E-plane sectoral horn.
    """
    # Calculate the wavelength
    wavelength = c / frequency

    # Get the Fresnel integrals
    C, S = fresnel(horn_height / sqrt(2.0 * horn_effective_length * wavelength))

    return 64.0 * guide_width * horn_effective_length / (pi * wavelength * horn_height) * (C ** 2 + S ** 2)


def power_radiated(guide_width, horn_height):
    """
    Calculate the normalized power radiated by the E-plane sectoral horn.
    :param guide_width: The width of the waveguide feed (m).
    :param horn_height: The height of the horn (m).
    :return: The power radiated by the E-plane sectoral horn (normalized by |E0|^2) (W).
    """
    return horn_height * guide_width / (4.0 * sqrt(mu_0 / epsilon_0))


def I(k, r, theta, phi, horn_effective_length, horn_height, guide_width):
    """
    Calculate the integral used in the far field calculations.
    :param k: The wavenumber (rad/m).
    :param r: The distance to the field point (m).
    :param theta: The theta angle to the field point (rad).
    :param phi: The phi angle to the field point (rad).
    :param horn_effective_length: The horn effective length (m).
    :param horn_height: The horn height (m).
    :param guide_width: The width of the waveguide feed (m).
    :return: The result of the integral for far field calculations.
    """
    # Calculate the x and y components of the wavenumber
    kx = k * sin(theta) * cos(phi)
    ky = k * sin(theta) * sin(phi)

    # Two separate terms for the Fresnel integrals
    t1 = sqrt(1.0 / (pi * k * horn_effective_length)) * (-k * horn_height * 0.5 - ky * horn_effective_length)
    t2 = sqrt(1.0 / (pi * k * horn_effective_length)) * ( k * horn_height * 0.5 - ky * horn_effective_length)

    # Get the Fresnel sin and cos integrals
    s1, c1 = fresnel(t1)
    s2, c2 = fresnel(t2)

    index = (kx * guide_width != pi) & (kx * guide_width != -pi)
    term2 = -ones_like(kx) / pi
    term2[index] = cos(kx[index] * guide_width * 0.5) / ((kx[index] * guide_width * 0.5) ** 2 - (pi * 0.5) ** 2)

    return exp(1j * ky ** 2 * horn_effective_length / (2.0 * k)) * -1j * guide_width * \
           sqrt(pi * k * horn_effective_length) / (8.0 * r) * exp(-1j * k * r) * term2 * ((c2 - c1) - 1j * (s2 - s1))
