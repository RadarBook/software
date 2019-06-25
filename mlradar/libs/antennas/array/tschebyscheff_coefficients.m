function a = tschebyscheff_coefficients(N, sll)
%% Calculate the tschebyscheff coefficients
%     :param N: number of points in the window.
%     :param sll: the desired sidelobe level (dB).
%     :return: The Hamming window coefficients.
%
%     Created by: Lee A. Harrison
%     On: 4/26/2019

z0 = cosh( 1/(N-1) * acosh(10^(sll/20)) );

if mod(N,2) == 0
   
   M = N/2;
   
   for n = 1:M
      a(n) = 0;
      for q = n:M
         a(n) = a(n) + (-1)^(M-q) * z0^(2*q-1) * ( factorial(q+M-2) * (2*M - 1) )...
            / ( factorial(q-n)*factorial(q+n-1)*factorial(M-q) );
      end
   end
   
else
   
   M = (N-1)/2;
   
   for n = 1:M+1
      a(n) = 0;
      if n == 1
         epsn = 2;
      else
         epsn = 1;
      end
      
      for q = n:M+1
         a(n) = a(n) + (-1)^(M-q+1) * z0^(2*(q-1)) * ( factorial(q+M-2) * (2*M) )...
            / ( epsn*factorial(q-n)*factorial(q+n-2)*factorial(M-q+1) );
      end
   end   
end
