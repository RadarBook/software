classdef linear_array
    % Linear array antenna
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    %
    % Copyright (C) 2019 Artech House (artech@artechhouse.com)
    % This file is part of Introduction to Radar Using Python and MATLAB
    % and can not be copied and/or distributed without the express permission of Artech House.
    
    properties
        % Properties for linear arrays
        number_of_elements = 10; % The number of elements in the array.
        scan_angle = 0.5 * pi; % The scan angle of the main lobe (rad).
        element_spacing = 0.5; % The spacing between each element (m).
        frequency = 300.0e6; % The operating frequency (Hz).
        theta = 0.25 * pi; % The angle at which to evalue the array factor (rad).
        window_type = 'Uniform'; % The weighting on the array elements.
        side_lobe_level = -20.0; % The side lobe level for Tschebyscheff array (dB).
    end
    
    methods
        % Methods for linear arrays
        function obj = linear_array(number_of_elements, scan_angle, element_spacing,...
                frequency, theta, window_type, side_lobe_level)
            % Class constructor
            if(nargin > 0)
                obj.theta = theta;
                obj.frequency = frequency;
                obj.number_of_elements = number_of_elements;
                obj.scan_angle = scan_angle;
                obj.element_spacing = element_spacing;
                obj.theta = theta;
                obj.window_type = window_type;
                obj.side_lobe_level = side_lobe_level;
            end
        end
        
        function af = array_factor(obj)
            % Calculate the array factor for a linear binomial excited array.
            % :param window_type: The string name of the window.
            % :param side_lobe_level: The sidelobe level for Tschebyscheff window (dB).
            % :param number_of_elements: The number of elements in the array.
            % :param scan_angle: The angle to which the main beam is scanned (rad).
            % :param element_spacing: The distance between elements.
            % :param frequency: The operating frequency (Hz).
            % :param theta: The angle at which to evaluate the array factor (rad).
            % :return: The array factor as a function of angle.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the phase
            psi = k * obj.element_spacing * (cos(obj.theta) - cos(obj.scan_angle));
            
            % Calculate the coefficients
            if strcmp(obj.window_type, 'Uniform')
                coefficients = ones(obj.number_of_elements, 1);
            elseif strcmp(obj.window_type, 'Binomial')
                clear coefficients
                for k = 1:obj.number_of_elements-1
                    coefficients(k+1) = nchoosek(obj.number_of_elements-1, k);
                end
                coefficients = coefficients';
            elseif strcmp(obj.window_type, 'Tschebyscheff')
                coefficients = tschebyscheff_coefficients(obj.number_of_elements, obj.side_lobe_level)';
            elseif strcmp(obj.window_type, 'Hanning')
                k = 0:obj.number_of_elements-1;
                coefficients = 0.5 - 0.5 * cos(2.0 * pi * k' / (obj.number_of_elements - 1));
            elseif strcmp(obj.window_type, 'Hamming')
                k = 0:obj.number_of_elements-1;
                coefficients = 0.54 - 0.46 * cos(2.0 * pi * k' / (obj.number_of_elements - 1));
            end
            
            % Calculate the offset for even/odd
            offset = floor(obj.number_of_elements / 2);
            
            % Odd case
            if mod(obj.number_of_elements,2) == 1
                coefficients = circshift(coefficients, offset + 1);
                coefficients(1) = 0.5 * coefficients(1);
                af = zeros(1, numel(obj.theta));
                for i = 1:offset + 1
                    af = af + coefficients(i) * cos((i-1) * psi);
                end
                af = af / max(max(abs(af)));
                % Even case
            else
                coefficients = circshift(coefficients, offset);
                af = zeros(1, numel(obj.theta));
                for i = 1:offset
                    af = af + coefficients(i) * cos((i - 0.5) * psi);
                end
                af = af / max(max(abs(af)));
            end
            
        end
        
        function af = array_factor_un(obj)
            % Calculate the array factor for a linear binomial excited array.
            % :param window_type: The string name of the window.
            % :param side_lobe_level: The sidelobe level for Tschebyscheff window (dB).
            % :param number_of_elements: The number of elements in the array.
            % :param scan_angle: The angle to which the main beam is scanned (rad).
            % :param element_spacing: The distance between elements.
            % :param frequency: The operating frequency (Hz).
            % :param theta: The angle at which to evaluate the array factor (rad).
            % :return: The array factor as a function of angle.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the phase
            psi = k * obj.element_spacing * (cos(obj.theta) - cos(obj.scan_angle));
            
            % Calculate the coefficients
            if strcmp(obj.window_type, 'Uniform')
                coefficients = ones(obj.number_of_elements, 1);
            elseif strcmp(obj.window_type, 'Binomial')
                clear coefficients
                for k = 0:obj.number_of_elements-1
                    coefficients(k+1) = nchoosek(obj.number_of_elements, k);
                end
                coefficients = coefficients';
            elseif strcmp(obj.window_type, 'Tschebyscheff')
                coefficients = tschebyscheff_coefficients(obj.number_of_elements, obj.side_lobe_level)';
            elseif strcmp(obj.window_type, 'Hanning')
                k = 0:obj.number_of_elements-1;
                coefficients = 0.5 - 0.5 * cos(2.0 * pi * k' / (obj.number_of_elements - 1));
            elseif strcmp(obj.window_type, 'Hamming')
                k = 0:obj.number_of_elements-1;
                coefficients = 0.54 - 0.46 * cos(2.0 * pi * k' / (obj.number_of_elements - 1));
            end
            
            % Calculate the offset for even/odd
            offset = floor(obj.number_of_elements / 2);
            
            % Odd case
            if mod(obj.number_of_elements,2) == 1
                coefficients = circshift(coefficients, offset + 1);
                coefficients(1) = 0.5 * coefficients(1);
                af = zeros(1, numel(obj.theta));
                for i = 1:offset + 1
                    af = af + coefficients(i) * cos((i-1) * psi);
                end
                % Even case
            else
                coefficients = circshift(coefficients, offset);
                af = zeros(1, numel(obj.theta));
                for i = 1:offset
                    af = af + coefficients(i) * cos((i - 0.5) * psi);
                end
            end
            
            
        end
    end
end
