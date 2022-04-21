% Autor: Echedey Luis Álvarez
% Fecha: 11/05/2021
% 
% Aplicación general de aproximación de integrales por la Fórmula de Simpson Compuesta

function aprox = formula_simpson_composite(h, y)
%{ 
Aproxima la integral de una función que pasa por (xi, yi)
Argumentos:
  y: array puntos x de los vectores
  h: distancia homogénea entre cada par de puntos
Salida:
  aprox: valor aproximado de la integral
%}
if ( mod(size( y ), 2) == 0)
  error("formula_simpson_composite: Number of nodes must be odd (to match an even number of subintervals).");
end

aprox = ( h / 3 ) * ( y(1) + y(end) + 4 * sum( y( 2:2:end-1 ) ) + 2 * sum( ( y(3:2:end-2 ) ) ) );

end % De la función
