# Kriging Interpolation

A simple example of Kriging Interpolation using Python and NumPy.

Kriging Interpolation is a linear interpolation method, used primarily for geostatics. The process can be broken down into two main steps. 

# Variogram

First, we need a variogram, which describes the probabilistic values of the considered area around each point. Essentially, in linearly continuous data, particularly geographic and demographic data, we expect adjacent datapoints to transition relatively smoothly. By approximating the approximate gradient of this transition, or 'variation,' a variogram can be constructed which suggests a probable range of values of any point, based on the adjacent values.

For example, say that the height of the terrain changes by an average of 1 meter per unit of the map. Therefore, from a known height reading, if we travel one unit in any direction, we can expect an average change in height of 1 meter. Indeed, we can now calculate the value of this destination probabilistically, creating a probability distribution that can be projected around each point. Many methods exist for calculating this distribution. In this example, a simple Spherical approach has been selected.

# Maximize

Second, we must combine these variograms to calculate, in simple terms: the value which best satisfies every overlapping probability distribution. More technically, we simply need to sum up the biased means, of every overlapping distribution at this point. The bias in this case, is essentially given by the "knowability" of the point, for which we can simply use Euclidian distance - as the data can be assumed to be linearly continuous, uncertainty grows very proportionately to the distance from a known value.

Quite usefully, by considering the breadth of the probability distributions at each point, we can also predict, in statistical form, the expected level of uncertainty (or error) at each calculated point.

# Summary

Maths is fully vectorized, uses a simple Spherical variogram construction, and uses MatPlotLib to plot the results visually.

Csv data files taken from https://github.com/GeostatsGuy/GeoDataSets/

Requires: matplotlib, numPy
