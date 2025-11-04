import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

L1 = 1.0
L2 = 0.5
min,max = abs(L1-L2), L1+L2

#defining plotting standards
t = np.linspace(0, 2*np.pi, 1000)
x_min, y_min = min*np.cos(t), min*np.sin(t)
x_max, y_max = max*np.cos(t), max*np.sin(t)

fig, graph = plt.subplots()
graph.plot(x_min, y_min)
graph.plot(x_max, y_max)
graph.set_xlim(-1*max,max)
graph.set_ylim(-1*max,max)
plt.title("Click 5 points inside the workspace")
points = plt.ginput(5, timeout=-1)

points = np.array(points)

px = points[:, 0]
py = points[:, 1]
#DEBUG: print(px, " ", py)

#Spline

#arc params (from SciPy documentation)
ds = np.hypot(np.diff(px), np.diff(py))
s = np.concatenate(([0.0], np.cumsum(ds)))

#Spline sampling (for smooth connection)
sx = CubicSpline(s, px)
sy = CubicSpline(s, py)
su = np.linspace(s[0],s[-1],400)
xs = sx(su)
ys = sy(su)

graph.plot(px, py, 'x')
graph.plot(xs, ys)
plt.pause(0.5)

r = np.sqrt(px**2 + py**2)
theta1 = np.arctan2(py,px) - np.arccos((r**2+L1**2-L2**2)/(2*r*L1))
theta2 = np.pi - np.arccos((L1**2+L2**2-r**2)/(2*L1*L2))

#DEBUG: print (theta1, " ", theta2)

#FK arrays based on theta1 theta2 to plot the link positions
fk_x1 = L1*np.cos(theta1_array)
fk_x2 = fk_x1 + L2*(np.cos(theta1_array+theta2_array))
fk_y1 = L1*np.sin(theta1_array)
fk_y2 = fk_y1 + L2*(np.sin(theta1_array+theta2_array))

#vars to plot manipulator movement 
link1, = graph.plot([], [])
link2, = graph.plot([], [])
trace, = graph.plot([], [])

outOfBoundsMax = False
outOfBoundsMin = False


for i in range(len(fk_x1)):
    #Matplotlib animation documentation used for set data functions (originally was plotting all points)
    link1.set_data([0, fk_x1[i]], [0, fk_y1[i]])
    link2.set_data([fk_x1[i], fk_x2[i]], [fk_y1[i], fk_y2[i]])
    trace.set_data([fk_x2[i]], [fk_y2[i]])
    plt.pause(0.001) #Change time var based on how fast/slow we want the sim

    #Boundary conditions (DEBUG)
    link2_mag = np.sqrt(fk_x2[i]**2 + fk_y2[i]**2)
    link2_mag_prev = np.sqrt(fk_x2[i-1]**2 + fk_y2[i-1]**2)


    print(link2_mag,"\n")
    if (np.isnan(link2_mag) and link2_mag_prev > L1 or outOfBoundsMax):
        outOfBoundsMax = True
        print("out of bounds (max)")
    elif(link2_mag > min and link2_mag < max):
        outOfBoundsMin = False  
        outOfBoundsMax = False
plt.show()
