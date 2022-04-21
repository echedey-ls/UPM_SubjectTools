% Autor: Echedey Luis Álvarez
% Fecha: 11/05/2021
%
% Tests para: Fórmula del Trapecio Compuesta y Fórmula de Simpson Compuesta

% Clear workspace and screen, set up format configuration
clear, clc;
format long g;

% Runtime config variables
% What vars you use is up to you, but take into account the algorithm is made to fit a certain number of nodes.
% Number of intervals being used
subs_trapezium = 1e6;
subs_simpson = 8e2;
% Number of nodes being used
nodes_tr = subs_trapezium + 1;
nodes_sp = subs_simpson + 1;

calculate_single_node_number = true;
  % True: calculates just with the given number of nodes (recommended)
  % False: calculates for nodes = 2:[1 or 2]:nodes (not recommended, uses up too much memory)
show_sols = false;
  % Lets you display all calculated aproximations (not recommended, used for debugging)

% Función a integrar
f = @(x) 1 ./ (1 + x .^ 2);
% Extremos integración
a = 0; b = 4.06;
% Cuyo valor exacto es F = arctan(x), la evaluamos entre 3 y 7
true_value = atan(b) - atan(a);
% Por tanto los métodos deben converger a true_value = 0.1798534997924783

% Show config
fprintf("Calculating integral of:\n");
disp(f);
fprintf("Evaluated between %G and %G\n", a, b);

% Checks and user-proofing
if ( nodes_tr < 2 )
  error("Nodes must be greater or equal than 2 to apply Trapezium");
end
if ( nodes_sp < 3 )
  error("Nodes must be greater or equal than 3 to apply Simpson");
end

% Runtime variable alocation
best_trapezium = 0;
best_simpson = 0;

if (~calculate_single_node_number)
  sols_trapezium = NaN(nodes_tr-1, 2);
  sols_simpson = NaN(nodes_sp/2-1, 2);
end


% Trapezium
fprintf("\nTrapezium: start of calculations\n");
if (calculate_single_node_number)
  x = linspace(a, b, nodes_tr);
  y = f(x);

  best_trapezium = formula_trapezium_composite(x(2) - x(1), y);

else
  for i = 2:nodes_tr

    x = linspace(a, b, i);
    y = f(x);

    valor = formula_trapezium_composite(x(2) - x(1), y);

    sols_trapezium(i-1, :) = [i, valor];

    if (show_sols)
      fprintf(sols_trapezium);
    end

  end % !for
  best_trapezium = sols_trapezium(end);
end % !if
fprintf("Trapezium with %G nodes: %.10G\n", nodes_tr, best_trapezium);
fprintf("Trapezium: end of calculations\n");

% Simpson
fprintf("\nSimpson: start of calculations\n");

nodes_simpson = nodes_sp - mod(nodes_sp - 1, 2);
if (mod(nodes_sp - 1, 2) ~= 0)
  fprintf("Warning: not using a multiple-of-2 number of subintervals, now using %G nodes to execute Simpson properly\n", nodes_simpson );
end

if (calculate_single_node_number)

  x = linspace(a, b, nodes_simpson);
  y = f(x);

  best_simpson = formula_simpson_composite(x(2) - x(1), y);

else
  for i = 2:2:nodes_simpson

    x = linspace(a, b, i);
    y = f(x);

    valor = formula_simpson_composite(x(2) - x(1), y);

    sols_simpson(i/2, :) = [i, valor];

    if (show_sols)
      fprintf(sols_simpson);
    end

  end % !for
  best_simpson = sols_simpson(end);
end % !if
fprintf("Simpson with %G nodes: %.10G\n", nodes_simpson, best_simpson);
fprintf("Simpson: end of calculations\n");


% Show errors
fprintf("\nErrors:\n");
fprintf("Err(Trapezium) = %.10G [%G nodes]\n", true_value - best_trapezium, nodes_tr);
fprintf("Err(Simpson) = %.10G [%G nodes]\n", true_value - best_simpson, nodes_simpson);

% Errors:
% Err(Trapezium) = 3.648925873E-08 [1001 nodes]
% Err(Simpson) = 3.899103262E-13 [501 nodes]

% Errors:
% Err(Trapezium) = 6.550315845E-14 [1E+06 nodes]
% Err(Simpson) = 5.86197757E-14 [801 nodes]

% Simpson is the boss
