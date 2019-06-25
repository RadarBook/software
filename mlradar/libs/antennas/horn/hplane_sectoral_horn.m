classdef hplane_sectoral_horn
    % H-plane sectoral horn
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    
    properties
        % Properties associated with the H-plane sectoral horn
        horn_width = 1.0; % The width of the horn (m).
        guide_height = 0.1; % The height of the waveguide feed (m).
        horn_effective_length = 1.0; % The effective length of the horn (m).
        frequency = 300.0e6; % The operating freqeuncy (Hz).
        x = 0.0; % The x coordinate to calculate the field in the aperture (m).
        y = 0.0; % The y coordinate to calculate the field in the aperture (m).
        r = 1.0e6; % The range to the field point (m).
        theta = 0.5 * pi; % The theta angle to the field point (rad).
        phi = 0.5 * pi; % The phi angle to the field point (rad).
    end
    
    methods
        % Methods associated with the H-plane sectoral horn
        function obj = hplane_sectoral_horn(horn_width, guide_height, horn_effective_length, frequency, ...
                x, y, r, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.frequency = frequency;
                obj.horn_width = horn_width;
                obj.guide_height = guide_height;
                obj.horn_effective_length = horn_effective_length;
                obj.x = x;
                obj.y = y;
                obj.r = r;
                obj.theta = theta;
                obj.phi = phi;
            end
        end
        
        function [e_x, e_y, e_z, h_x, h_y, h_z] = aperture_fields(obj)
            % Calculate the electric field at the aperture of the horn.
            % Assuming that the fields of the feeding waveguide are those of the dominant TE10 mode.
            % And that the horn length is large compared to the dimensions of the waveguide.
            % :param x: The x coordinate to calculate the field in the aperture (m).
            % :param y: The y coordinate to calculate the field in the aperture (m).
            % :param horn_width: The width of the horn (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The electric and magnetic fields in the aperture (V/m), (A/m).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the x-component of the electric field
            e_x = 0.0;
            
            % Define the y-component of the electric field
            e_y = cos(pi * obj.x / obj.horn_width) .* exp(-1j * k * 0.5 * (obj.x .^ 2 / obj.horn_effective_length));
            
            % Define the z-component of the electric field
            e_z = 0.0;
            
            % Define the x-component of the magnetic field
            h_x = -cos(pi * obj.x / obj.horn_width) / eta .* exp(-1j * k * 0.5 * (obj.x .^ 2 / obj.horn_effective_length));
            
            % Define the y-component of the magnetic field
            h_y = 0.0;
            
            % Define the z-component of the magnetic field
            h_z = 0.0;
            
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_fields(obj)
            % Calculate the electric and magnetic fields in the far field of the horn.
            % :param r: The distance to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param guide_height: The height of the waveguide feed (m).
            % :param horn_width: The width of the horn (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The electric and magnetic fields radiated by the horn (V/m), (A/m).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Define the radial-component of the electric field
            e_r = 0.0;
            
            % Define the theta-component of the electric field
            e_theta = sin(obj.phi) .* (1.0 + cos(obj.theta)) .* sinc(k * obj.guide_height * 0.5 * sin(obj.theta) .* sin(obj.phi)) .* I(obj);
            
            % Define the phi-component of the electric field
            e_phi = cos(obj.phi) .* (1.0 + cos(obj.theta)) .* sinc(k * obj.guide_height * 0.5 * sin(obj.theta) .* sin(obj.phi)) .* I(obj);
            
            % Define the radial-component of the magnetic field
            h_r = 0.0;
            
            % Define the theta-component of the magnetic field
            h_theta = -cos(obj.phi) / eta .* (1.0 + cos(obj.theta)) .* sinc(k * obj.guide_height * 0.5 * sin(obj.theta) .* sin(obj.phi)) .* I(obj);
            
            % Define the phi-component of the magnetic field
            h_phi = sin(obj.phi) / eta .* (1.0 + cos(obj.theta)) .* sinc(k * obj.guide_height * 0.5 * sin(obj.theta) .* sin(obj.phi)) .* I(obj);
            
        end
        
        
        function d = directivity(obj)
            % Calculate the directivity for the H-plane horn.
            % :param guide_height: The height of the waveguide feed (m).
            % :param horn_width: The width of the horn (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The directivity for the H-plane horn.
            
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the arguments for the Fresnel integrals
            u = 1.0 / sqrt(2.0) * (sqrt(wavelength * obj.horn_effective_length) / obj.horn_width ...
                + obj.horn_width / sqrt(wavelength + obj.horn_effective_length));
            
            v = 1.0 / sqrt(2.0) * (sqrt(wavelength * obj.horn_effective_length) / obj.horn_width...
                - obj.horn_width / sqrt(wavelength + obj.horn_effective_length));
            
            % Calculate the Fresnel integrals
            [Cu, Su] = fresnel(u);
            [Cv, Sv] = fresnel(v);
            
            d = 4.0 * pi * obj.guide_height * obj.horn_effective_length / (obj.horn_width * wavelength) * ((Cu - Cv) ^ 2 + (Su - Sv) ^ 2);
        end
        
        
        function prad = power_radiated(obj)
            % Calculate the normalized power radiated by the H-plane horn.
            % :param guide_height: The height of the waveguide feed (m).
            % :param horn_width: The width of the horn (m).
            % :return: The power radiated by the H-plane horn (normalized by |E0|^2) (W).
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Calculate the power radiated
            prad = obj.horn_width * obj.guide_height / (4.0 * eta);
        end
        
        
        function a = I(obj)
            % Calculate the integral used in the far field calculation.
            % :param k: The wavenumber (rad/m).
            % :param r: The distance to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param horn_width: The width of the horn (m).
            % :param guide_height: The height of the waveguide feed (m).
            % :param horn_effective_length: The effective length of the horn (m).
            % :return: The integral used in far field calculations.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the wavenumber prime and double prime terms
            kx_p = k * sin(obj.theta) .* cos(obj.phi) + pi / obj.horn_width;
            kx_m = k * sin(obj.theta) .* cos(obj.phi) - pi / obj.horn_width;
            
            % Phase terms for prime and double prime terms
            f1 = kx_p .* kx_p .* obj.horn_effective_length / (2.0 * k);
            f2 = kx_m .* kx_m .* obj.horn_effective_length / (2.0 * k);
            
            % Arguments of the Fresnel integrals for prime and double prime terms
            t1_p = sqrt(1.0 / (pi * k * obj.horn_effective_length)) * (-k * obj.horn_width * 0.5 - kx_p * obj.horn_effective_length);
            t2_p = sqrt(1.0 / (pi * k * obj.horn_effective_length)) * ( k * obj.horn_width * 0.5 - kx_p * obj.horn_effective_length);
            
            t1_m = sqrt(1.0 / (pi * k * obj.horn_effective_length)) * (-k * obj.horn_width * 0.5 - kx_m * obj.horn_effective_length);
            t2_m = sqrt(1.0 / (pi * k * obj.horn_effective_length)) * ( k * obj.horn_width * 0.5 - kx_m * obj.horn_effective_length);
            
            % Calculate the Fresnel sin and cos integrals
            [c1p, s1p] = fresnel(t1_p);
            [c2p, s2p] = fresnel(t2_p);

            [c1m, s1m] = fresnel(t1_m);
            [c2m, s2m] = fresnel(t2_m);            
            
            a = 1j * obj.guide_height * sqrt(k * obj.horn_effective_length / pi) / (8.0 * obj.r) .* exp(-1j * k * obj.r) .* ...
                (((c2p - c1p) - 1j * (s2p - s1p)) .* exp(1j * f1) + ((c2m - c1m) - 1j .* (s2m - s1m)) .* exp(1j * f2));
            
            
        end
        
    end
    
end

