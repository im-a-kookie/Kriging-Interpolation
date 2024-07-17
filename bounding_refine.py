import math

### defines the boundaries for the given points
# basically turns some random arbitrary range
# into a nicely shaped region
def refine_boundary(x0, y0, x1, y1):
    _w = x1 - x0
    _h = y1 - y0
    
    omw = 10**math.floor(math.log10(_w) - 1)
    omh = 10**math.floor(math.log10(_h) - 1)

    x0 = math.floor(x0 / omw) * omw;
    y0 = math.floor(y0 / omh) * omh;
    x1 = math.ceil(x1 / omw) * omw;
    y1 = math.ceil(y1 / omh) * omh;

    return [x0, y0, x1, y1]

