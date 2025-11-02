import numpy
from scipy.interpolate import CubicSpline


L1 = 1.0
L2 = 0.5
px = float(input("Enter px: "))
py = float(input("Enter py: "))
print(px, " ", py)


r = numpy.sqrt(px**2 + py**2)
theta1 = numpy.arctan2(py,px) - numpy.arccos((r**2+L1**2-L2**2)/(2*r*L1))
theta2 = numpy.pi - numpy.arccos((L1**2+L2**2-r**2)/(2*L1*L2))

print (theta1, " ", theta2)