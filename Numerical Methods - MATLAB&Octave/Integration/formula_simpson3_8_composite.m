% Autor: Echedey Luis Álvarez
% Fecha: 11/05/2021
% 
% Aplicación general de aproximación de integrales por la Fórmula de Simpson 3/8 Compuesta

function aprox = formula_simpson3_8_composite(h, y)
%{ 
Aproxima la integral de una función que pasa por (xi, yi)
Argumentos:
  y: array puntos x de los vectores
  h: distancia homogénea entre cada par de puntos
Salida:
  aprox: valor aproximado de la integral
%}
if ( mod(size( y ), 3) ~= 0)
  error("formula_simpson_composite 3/8: Number of nodes must be multiple of 3.");
end

aprox = 0;

end % De la función


######## Tests 
## Cabecera
% Tests para:  Fórmula de Simpson 3/8 Compuesta

best_simpson3_8 = 0;
if (~calculate_single_node_number)
  sols_simpson3_8 = NaN(nodes/3-1, 2);
end

% Cuerpo
% Simpson 3/8
printf("Simpson 3/8: start of calculations");
if (calculate_single_node_number)
  nodes_simpson3_8 = nodes - mod(nodes, 3);
  if (mod(nodes, 3) ~= 0)
    printf("Warning: not using a multiple-of-3 number of nodes, now using %G nodes to execute Simpson properly", nodes_simpson3_8 );
  end
  
  x = linspace(3, 7, nodes_simpson3_8);
  y = f(x);

  best_simpson3_8 = formula_simpson3_8_composite(x(2) - x(1), y);

else
  for i = 2:nodes/2
    
    x = linspace(3, 7, i*2);
    y = f(x);

    valor = formula_simpson3_8_composite(x(2) - x(1), y);
    
    sols_simpson3_8(i-1, :) = [i*2, valor];
    
    if (show_sols)
      printf(sols_simpson3_8);
    end

  end % !for
  best_simpson3_8 = sols_simpson3_8(end);
end % !if
printf("Simpson 3/8 with %G nodes: %G\n", nodes_simpson3_8, best_simpson3_8);
printf("Simpson 3/8: end of calculations");

% Fin
printf("Err(Simpson 3/8) = %G [%G nodes]\n", true_value - best_simpson3_8, nodes_simpson3_8);7
