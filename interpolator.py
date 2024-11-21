import numpy as np

import matplotlib.pyplot as plot
from matplotlib.widgets import Slider, Button
from matplotlib.colors import Normalize

import csv_reader as f #simple thing that does magic
import bounding_refine as refiner #simple thing that does magic

import math
import threading

TARGET_COLUMN = "porosity"

#default target resolution in horizontal units
chart_resolution = 50
#default radius for the variogram search
variogram_radius = 800

#load the csv data using the simple thing that does magic
data = f.loadcsv("geostats_data.csv")
print("Loaded CSV...")

# Now we can just get the columns because yes
_x = np.array(data.get("X"))
_y = np.array(data.get("Y"))
_p = np.array(data.get(TARGET_COLUMN))

count = len(_x)

if (len(_x) != len(_y) or len(_x) != len(_p)):
    print("Fatal Error: Data columns are unmatched sizes!")
    exit(0)

#First we should automatically calculate something resembling a good bounding area

min_x = np.min(_x)
min_y = np.min(_y)
max_x = np.max(_x)
max_y = np.max(_y)

# Refine the min/max bounds to something tidy
boundary = refiner.refine_boundary(min_x, min_y, max_x, max_y)
x0 = boundary[0]
y0 = boundary[1]
x1 = boundary[2]
y1 = boundary[3]

# Print some updates about where it's at
print(f"Data Bounds: [{min_x},{min_y}] to [{max_x},{max_y}]")
print(f"View Bounds: [{x0},{y0}] to [{boundary[2]},{boundary[3]}]")
print(f"Dataset Prepared! Variable: {TARGET_COLUMN}")


# We need to know the distances between every single point in the array
def calculate_distance_matrix(x, y):
    assert len(x) == len(y)
    # create the nxn arrays
    # Then subtract the x[0] and y[0] values across the matrix
    x_diff = x[:, np.newaxis] - x[np.newaxis, :]
    y_diff = y[:, np.newaxis] - y[np.newaxis, :]
    # Now compute the euclidiean distances
    distances = np.sqrt(x_diff**2 + y_diff**2)
    return distances


# caculates the distances of every point to the given point
def calculate_distances_to_point(posx, posy, x, y):
    return np.sqrt(np.add((x - posx)**2, (y - posy)**2))

# The variogram provides an estimate of the variance of the distribution,
# In this casae, we will use a spherical variogram of a given radius,
def calculate_spherical_variogram(distances, radius):
    partials = np.clip(-999, 1, distances / radius)
    variogram = 1.5 * partials - 0.5 * partials**3
    return variogram

# A linear variogram can be constructed simply by the following;
def calculate_linear_variogram(distances, radius):
    return distances / radius

# A gaussian variogram can also be made pretty easily
def calculate_gaussian_variogram(distances, radius):
    return 1 - np.exp(-(distances / radius) ** 2)


def compute_kriging(resolution, radius):

    # compute the resolution amounts
    # use the resolution as a vertical resolution
    # since that's what screens do. Unsure if this is correct convention for geostatics.
    scale_y = resolution + 1
    scale_x = math.floor(scale_y * (y1 - y0) / (x1 - x0))
    print(f"Computing {scale_x}x{scale_y} Interpolation...")

    #calculate and store the array of all distances
    dists = calculate_distance_matrix(_x, _y)
    # and the semivariance function, which wee can invert now
    inv_variogram = np.linalg.inv(1 - calculate_spherical_variogram(dists, radius))
    
    # calculate the mean and residuals
    mean = np.sum(_p) / count
    residuals = _p - mean
    
    # Create a plot for graphing the interpolated values to
    xaxis = np.linspace(x0, x1, scale_x, endpoint=True)
    yaxis = np.linspace(y0, y1, scale_y, endpoint=True)
    # Remember, numpy indexes work backwards, so the indices have to be backdy-doody :D
    kriging = np.zeros((scale_y, scale_x)) #gridx tells us the entire dimensionality

    for i in range(scale_x):
        for j in range(scale_y):
            # now get the local distance and covariance matrix
            # we need to refer to gridy[i,j] for the stepped y value
            local_distances = calculate_distances_to_point(xaxis[i], yaxis[j], _x, _y)
            local_covariances = 1 - calculate_spherical_variogram(local_distances, radius)
            # the weight values are found by the matrix product of the semivariances
            weights = np.matmul(local_covariances, inv_variogram)
            kriging[j,i] = np.sum(residuals * weights) + mean
    return kriging

#set up the plot
fig, ax = plot.subplots()

plot.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9)
#set up the heatmap from the interpolated kriging array
#and scatterplot the known x/y values
heatmap = ax.imshow(np.zeros((chart_resolution, chart_resolution)), cmap='viridis', extent=(x0, x1, y0, y1), origin='lower')
scatter = ax.scatter(_x, _y, c=_p, edgecolors='k', marker='o')
mappable = ax.collections[0]

#set up the axis titles and labels and so on
plot.colorbar(mappable, label='Porosity')
ax.set_title('Interpolated Porosity (Kriging, Spherical Semivariance)')
ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')

#callback to update the plot resolution
def update_res(val):
    global chart_resolution
    chart_resolution = val
    
#callback to update the variogram radius
def update_rad(val):
    global variogram_radius
    variogram_radius = val

def update_plot(event):
    do_thing(chart_resolution, variogram_radius)

#what's main() anyway
# this function just recalculates the kriging and pushes it to the grid
def do_thing(resolution, radius):
    kriging = compute_kriging(resolution, radius)
    heatmap.set_data(kriging)
    #As the ranges might have changed, we should renormalize the colors
    norm = Normalize(vmin=kriging.min(), vmax=kriging.max())
    heatmap.set_norm(norm)
    #done, redraw
    fig.canvas.draw_idle()

# configure the sliders and buttons
# Adjusting these values will move the buttons and sliders around
slider_res_axis = plot.axes([0.25, 0.12, 0.5, 0.03]) 
slider_rad_axis = plot.axes([0.25, 0.07, 0.5, 0.03]) 
button_go_axis = plot.axes([0.7, 0.015, 0.1, 0.04])
#and configure the actual slider areas and callbacks
slider_res = Slider(slider_res_axis, 'Resolution', 10, 400, valinit=chart_resolution, valstep=1)  # Create the slider object
slider_res.on_changed(update_res)  # Link slider to update function
slider_rad = Slider(slider_rad_axis, 'Radius', 1, (max_x - min_x) * 2**0.5, valinit=variogram_radius, valstep=1)  # Create the slider object
slider_rad.on_changed(update_rad)  # Link slider to update function
button = Button(button_go_axis, 'Update')  # Create the button object
button.on_clicked(update_plot)  # Link button to update function

#do an initial grid population
do_thing(chart_resolution, variogram_radius)

plot.show()


