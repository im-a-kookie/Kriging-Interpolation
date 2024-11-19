# Kriging Interpolation

A simple example of Kriging Interpolation using Python and NumPy.

Kriging Interpolation is a linear interpolation method, used primarily for geostatics. The process can be broken down into two main components. 

# The Variogram

The variogram describes the values of the random variables around a given point. This is a probabilistic description based on the gradients of the provided data, and typically resembles a sigmoid function. Essentially, linearly continuous data (e.g geographic data) transitions relatively smoothly between adjacent points. By finding the average gradient of this transition, we can make statistical predictions about the total change across a given interval.

# Maximization

If a value is randomly chosen for a given point, the variogram describes the probability of that value being correct based on the known data. This probability is maximized at the mean value of the probability distribution. Therefore, the sum of the distance-weighted means of all overlapping variograms, provides the best linear prediction of the value at any given point.

By constructing the variogram as a description of the distance of the value from the mean, we can ensure that the sum of the errors is 0, which means that the above linear prediction will be unbiased.

# Summary

Maths is fully vectorized via NumPY and plotted with MatPlotLib. A spherical variogram method is selected as the most common and versatile approach. Variogram selection is currently beyond the scope of this project.

Requires: matplotlib, numPy
