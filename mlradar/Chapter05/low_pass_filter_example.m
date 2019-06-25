%% Low pass filter example
% Created by: Lee A. Harrison
% On: 9/19/2018

clear, clc

% Set the parameters
filter_order = 4;
critical_frequency = 100;
maximum_ripple = 5.0;
minimum_attenuation = 40.0;

% Butterworth
[zb, pb, kb] = butter(filter_order, 2.0 * pi * critical_frequency, 's');
[bb, ab] = zp2tf(zb, pb, kb);
[hb, wb] = freqs(bb, ab, 4096);

% Chebyshev Type I 
[z1, p1, k1] = cheby1(filter_order, maximum_ripple, 2.0 * pi * critical_frequency, 's');
[b1, a1] = zp2tf(z1, p1, k1);
[h1, w1] = freqs(b1, a1, 4096);

% Chebyshev Type II
[z2, p2, k2] = cheby2(filter_order, minimum_attenuation, 2.0 * pi * critical_frequency, 's');
[b2, a2] = zp2tf(z2, p2, k2);
[h2, w2] = freqs(b2, a2, 4096);

% Elliptic filter
[ze, pe, ke] = ellip(filter_order, maximum_ripple, minimum_attenuation, 2.0 * pi * critical_frequency, 's');
[be, ae] = zp2tf(ze, pe, ke);
[he, we] = freqs(be, ae, 4096);

% Plot the results
plot(wb / (critical_frequency * pi), 20 * log10(abs(hb))); hold on
plot(w1 / (critical_frequency * pi), 20 * log10(abs(h1)));
plot(w2 / (critical_frequency * pi), 20 * log10(abs(h2)));
plot(we / (critical_frequency * pi), 20 * log10(abs(he)));
grid on;
xlabel('Frequency (Hz)')
ylabel('Attenuation (dB)')
legend('Butterworth','Chebyshev I','Chebyshev II','Elliptic')