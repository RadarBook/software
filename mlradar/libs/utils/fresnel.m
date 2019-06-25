function [C,S] = fresnel(x)
%% Fresnel sin and cos integrals
% :param x: The array of integral arguments.
% :return: The value of the sin and cos integrals.
%
% Created by: Lee A. Harrison
% On: 6/18/2018

% Keep the sign and evaluate for positive arguments
signy = sign(x);
x = abs(x);

% The coefficients
fn = [0.49999988085884732562 1.3511177791210715095 1.3175407836168659241 1.1861149300293854992 ...
    0.7709627298888346769 0.4173874338787963957 0.19044202705272903923 0.06655998896627697537 ...
    0.022789258616785717418 0.0040116689358507943804 0.0012192036851249883877];

fd = [1.0 2.7022305772400260215 4.2059268151438492767 4.5221882840107715516 ...
    3.7240352281630359588 2.4589286254678152943  1.3125491629443702962 0.5997685720120932908 ...
    0.20907680750378849485 0.07159621634657901433 0.012602969513793714191 0.0038302423512931250065];

gn = [0.50000014392706344801 0.032346434925349128728 0.17619325157863254363 0.038606273170706486252...
    0.023693692309257725361 0.007092018516845033662 0.0012492123212412087428 0.00044023040894778468486...
    -8.80266827476172521e-6 -1.4033554916580018648e-8 2.3509221782155474353e-10];

gd  = [1.0 2.0646987497019598937 2.9109311766948031235 2.6561936751333032911 2.0195563983177268073...
    1.1167891129189363902 0.57267874755973172715 0.19408481169593070798 0.07634808341431248904...
    0.011573247407207865977 0.0044099273693067311209 -0.00009070958410429993314];

% Get the size of the argument
[m, n] = size(x);

% Preallocate the arrays
C = zeros(m,n);
S = zeros(m,n);


% Loop over all the elements in the input argument
for im = 1:m
    
    for in = 1:n
        
        xi = x(im, in);
        
        if xi < 1.0 
            
            % cos series
            twofn = 0.0;  
            fact = 1.0;  
            denterm = 1.0; 
            numterm = 1.0; 
            ss = 1.0; 
            ratio = 10.0;
            t = -(0.5 * pi * xi * xi) ^ 2;
            
            while ratio > eps
                
                twofn = twofn + 2.0;
                fact = fact * twofn * (twofn - 1.0);
                denterm = denterm + 4.0;
                numterm = numterm * t;
                term = numterm / (fact * denterm);
                ss = ss + term;
                ratio = abs(term / ss);
                
            end
            
            C(im, in) =  xi * ss;
            
            % sin series
            twofn = 1.0;  
            fact = 1.0;  
            denterm = 3.0;  
            numterm = 1.0;  
            ss = 1.0/3.0;
            ratio = 10.0;
            
            while ratio > eps  
                
                twofn = twofn + 2.0;
                fact = fact * twofn * (twofn - 1.0);
                denterm = denterm + 4.0;
                numterm = numterm * t;
                term = numterm / (fact * denterm);
                ss = ss + term;
                ratio = abs(term / ss);
                
            end
            
            S(im, in) =  0.5 * pi * xi * xi * xi * ss;
            
        elseif xi < 6.0
            
            sumn =  0.0;
            sumd =  fd(12);
            
            for k=11:-1:1
                sumn = fn(k) + xi * sumn;
                sumd = fd(k) + xi * sumd;
            end
            
            f = sumn / sumd;
            
            sumn =  0.0;
            sumd =  gd(12);
            
            for k=11:-1:1
                sumn = gn(k) + xi * sumn;
                sumd = gd(k) + xi * sumd;
            end
            
            g = sumn / sumd;
            
            u = 0.5 * pi * xi * xi;
            
            su = sin(u);
            cu = cos(u);
            
            C(im, in) = 0.5 + f * su - g * cu;
            S(im, in) = 0.5 - f * cu - g * su;
           
        else
            
            numterm = -1.0;   	
            term = 1.0;  	
            ss = 1.0;  	
            oldterm = 1.0;
            ratio = 10.0; 	
            t = -(pi * xi * xi) ^ -2.0;
            
            while ratio > 0.1 * eps
                
                numterm = numterm + 4.0;
                term = term * numterm * (numterm - 2.0) * t;
                ss = ss + term;
                absterm = abs(term);
                ratio = abs(term / ss);
                
                if oldterm < absterm
                    ratio = 0.1 * eps;
                end
                
                oldterm = absterm;
                
            end
            
            f = ss / (pi * xi);

            numterm = -1.0;   
            term = 1.0; 	
            ss = 1.0; 	
            oldterm = 1.0;	
            ratio = 10.0;
            
            while ratio > 0.1 * eps
                
                numterm = numterm + 4.0;
                term = term * numterm * (numterm + 2.0) * t;
                ss = ss + term;
                absterm = abs(term);
                ratio = abs(term / ss);    
                
                if ( oldterm < absterm )                    
                    ratio = 0.1 * eps;
                end
                
                oldterm = absterm;
                
            end
            
            g = ss / ((pi * xi)^2 * xi);
            u = 0.5 * pi * xi * xi;
            
            su = sin(u);
            cu = cos(u);
            
            C(im, in) = 0.5 + f * su - g * cu;
            S(im, in) = 0.5 - f * cu - g * su;
            
        end
    end
end

% For negative input arguments
C = C .* signy;
S = S .* signy;