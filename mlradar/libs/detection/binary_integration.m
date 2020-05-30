function [ pd_binary, pfa_binary ] = binary_integration( m, n, pd, pfa )
% Calculate the probability of detection for M of N integration.
% Calcualte the probability of false alarm for M of N integration.
%     :param m: The number of required detections.
%     :param n: The total number of measurements.
%     :param pd: The probability of detection for a single measurement.
%     :return: The probability of M on N detections.
%     :return: The probability false alarm for M on N detections.
%
%     Created by: Lee A. Harrison
%     On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

pd_binary = 0;
pfa_binary = 0;

for k = m:n
    pd_binary = pd_binary + nchoosek(n, k) * pd ^ k * (1.0 - pd) ^ (n - k);    
    pfa_binary = pfa_binary + nchoosek(n, k) * pfa ^ k * (1.0 - pfa) ^ (n - k);
end

end

