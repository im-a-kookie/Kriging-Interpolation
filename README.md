# Kriging Interpolation

A simple example of Kriging Interpolation using Python and NumPy.

Kriging Interpolation is a standard interpolation method with primary use in geostatics, providing unbiased linear prediction of values across linearly continuous datasets. Kriging interpolation can be broken down into two main components; the variogram and calculation of covariances, and the maximization of the resulting probability field.

# Covariance

The variogram describes the spatial variance of random variables around a given point and models how this variance changes with distance. In other words, as linearly continuous data transitions relatively smoothly, the variogram provides a description of the average gradient. An optimal variogram can be fitted by calculating the empirical semi-variogram from the data and then finding a function of best fit through regression. For simplicity, a simple spherical variogram is used in this example.

# Maximization

Considering some unknown variable Z, the variogram describes the spatial correlation of Z with the known datapoints. Framed differently, this correlation informs the probability that some random guess for Z will be "correct," and implicit in probability theory is that mean probability informs function maxima.

Therefore, implicitly, if we take the distance-weighted spatial correlation of Z with every known point, the conditional mean will provide the best linear estimate of Z. By constructing the variograms as a description of of residuals (rather than of the actual gradient itself), the sum of errors will implicitly converge to 0, meaning that this estimate is unbiased (aka, that it does not introduce systematic under- or over-estimation).

# Summary

Maths is fully vectorized via NumPY and plotted with MatPlotLib. A spherical variogram method is selected as the most common and versatile approach. Variogram selection is an extensive topic beyond the scope of this project.

Requires: matplotlib, numPy
