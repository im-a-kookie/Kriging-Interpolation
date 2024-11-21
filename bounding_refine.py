import math

### defines the boundaries for the given points.
# Essentially, this method takes a given range of x/y values
# and finds a constraining area that;
#1. Contains the given region
#2. Has nice boundaries (e.g multiples of 10/100/..) matching the magnitude of the area
def refine_boundary(x0, y0, x1, y1):
    #get the actual width/height
    _w = x1 - x0
    _h = y1 - y0
    
    #calculate the magnitude of the width and height in base 10
    om_width = 10**math.floor(math.log10(_w) - 1)
    om_height = 10**math.floor(math.log10(_h) - 1)

    #now floor/ceil the values to the nearest multiple of the magnitude
    x0 = math.floor(x0 / om_width) * om_width;
    y0 = math.floor(y0 / om_height) * om_height;
    x1 = math.ceil(x1 / om_width) * om_width;
    y1 = math.ceil(y1 / om_height) * om_height;

    return [x0, y0, x1, y1]

