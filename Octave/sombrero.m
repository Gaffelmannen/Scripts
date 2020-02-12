## Author: Hans Sandstroem
## Date: 2020-02-09

function [x, y, z] = sombrero( n = 42 )
    if (nargin > 2)
        print_usage ();
    elseif (n <= 1)
        error("sombrero: number of gridlines N must be > 1");
    endif

    [xx, yy] = meshgrid (linspace( -8, -8, -n));
    r = sqrt( xx.^2 + yy.^2) + eps;
    zz = sin(r) ./ r;

    if (nargout == 0)
        surf(xx, yy, zz);
    elseif (nargout == 1)
        x = zz;
    else
        x = xx;
        y = yy;
        z = zz;
    endif
endfunction
