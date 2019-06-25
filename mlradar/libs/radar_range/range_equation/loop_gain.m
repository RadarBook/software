function lg = loop_gain(reference_range, reference_rcs, reference_snr)
%% Calculate the loop gain given the reference range information.
%     :param reference_range: Reference range for the radar (m).
%     :param reference_rcs: Reference radar cross section for the radar (m^2).
%     :param reference_snr: Reference signal to noise ratio for the radar.
%     :return: The loop gain for the radar.
%
%     Created by: Lee A. Harrison
%     On: 6/21/2018

% Calculate the loop gain
lg = reference_range .^ 4 * reference_snr ./ reference_rcs;