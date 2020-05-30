function [An, Bn] = sphere_coefficients(frequency, epsilon, mu, radius, number_of_modes, pec)
%% Calculate the scattering coefficients for a stratified sphere.
%     :param frequency: The frequency of the incident wave (Hz).
%     :param epsilon: The relative permittivity of the layers.
%     :param mu: The relative permeability of the layers.
%     :param radius: The radius of each layer.
%     :param number_of_modes: The number of modes to calculate.
%     :param pec: True for PEC core.
%     :return: The scattering coefficients for a stratified sphere.

%     Created by: Lee A. Harrison
%     On: 1/18/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Speed of light
c = 299792458;

% Wavenumber
k = 2.0 * pi * frequency / c;

% Free space impedance
mu_0 = 4 * pi * 1e-7;
epsilon_0 = 8.854187817620389e-12;
eta_0 = sqrt(mu_0 / epsilon_0);

% Interfaces
number_of_interfaces = numel(mu);

An = zeros(1, number_of_modes);
Bn = zeros(1, number_of_modes);

z = zeros(number_of_interfaces, number_of_modes);
y = zeros(number_of_interfaces, number_of_modes);

% Loop over the interfaces
for i_layer = number_of_interfaces - 2: -1: 0
    eta_i = sqrt(mu(i_layer + 2) / epsilon(i_layer + 2)) * eta_0;
    m = sqrt(mu(i_layer + 2) * epsilon(i_layer + 2));
    
    if i_layer == number_of_interfaces - 2
        
        if ~pec
            za = k * m * radius(i_layer + 1);
            for n = 1:number_of_modes
                p(n) = spherical_j(n, za, false) / spherical_j(n, za, true);
            end
            
            z(i_layer + 1, :) = p * eta_i;
            y(i_layer + 1, :) = p / eta_i;
        end
        
    else
        z1 = m * k * radius(i_layer + 1);
        z2 = m * k * radius(i_layer + 2);
        
        for n = 1:number_of_modes
            j1 = spherical_j(n, z1, false);
            j2 = spherical_j(n, z2, false);
            
            j1p = spherical_j(n, z1, true);
            j2p = spherical_j(n, z2, true);
            
            h1 = spherical_h(n, 2, z1, false);
            h2 = spherical_h(n, 2, z2, false);
            
            h1p = spherical_h(n, 2, z1, true);
            h2p = spherical_h(n, 2, z2, true);
            
            u = (j2p * h1p) / (j1p * h2p);
            
            v = (j2 * h1) / (j1 * h2);
            
            p1 = j1 / j1p;
            
            p2 = j2 / j2p;
            
            q2 = h2 / h2p;
            
            if (i_layer == number_of_interfaces - 3) && pec
                z(i_layer + 1, n) = (eta_i .* p1 .* (1.0 - v)) ./ (1.0 - u .* p2 ./ q2);
                y(i_layer + 1, n) = (p1 ./ eta_i) .* (1.0 - v .* q2 / p2) ./ (1.0 - u);
                
            else
                t1 = 1.0 - z(i_layer + 2, n) ./ (eta_i .* q2);
                t2 = 1.0 - z(i_layer + 2, n) ./ (eta_i .* p2);
                z(i_layer + 1, n) = eta_i .* p1 * (1.0 - v .* t2 ./ t1);
                
                t1 = 1.0 - eta_i .* q2 ./ z(i_layer + 2, n);
                t2 = 1.0 - eta_i .* p2 ./ z(i_layer + 2, n);
                z(i_layer + 1, n) = z(i_layer + 1, n) ./ (1.0 - u .* t2 ./ t1);
                
                t1 = 1.0 - eta_i .* y(i_layer + 2, n) ./ q2;
                t2 = 1.0 - eta_i .* y(i_layer + 2, n) ./ p2;
                y(i_layer + 1, n) = (p1 ./ eta_i) .* (1.0 - v .* t2 ./ t1);
                
                t1 = 1.0 - q2 ./ (eta_i .* y(i_layer + 2, n));
                t2 = 1.0 - p2 ./ (eta_i .* y(i_layer + 2, n));
                y(i_layer + 1, n) = y(i_layer + 1, n) ./ (1.0 - u .* t2 ./ t1);
            end
        end
    end
end

Zn = 1j * z(1, :) / eta_0;
Yn = 1j * y(1, :) * eta_0;

z = k * radius(1);

for n = 1:number_of_modes
    jn = spherical_j(n, z, false);
    jp = spherical_j(n, z, true);
    
    hn = spherical_h(n, 2, z, false);
    hp = spherical_h(n, 2, z, true);
    
    An(n) = -(1j ^ n) * (2.0 * n + 1.0) / (n * (n + 1.0)) * (jn + 1j * Zn(n) * jp) / (hn + 1j * Zn(n) * hp);
    
    Bn(n) = 1j ^ (n + 1) * (2.0 * n + 1.0) / (n * (n + 1.0)) * (jn + 1j * Yn(n) * jp) / (hn + 1j * Yn(n) * hp);
end
end


function x = spherical_j(mode, z, derivative)
%% Calculate the spherical Bessel function or derivatives.
%     :param mode: The mode.
%     :param z: The argument.
%     :param derivative: True for derivatives.
%     :return: The spherical Bessel function or derivatives.

s = sqrt(0.5 * pi / z);

if derivative
    x = (z * besselj(mode - 0.5, z) * s - mode * besselj(mode + 0.5, z) * s);
else
    x = z *  besselj(mode + 0.5, z) * s;
end
end


function x = spherical_h(mode, kind, z, derivative)
%% Calculate the spherical Hankel function or derivatives.
%     :param mode: The mode.
%     :param kind: First or second kind.
%     :param z: The argument.
%     :param derivative: True for derivatives.
%     :return: The spherical Hankel function or derivative.

s = sqrt(0.5 * pi / z);

if derivative
    x = (z * besselh(mode - 0.5, kind, z) * s - mode .*  besselh(mode + 0.5, kind, z) * s);
else
    x = z *  besselh(mode + 0.5, kind, z) * s;
end
end
