import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
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

# First we need the empirical variogram, which is essentially just a direct collection
# of all the semivariances of every value in the map.
def empirical_semivariance(x, y, values):
    # Convert inputs to numpy arrays if they are not already
    x = np.array(x)
    y = np.array(y)
    values = np.array(values)

    # Calculate pairwise distances using broadcasting
    dx = x[:, np.newaxis] - x[np.newaxis, :]
    dy = y[:, np.newaxis] - y[np.newaxis, :]
    distances = np.sqrt(dx**2 + dy**2)

    # Calculate pairwise semivariance (0.5 * (value_i - value_j)^2)
    value_diff = values[:, np.newaxis] - values[np.newaxis, :]
    semivariances = 0.5 * value_diff**2

    # Flatten the arrays and exclude the diagonal (i == j), which is 0 distance
    tril_indices = np.tril_indices(len(x), -1)  # Get lower triangle indices to avoid double counting

    distances = distances[tril_indices]
    semivariances = semivariances[tril_indices]

    return distances, semivariances

# Get the empirical variogram
distances, semivariances = empirical_semivariance(_x, _y, _p)

# Now define the different variogram models

def spherical_variogram(h, nugget, sill, r):
    # Spherical model equation
    return nugget + sill * (1.5 * (h/r) - 0.5 * (h/r)**3) * (h <= r) + sill * (h > r)

def exponential_variogram(h, nugget, sill, r):
    # Exponential model equation
    return nugget + sill * (1 - np.exp(-h/r))

def gaussian_variogram(h, nugget, sill, r):
    # Gaussian model equation
    return nugget + sill * (1 - np.exp(-(h/r)**2))


# Let's make a new figure and plot the empirical variogram
plt.figure(figsize=(8, 6))
plt.scatter(distances, semivariances, label="Empirical Variogram", color='blue', alpha=0.1)

# Now we need to fit the different variograms to the empirical variogram
avg_distance = np.mean(distances)  # Average distance between points
r_guess = avg_distance  # Start with the average distance
sill_guess = np.max(_p) - np.min(_p)


params, _ = opt.curve_fit(exponential_variogram, distances, semivariances, p0=[0.5, sill_guess, r_guess])
print(params)
fitted_variogram = exponential_variogram(distances, *params)

# Plot the fitted variogram
plt.plot(distances, fitted_variogram, label="Fitted Spherical Model", color='red')

plt.xlabel('Distance')
plt.ylabel('Semivariance')
plt.title('Empirical vs Fitted Variogram')
plt.legend()
plt.show()