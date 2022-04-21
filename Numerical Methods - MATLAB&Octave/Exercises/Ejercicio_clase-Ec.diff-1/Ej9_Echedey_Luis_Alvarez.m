% TEMA 5 - EJERCICIO 9
%{
*** ENUNCIADO ***
Sea el problema del valor inicial (PVI) { y' + 30y = 0, 0<=t<=1, y(0) = 1 }
cuya solución exacta es e^(-30t),
aproximar por el método de Euler de pasos 0.1, 0.05 y 0.01
y representar gráficamente junto con la solución exacta.
Comentar los resultados
%}

% Clear workspace and screen, set up format configuration
clear, clc;
format long g;

% Runtime config variables
%   Visualización de datos
nx_plots = 1;
ny_plots = 3;

% Función y dato inicial
f = @(t, y) - 30 .* y;
y0 = 1;

% Solución exacta
y_sol = @(t) exp(-30 .* t);

% Intervalo para aproximar
a = 0; b = 1;

% Tamaños de paso y pasos
h1 = 0.10; M1 = round( ( b - a ) / h1 )
h2 = 0.05; M2 = round( ( b - a ) / h2 )
h3 = 0.01; M3 = round( ( b - a ) / h3 )

% Cálculo de las soluciones por Euler
E1 = euler(f, a, b, y0, M1); disp(E1);
E2 = euler(f, a, b, y0, M2); disp(E2);
E3 = euler(f, a, b, y0, M3); disp(E3);

% Representación gráfica de las soluciones
% La exacta
t = a:0.01:b;
y = y_sol (t);

% Aproximaciones
subplot (nx_plots, ny_plots, 1);
plot(t, y, 'r', E1(:,2), E1(:,3), 'b--' , "LineWidth", 2 );

subplot (nx_plots, ny_plots, 2);
plot(t, y, 'r', E2(:,2), E2(:,3), 'g-.' , "LineWidth", 2 );

subplot (nx_plots, ny_plots, 3);
plot(t, y, 'r', E3(:,2), E3(:,3), 'k: ' , "LineWidth", 2 );
