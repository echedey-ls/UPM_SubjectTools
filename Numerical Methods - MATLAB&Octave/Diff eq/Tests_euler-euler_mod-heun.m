% TESTS FOR FUNCTIONS:
%   euler.m
%   euler_mod.m

% USING: TEMA 5 - EJERCICIO 9
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
h10 = 0.01; M10 = round( ( b - a ) / h10 )
h20 = 0.01; M20 = round( ( b - a ) / h20 )
h30 = 0.01; M30 = round( ( b - a ) / h30 )

% Cálculo de las soluciones por Euler
E10 = euler(f, a, b, y0, M10); disp(E10);
E20 = euler_mod(f, a, b, y0, M20); disp(E20);
E30 = heun(f, a, b, y0, M30); disp(E30);

% Representación gráfica de las soluciones
% La exacta
t = a:0.01:b;
y = y_sol (t);

% Aproximaciones
subplot (nx_plots, ny_plots, 1);
plot(t, y, 'r', E10(:,2), E10(:,3), 'b- ' , "LineWidth", 2 );
title("Metodo de Euler");
grid on;

subplot (nx_plots, ny_plots, 2);
plot(t, y, 'r', E20(:,2), E20(:,3), 'b- ' , "LineWidth", 2 );
title("Metodo de Euler modificado");
grid on;

subplot (nx_plots, ny_plots, 3);
plot(t, y, 'r', E30(:,2), E30(:,3), 'b- ' , "LineWidth", 2 );
title("Metodo de Heun");
grid on;
