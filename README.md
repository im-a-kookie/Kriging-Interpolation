# Kriging Interpolation

A simple example of Kriging Interpolation using Python and NumPy.

Kriging Interpolation is a standard interpolation method with primary use in geostatics, providing unbiased linear prediction of values across linearly continuous datasets. Kriging interpolation can be broken down into two main components; the variogram and calculation of covariances, and the maximization of the resulting probability field.

# Covariance

The variogram describes the spatial variance of random variables around a given point and models how this variance changes with distance. In other words, as linearly continuous data transitions relatively smoothly, the variogram provides a description of the average gradient. An optimal variogram can be fitted by calculating the empirical semi-variogram from the data and then finding a function of best fit through regression. For simplicity, a simple spherical variogram is used in this example.

# Maximization

If a value Z is randomly guessed for a given point, the variogram models the probability of this guess being correct. Implicitly, this is maximized at the mean value of the probability distribution, so the mean regression provides the best linear estimate of Z. By constructing the variograms as a description of of residuals (rather than of the actual gradient itself), the sum of errors will implicitly converge to 0, meaning that this estimate is unbiased (aka, that it does not introduce systematic under- or over-estimation).

# Summary

Maths is fully vectorized via NumPY and plotted with MatPlotLib. A spherical variogram method is selected as the most common and versatile approach. Variogram selection is an extensive topic beyond the scope of this project.

Requires: matplotlib, numPy
