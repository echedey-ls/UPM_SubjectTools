% Autor: Echedey Luis Álvarez
% Fecha: 07/03/2021
% 
% Aplicación general del método de Newton-Raphson.

function [p, err_rel] = metodo_newton_raphson(f, df, p0, max_iter, deltaRel)
% ----Aproxima la raíz de una función por el método de Newton-Raphson------
% Argumentos:
%   f: función a calcular raíz
%   df: primera derivada de f
%   p0: valor de la abscisa inicial
%   max_iter: número máximo de iteraciones
%   deltaRel: error relativo entre iteraciones consecutivas. Si es menor,
%       el programa finaliza aunque no haya alcanzado max_iter. Indique 0
%       para que se hagan max_iter iteraciones
% Salida:
%   p: vector columna de tamaño i con la sucesión de puntos p que convergen
%       a alguna solución de f(p) = 0
%   err_rel: vector columna de tamaño i. Tiene el error relativo entre
%       p(n) y p(n-1) para todos los p excepto el primero. El primer p
%       tiene error NaN porque no existe número anterior a él que permita
%       calcularlo.
%           El tamaño i es el número de iteraciones que se han hecho hasta
%           que se ha finalizado el algoritmo.

% Allocamos la memoria máxima que usa o puede usar el programa
% Inicializar en NaN para luego eliminar lo que sobre.
p = NaN(max_iter, 1);
err_rel = p; % El primero no se calculará porque no se puede sin otro dato inicial

% Inicialización variables
p(1)=p0; % Asignación dato inicial para la convergencia

j=1; % Inicialización contador
g = @(x) x - f(x)./df(x); % Función del método iterativo

% Calcula la sucesión
while ( (err_rel(j)>=deltaRel) || isnan(err_rel(j)) ) && (j <= max_iter)
    p(j+1)=g(p(j));
    err_rel(j+1)=abs(p(j+1)-p(j))/abs(p(j+1) + eps);
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
