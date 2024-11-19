# Kriging Interpolation

A simple example of Kriging Interpolation using Python and NumPy.

Kriging Interpolation is a standard interpolation method with primary use in geostatics. It provides the best unbiased linear prediction of values across linearly continuous datasets. Kriging interpolation can be broken down into two main components; the variogram and calculation of covariances, and the maximization of the resulting probability field.

# The Variogram

The variogram describes the values of the random variables around a given point. This is a probabilistic description based on the gradients of the provided data. Essentially, linearly continuous data (e.g geographic data) transitions relatively smoothly between adjacent points. Through a mathematical description of the gradient of this transition, we can make statistical predictions about the total change across a given interval.

Many different methods exist for creating this mathematical description. In this case, the spherical variogram is selected, being the most common and versatile approach.

# Maximization

If a value is randomly chosen for a given point, the variogram describes the probability of that value being correct based on the known data. This probability is maximized at the mean value of the probability distribution. Therefore, the sum of the distance-weighted means of all overlapping variograms, provides the best linear prediction of the value at any given point.

By constructing the variogram as a description of the distance of the value from the mean, we can ensure that the sum of the errors is 0, which means that the above linear prediction will be unbiased.

# Summary

Maths is fully vectorized via NumPY and plotted with MatPlotLib. A spherical variogram method is selected as the most common and versatile approach. Variogram selection is an extensive topic beyond the scope of this project.

Requires: matplotlib, numPy
