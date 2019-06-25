"""
Project: RadarBook
File: diffraction.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm
"""
from scipy import sqrt, radians, cos, arccos, pi, log10
from Libs.utils import lla_to_ecef


def attenuation(radar, target, frequency, relative_permittivity, conductivity):
    """
    Calculate the attenuation due to diffraction over a spherical Earth.
    :param radar: The radar LLA location (deg, deg, m).
    :param target: The target LLA location (deg, deg, m).
    :param frequency: The operating frequency (Hz).
    :param relative_permittivity: The relative permittivity.
    :param conductivity: The conductivity (S).
    :return: The attenuation due to diffraction over a spherical Earth (dB).
    """
    # Wavelength
    wavelength = 299792458 / frequency

    # Define h1 and h2 for nomenclature purposes
    h1 = radar['alt']
    h2 = target['alt']

    # Calculate the distance between the radar and the target
    rx, ry, rz = lla_to_ecef.convert(radians(radar['lat']), radians(radar['lon']), radar['alt'])
    tx, ty, tz = lla_to_ecef.convert(radians(target['lat']), radians(target['lon']), target['alt'])

    d = sqrt((rx - tx) ** 2 + (ry - ty) ** 2 + (rz - tz) ** 2)

    # Calculate the marginal line of sight distance
    effective_earth_radius = 6378137
    d_los = sqrt(2. * effective_earth_radius) * (sqrt(h1) + sqrt(h2))

    # Two cases for diffraction loss
    if d >= d_los:
        diffraction_loss = _loss(effective_earth_radius, relative_permittivity, wavelength, conductivity, d, h1, h2)
    else:
        # Calculate the clearance heights
        c = (h1 - h2) / (h1 + h2)

        m = d ** 2 / (4. * effective_earth_radius * (h1 + h2))

        b = 2. * sqrt((m + 1.) / (3. * m)) * cos(
            pi / 3. + 1. / 3. * arccos(3. * c / 2. * sqrt((3. * m) / (m + 1.) ** 3)))

        d1 = 0.5 * d * (1. + b)
        d2 = d - d1

        # Smallest clearance height
        hc = ((h1 - d1 ** 2 / (2. * effective_earth_radius)) * d2 + (
                h2 - d2 ** 2 / (2. * effective_earth_radius)) * d1) / d

        # Clearance required for zero diffraction
        h0 = 0.552 * sqrt((d1 * d2 * wavelength) / d)

        if hc > h0:
            diffraction_loss = 0.
        else:
            # Calculate the modified effective earth radius
            effective_earth_radius_modified = 0.5 * (d / (sqrt(h1) + sqrt(h2))) ** 2

            diffraction_loss = _loss(effective_earth_radius_modified, relative_permittivity, wavelength, conductivity,
                                     d, h1, h2)

    return diffraction_loss


def _loss(effective_earth_radius, relative_permittivity, wavelength, conductivity, d, h1, h2):
    """
    Calculate the loss for the cases where h0 >= the critical height.
    :param effective_earth_radius: The effective Earth radius (m).
    :param relative_permittivity: The relative permittivity.
    :param wavelength: The wavelength (m).
    :param conductivity: The conductivity (S).
    :param d: The distance between the radar and target (m).
    :param h1: The height of the radar (m).
    :param h2: The height of the target (m).
    :return: The result of the loss calculation for this specific case (dB).
    """
    # Calculate the surface admittance for both polarizations
    Yh = (2. * pi * effective_earth_radius / wavelength) ** (-1. / 3.) * \
         ((relative_permittivity - 1.) ** 2 + (60. * wavelength * conductivity) ** 2) ** (-0.25)

    Yv = Yh * sqrt(relative_permittivity ** 2 + (60. * wavelength * conductivity) ** 2)

    # Earth electrical factor (semi empirical)
    beta_h = (1. + 1.6 * Yh ** 2 + 0.67 * Yh ** 4) / (1. + 4.5 * Yh ** 2 + 1.53 * Yh ** 4)
    beta_v = (1. + 1.6 * Yv ** 2 + 0.67 * Yv ** 4) / (1. + 4.5 * Yv ** 2 + 1.53 * Yv ** 4)

    # Calculate the normalized distance and heights
    dn = beta_h * d * (pi / (wavelength * effective_earth_radius ** 2)) ** (1./3.)
    h1n = 2. * beta_h * h1 * (pi ** 2 / (wavelength ** 2 * effective_earth_radius)) ** (1. / 3.)
    h2n = 2. * beta_h * h2 * (pi ** 2 / (wavelength ** 2 * effective_earth_radius)) ** (1. / 3.)

    return _distance_gain(dn) + _height_gain(beta_h, h1n) + _height_gain(beta_h, h2n)


def _distance_gain(dn):
    """
    Calculate the distance gain term.
    :param dn: The normalized distance (m).
    :return: The distance gain (dB).
    """
    if dn >= 1.6:
        return 11. + 10. * log10(dn) - 17.6 * dn
    else:
        return -20.0 * log10(dn) - 5.6488 * dn ** 1.425


def _height_gain(beta, h):
    """
    Calculate the height gain term.
    :param beta: The height coefficient (1/m).
    :param h: The height (m).
    :return: The height gain (dB).
    """
    bh = beta * h
    if bh > 2.:
        return 17.6 * sqrt(bh - 1.1) - 5. * log10(bh - 1.1) - 8.
    else:
        return 20. * log10(bh + 0.1 * bh ** 3)
