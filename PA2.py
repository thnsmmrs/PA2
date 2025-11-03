import numpy
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

L1 = 1.0
L2 = 0.5
min,max = abs(L1-L2), L1+L2

#defining plotting standards
t = numpy.linspace(0, 2*numpy.pi, 1000)
x_min, y_min = min*numpy.cos(t), min*numpy.sin(t)
x_max, y_max = max*numpy.cos(t), max*numpy.sin(t)

fig, graph = plt.subplots()
graph.plot(x_min, y_min)
graph.plot(x_max, y_max)
graph.set_xlim(-1*max,max)
graph.set_ylim(-1*max,max)
plt.title("Click 5 points inside the workspace")
points = plt.ginput(5, timeout=-1)

points = numpy.array(points)

px = points[:, 0]
py = points[:, 1]
#DEBUG: print(px, " ", py)

#Spline

#arc params (from SciPy documentation)
ds = numpy.hypot(numpy.diff(px), numpy.diff(py))
s = numpy.concatenate(([0.0], numpy.cumsum(ds)))

#Spline sampling (for smooth connection)
sx = CubicSpline(s, px)
sy = CubicSpline(s, py)
su = numpy.linspace(s[0],s[-1],400)
xs = sx(su)
ys = sy(su)

graph.plot(px, py, 'x')
graph.plot(xs, ys)
plt.show()

r = numpy.sqrt(px**2 + py**2)
theta1 = numpy.arctan2(py,px) - numpy.arccos((r**2+L1**2-L2**2)/(2*r*L1))
theta2 = numpy.pi - numpy.arccos((L1**2+L2**2-r**2)/(2*L1*L2))

#DEBUG: print (theta1, " ", theta2)
