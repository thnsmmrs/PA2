import numpy
import matplotlib
from scipy.interpolate import CubicSpline

L1 = 1.0
L2 = 0.5

px = numpy.array(5)
py = numpy.array(5)
#DEBUG: print(px, " ", py)

#Spline
cs = CubicSpline(x,y)
xs = numpy.linspace(x[0]-0.5, x[-1]+0.5, 400)

fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(x, y, 'o', label='data')
ax.plot(xs, cs(xs), label='S(x)')
ax.plot(xs, cs(xs, 1), label="S'(x)")
ax.plot(xs, cs(xs, 2), label="S''(x)")
ax.plot(xs, cs(xs, 3), label="S'''(x)")
ax.set_xlim(x[0]-0.5, x[-1]+0.5)
ax.legend(loc='best')
ax.grid(True)
plt.show()

r = numpy.sqrt(px**2 + py**2)
theta1 = numpy.arctan2(py,px) - numpy.arccos((r**2+L1**2-L2**2)/(2*r*L1))
theta2 = numpy.pi - numpy.arccos((L1**2+L2**2-r**2)/(2*L1*L2))

#DEBUG: print (theta1, " ", theta2)
