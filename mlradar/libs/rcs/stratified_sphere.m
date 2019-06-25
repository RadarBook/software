function [ rcs_th, rcs_ph ] = stratified_sphere(frequency, theta, phi, An, Bn)
%% Calculate the radar cross section for a stratified sphere.
%     :param frequency: The frequency of the incident wave (Hz).
%     :param theta: The observation angle theta (rad).
%     :param phi: The observation angle phi (rad).
%     :param An: Scattering coefficient.
%     :param Bn:Scattering coefficient.
%     :return: The radar cross section for a stratified sphere.

%     Created by: Lee A. Harrison
%     On: 1/18/2019

% Speed of light
c = 299792458;

% Wavelength
wavelength = c / frequency;

% Wavenumber
k = 2.0 * pi / wavelength;

st = abs(sin(theta));
ct = cos(theta);

% Associated Legendre Polynomial
p_lm = zeros(numel(An) + 1, 1);
p_lm(1) = -st;
p_lm(2) = -3.0 * st * ct;

s1 = 0;
s2 = 0;

p = p_lm(1);

for i_mode = 1:numel(An)
    % Derivative of associated Legendre Polynomial
    if abs(ct) < 0.999999999
        if i_mode == 1
            dp = ct * p_lm(1) / sqrt(1.0 - ct ^ 2);
        else
            dp = (i_mode * ct * p_lm(i_mode) - (i_mode + 1.0) * p_lm(i_mode - 1)) / sqrt(1.0 - ct ^ 2);
        end
    end
    
    if st > 1.0e-9
        t1 = An(i_mode) * p / st;
        t2 = Bn(i_mode) * p / st;
    end
    
    if ct > 0.999999999
        val = 1j ^ (i_mode - 1) * (i_mode * (i_mode + 1.0) / 2.0) * (An(i_mode) - 1j * Bn(i_mode));
        s1 = s1 + val;
        s2 = s2 + val;
    elseif ct < -0.999999999
        val = (-1j) ^ (i_mode - 1) * (i_mode * (i_mode + 1.0) / 2.0) * (An(i_mode) + 1j * Bn(i_mode));
        s1 = s1 + val;
        s2 = s2 - val;
    else
        s1 = s1 + 1j ^ (i_mode + 1) * (t1 - 1j * Bn(i_mode) * dp);
        s2 = s2 + 1j ^ (i_mode + 1) * (An(i_mode) * dp - 1j * t2);
    end
    
    % Recurrence relationship for nex Associated Legendre Polynomial
    if i_mode > 1
        p_lm(i_mode + 1) = (2.0 * i_mode + 1.0) * ct * p_lm(i_mode) / i_mode - (i_mode + 1.0) * p_lm(i_mode - 1) / i_mode;
    end
    
    p = p_lm(i_mode + 1);
    
    rcs_th = s1 * cos(phi) * sqrt(4.0 * pi) / k;
    rcs_ph = -s2 * sin(phi) * sqrt(4.0 * pi) / k;
end
end