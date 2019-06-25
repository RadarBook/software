"""
Project: RadarBook
File: atmosphere.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm
"""
from scipy import sqrt, exp, empty, empty_like, sum
from pathlib import Path


def attenuation(frequency, temperature, dry_air_pressure, water_vapor_density):
    """
    Calculate the attenuation due to the atmosphere.
    :param frequency: The frequency of operation (Hz).
    :param temperature: The atmospheric temperature (K).
    :param dry_air_pressure: The dry air pressure (hPa).
    :param water_vapor_density: The water vapor density (g/m^3).
    :return: The specific attenuation (dB/km).
    """
    # Set up the O2 and H2O coefficient arrays
    fo = empty(44)
    a1 = empty(44)
    a2 = empty(44)
    a3 = empty(44)
    a4 = empty(44)
    a5 = empty(44)
    a6 = empty(44)

    fw = empty(35)
    b1 = empty(35)
    b2 = empty(35)
    b3 = empty(35)
    b4 = empty(35)
    b5 = empty(35)
    b6 = empty(35)

    # Read in the spectral data for oxygen
    base_path = Path(__file__).parent
    i = 0
    with open((base_path / "oxygen_spectral_attenuation.txt"), "r") as f:
        data = f.readlines()
        for line in data:
            fo[i], a1[i], a2[i], a3[i], a4[i], a5[i], a6[i] = [float(x) for x in line.split()]
            i += 1

    # Read in the spectral data for water
    i = 0
    with open((base_path / "water_vapor_spectral_attenuation.txt"), "r") as f:
        data = f.readlines()
        for line in data:
            fw[i], b1[i], b2[i], b3[i], b4[i], b5[i], b6[i] = [float(x) for x in line.split()]
            i += 1

    # Find the percent temperature
    theta = 300 / temperature

    # Calculate the water vapor partial pressure
    water_vapor_pressure = water_vapor_density * temperature / 216.7

    # Total barometric pressure = dry air pressure + water vapor partial pressure
    S_o = a1 * 1e-7 * dry_air_pressure * theta**3 * exp(a2 * (1. - theta))
    S_w = b1 * 0.1 * water_vapor_pressure * theta**3.5 * exp(b2 * (1. - theta))

    # Calculate the line widths
    delta_F_o = a3 * 1e-4 * (dry_air_pressure * theta**(0.8 - a4) + 1.1 * water_vapor_pressure * theta)
    delta_F_o = sqrt(delta_F_o**2 + 2.25e-6)

    delta_F_w = b3 * 1e-4 * (dry_air_pressure * theta**b4 + b5 * water_vapor_pressure * theta**b6)
    delta_F_w = 0.535 * delta_F_w + sqrt(0.217*delta_F_w**2 + (2.1316e-12 * fw**2) / theta)

    del_o = (a5 + a6*theta) * 1e-4 * (water_vapor_pressure + dry_air_pressure) * theta**0.8

    N_water_vapor = empty_like(frequency)
    N_oxygen = empty_like(frequency)

    # Loop over all the frequencies and calculate the O2 and H2O terms
    i = 0
    for f in frequency:
        term1_o = (delta_F_o - del_o * (fo - f)) / ((fo - f)**2 + delta_F_o**2)
        term2_o = (delta_F_o - del_o * (fo + f)) / ((fo + f)**2 + delta_F_o**2)
        # F_o = f / fo * (term1_o + term2_o)

        N_oxygen[i] = sum(S_o * f / fo * (term1_o + term2_o))

        term1_w = delta_F_w / ((fw - f) ** 2 + delta_F_w ** 2)
        term2_w = delta_F_w / ((fw + f) ** 2 + delta_F_w ** 2)
        # F_w = f / fw * (term1_w + term2_w)

        N_water_vapor[i] = sum(S_w * f / fw * (term1_w + term2_w))

        i += 1

    # Pressure induced nitrogen attenuation
    d = 5.6e-4 * (dry_air_pressure + water_vapor_pressure) * theta**0.8

    N_d = frequency * dry_air_pressure * theta**2 * (6.14e-5 / (d * (1. + (frequency/d)**2)) + 1.4e-12 *
                                                     dry_air_pressure * theta**1.5 / (1. + 1.9e-5 * frequency**1.5))

    return 0.1820 * frequency * (N_oxygen + N_d + N_water_vapor)
