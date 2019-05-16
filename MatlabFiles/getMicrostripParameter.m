function [Z_0,epsilon_e] = getMicrostripParameter(epsilon_r,w,h)
%Author- Dr. Michael Steer

% mstrip_single
%
% Calculate the parameters of a microstrip line 
%
% Uses the analysis of Hammerstad and Jensen in Section 4.10.2 of Steer,
% Microwave and RF Design
%
% INPUT:
%       espilon_r relative permittivity of substaret
%       u = width-to-height ratio.   u = w/h
%                              w = width of line(s)
%                              h = height of substrate
% OUTPUT:
%      Z_0 characteristic impedance of a single line
%      espilon_e effective relative permittivity of a single line
% Set microstrip parameters
    u = w/h;
    a = 1+log((u^4 + (u/52)^2)/(u^4+0.432))/49+log(1+(u/18.1)^3)/18.7;
    b = 0.564*((epsilon_r-0.9)/(epsilon_r+3))^0.053;
% Calculate effective permittivity
    epsilon_e = (epsilon_r+1)/2 + ((epsilon_r-1).*(1+10./u).^(-(a*b)))/2;
    F_1 = 6+(2*pi-6)*exp(-(30.999./u).^0.7528);
% Calculate free-space characteristic impedance of microstrip
    Z_01 = 60*log(F_1./u+sqrt(1+(2./u).^2));
% Calculate microstrip characteristic impedance
    Z_0 = Z_01./sqrt(epsilon_e);
end

