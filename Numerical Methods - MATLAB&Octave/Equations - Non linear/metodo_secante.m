% Autor: Echedey Luis Álvarez
% Fecha: 07/03/2021
% 
% Aplicación general del método de la secante. Es una copia barata del de Newton-Raphson, pero con un par de cambios.


function [p, err_rel] = metodo_secante(f, p0, p1, max_iter, deltaRel)
% ------Aproxima la raíz de una función por el método de Newton-Raphson--------
% Argumentos:
%   f: función a calcular raíz
%   p0: primer valor de la abscisa inicial
%   p1: segundo valor de la abscisa inicial
%   max_iter: número máximo de iteraciones
%   deltaRel: error relativo entre iteraciones consecutivas. Si es menor,
%       el programa finaliza aunque no haya alcanzado max_iter. Indique 0
%       para que se hagan max_iter iteraciones
% Salida:
%   p: vector columna de tamaño i con la sucesión de puntos p que convergen a alguna
%       solución de f(p) = 0
%   err_rel: vector columna de tamaño i. Tiene el error relativo entre
%       p(n) y p(n-1) para todos los p excepto el primero. El primer p
%       tiene error NaN porque no existe número anterior a él que permita
%       calcularlo.
%           El tamaño i es el número de iteraciones que se han hecho hasta que se
%           ha finalizado el algoritmo.

% Allocamos la memoria máxima que usa o puede usar el programa
% Inicializar en NaN para luego eliminar lo que sobre.
p = NaN(max_iter, 1);
err_rel = p;

% Inicialización variables
% Asignación datos iniciales para la convergencia
p(1)=p0;
p(2)=p1;
% Asignación inicial para el error. Imposible calcular
err_rel(1) = NaN;
err_rel(2) = abs(p(2)-p(1))/(abs(p(2)) + eps); % Nótese el uso de eps para no dividir por cero

j=2; % Inicialización contador

% Calcula la sucesión
while ( (err_rel(j)>=deltaRel) || isnan(err_rel(j)) ) && (j <= max_iter)
    p(j+1)=p(j) - f(p(j)).*(p(j)-p(j-1))./(f(p(j))-f(p(j-1)));
    err_rel(j+1)=abs(p(j+1)-p(j))/(abs(p(j+1)) + eps); % Nótese el uso de eps para no dividir por cero
    j=j+1;
end % Del bucle de iteraciones

% Elimina los NaNs finales (recorta los vectores columna)
invID = max_iter;
while isnan(p(invID)) % Así no obtengo un NaN. Véase función.
    invID = invID - 1;
end % Del bucle para cortar los arrays

p = p(1:invID);
err_rel = err_rel(1:invID);

end % De la función
