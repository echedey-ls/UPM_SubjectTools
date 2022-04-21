% Autor: Echedey Luis Álvarez
% Fecha: 11/05/2021
% 
% Aplicación general de aproximación de integrales por la Fórmula del Trapecio Compuesta

function aprox = formula_trapezium_composite(h, y)
%{ 
Aproxima la integral de una función que pasa por (xi, yi)
Argumentos:
  y: array puntos x de los vectores
  h: distancia homogénea entre cada par de puntos
Salida:
  aprox: valor aproximado de la integral
%}

aprox = h * ( (y(1) + y(end) ) / 2 + sum( y( 2:end-1 ) ) );

end % De la función
