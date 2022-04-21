% El único propósito de este programa es comprobar que las funciones
% funcionan, valga la redundancia.
% El documento y el nombre de las variables son self-explanatory

clear, clc
format long

f = @(x) x.^4 - 3*x - 5; % Esto me lo saco de la manga
df = @(x) 4*x.^3 - 3; % Y esto es la manga diferenciada

pto0 = 1; % Con el Geogebra se grafica f(x) y tomo un valor cualquiera
pto1 = 1.1; % Para el met. de la secante
err_rel = 0.001; % Porque es un buen número

[NR_p, NR_deltaRel] = metodo_newton_raphson(f, df, pto0, 20, err_rel);

[SEC_p, SEC_deltaRel] = metodo_secante(f, pto0, pto1, 20, err_rel);

% Debe converger a 1.795176530
disp("Por el método de Newton-Raphson");
porNewtonRaphson = table(NR_p, NR_deltaRel)
disp("Por el método de la secante");
porSecante = table(SEC_p, SEC_deltaRel)

% Solo quiero decir que esto es maravilloso
