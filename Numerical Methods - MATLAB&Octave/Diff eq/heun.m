% Author: Echedey Luis Álvarez
% Date: 25/05/2021
%
% Abstract: Aplicación general de aproximación de ec. diferenciales por el método de Heun
%   Se utiliza la media de las pendientes en  t_k y t_(k+1)

function E = euler_mod( f, a, b, y_a, M )
%{
    Args:
      f: 2-vars anonym function which represents explicitly the derivative of y
      a & b: begin and end of interval
      y_a: known value of f, f(a)
      M: desired number of iterations. M gets rounded to the nearest int32
    Output:
      E: (M+1) x 3 matrix
        E(:,1): index column (first one is 0)
        E(:,2): independent value (t_k, x_k)
        E(:,3): dependent value (y_k)
%}

    if ( a >= b )
      error("Cannot aproximate within given interval");
    end
    M = double ( uint32 (M) );
    if (M == 0)
      error("Number of iterations must be a natural number");
    end

    h = (b - a) / M;
    E = NaN( [M+1, 3] );
    f1 = f2 = 0;
    E(1, :) = [0, a, y_a];
    for j=1:M
      f1 = f( E(j, 2), E(j, 3) );
      f2 = f( E(j, 2) + h, E(j, 3) + h * f1 );
      E(j+1, :) = [ j, a + j .* h, E(j,3) + h/2 * ( f1 + f2 ) ];
    end % !for
end % !if
