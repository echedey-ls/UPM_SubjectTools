% Autor: Echedey Luis Álvarez
% Fecha: 07/03/2021
% 
% Ejercicio 24 de marzo
%{
Calcular el punto de la gráfica más próximo a P, dibujar la gráfica y aplicar el método de la secante
Condiciones: error menor a 1e-10
%}

%% Sección 1. Inicialización
% Limpieza de la zona de trabajo
clear, clc;
format long;
% ¿Estamos en Octave?
isOctave = exist('OCTAVE_VERSION', 'builtin');

% Función del ejercicio
h = @(x) sin( x - cos(x) );
dh = @(x) cos( x - cos(x) ).*( 1 + sen(x) );
elPtoP = [-1.63, 0.28];
%% Sección 2. Representar gráficamente la función en el intervalo [−3,6]
% Y ya que estamos el punto también
% _Comprobamos que lo que necesitamos existe_

if ( exist("elPtoP","var") ~= 1 )
    disp("Primero debes ejecutar el código de la primera sección.");
    return;
end
% Graficamos la función y el punto

xpoints = linspace(-3, 6, 100); % Vector con coordenadas en X a imprimir. 100 puntos.
ypoints = h(xpoints); % Vector con imágenes de X a imprimir

plot(xpoints, ypoints, "b-", elPtoP(1), elPtoP(2), "rx");
legend("h(x)", "Punto P");

%% Sección 3. Determinar el punto de la gráfica de _h_ que está más próximo a _P_
% _Comprobamos que lo que necesitamos existe_
% Nótese cuanto me gusta reciclar código del ejercicio 11 que hice hace tiempo.

% Si no has inicializado la primera parte pues muy mal
if ( (exist("h","var")~=1) || (exist("dh","var")~=1) || (exist("elPtoP","var")~=1) )
    disp("Primero debes ejecutar el código de la primera sección.");
    return;
end
% Y si no has descargado el script que aplica el método pues aún peor
if (exist("metodo_secante.m", "file")~=2)
    disp("No está el script que calcula una raíz por el método de la secante. Descargue los archivos.");
    return;
end
% _Buscamos las soluciones, y graficamos todo_

dist_h_P = @(x) sqrt((x - elPtoP(1)).^2 + ( h(x) - elPtoP(2) ).^2); % Indica la distancia entre un punto cualquiera de la función y el punto P
% >> syms x
% >> diff(dist_h_P(x)) % Esto es para hallar la derivada
dif_dist_h_P = @(x) (2.*x + 2.*cos(x - cos(x)).*(sin(x) + 1).*(sin(x - cos(x)) - 7/25) + 163/50)./(2.*((x + 163/100).^2 + (sin(x - cos(x)) - 7/25).^2).^(1/2));

xpoints = linspace(-3, 6, 1000); % Vector con coordenadas en X a imprimir. 100 puntos.
ypoints_dist = dist_h_P(xpoints); % Vector con imágenes de X a imprimir
ypoints_dif_dist = dif_dist_h_P(xpoints); % Vector con imágenes de X a imprimir

plot(xpoints, ypoints_dist, "k-", xpoints, ypoints_dif_dist, "m-.");
grid on;
legend("dist_h_P", "dif_dist_h_P");
% disp("Debe de haber algo mal porque en el mínimo que veo hacia -1.5 la
% derivada no se hace nula") %Falso, estoy bobo

% Vemos que existen 3 soluciones ara dif_dist_h_P(x) = 0, de las cuales la que 
% está entre -2 y -1 es el mínimo de dist_h_P(x). Por ello eligo los puntos -1 
% y -1.5 como iniciales, así a ojo.

cutoff_delta = 1e-10;
n_max_iters = 10;

pto0x = -1;
pto1x = -1.5;

[p, err] = metodo_secante(dif_dist_h_P, pto0x, pto1x, n_max_iters, cutoff_delta);
table(p, err)

if (isOctave);
  disp("El punto más cercano es: ");
  disp(p(end));
  disp("Para el cual la distancia vale: ");
  disp(dist_h_P(p(end)));
else
  disp("El punto más cercano es "+p(end)+" para el cual la distancia vale "+dist_h_P(p(end)));
 end