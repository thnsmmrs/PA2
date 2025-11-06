import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

L1 = 1.0
L2 = 0.5
min,max = abs(L1-L2), L1+L2

#defining max and min work space (circles)
t = np.linspace(0, 2*np.pi, 1000)
x_min, y_min = min*np.cos(t), min*np.sin(t)
x_max, y_max = max*np.cos(t), max*np.sin(t)

#defining graph based on max and min provided in problem
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

#Spline creation

#arc params (from SciPy documentation attached on git)
ds = np.hypot(np.diff(px), np.diff(py))
s = np.concatenate(([0.0], np.cumsum(ds)))

#Spline sampling (for smooth connection)
splinepoint_px = CubicSpline(s, px)
splinepoint_py = CubicSpline(s, py)
su = np.linspace(s[0],s[-1],400)
x_splinetrace = splinepoint_px(su)
y_splinetrace = splinepoint_py(su)

graph.plot(px, py, 'x')
graph.plot(x_splinetrace, y_splinetrace)
plt.pause(0.5) #makes it so the figure doesn't have to close for sim to work

r = np.sqrt(x_splinetrace**2 + y_splinetrace**2)
theta1_array = np.arctan2(y_splinetrace,x_splinetrace) - np.arccos((r**2+L1**2-L2**2)/(2*r*L1))
theta2_array = np.pi - np.arccos((L1**2+L2**2-r**2)/(2*L1*L2))

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

outOfBoundsMin = False
outOfBoundsMax = False

for i in range(len(fk_x1)):
    #Matplotlib animation documentation used for set data functions (originally was plotting all points)
    if(outOfBoundsMax == 0 and outOfBoundsMin == 0):
        link1.set_data([0, fk_x1[i]], [0, fk_y1[i]])
        link2.set_data([fk_x1[i], fk_x2[i]], [fk_y1[i], fk_y2[i]])
        trace.set_data([fk_x2[i]], [fk_y2[i]])
        plt.pause(0.001) #Change time var based on how fast/slow we want the sim

    #Boundary conditions (DEBUG)
    link2_mag = np.sqrt(fk_x2[i]**2 + fk_y2[i]**2)
    link2_mag_prev = np.sqrt(fk_x2[i-1]**2 + fk_y2[i-1]**2)
    #DEBUG: print(x_splinetrace[i], y_splinetrace[i], "\n")


    #Boundary handling past maximum
    #DEBUG: print(link2_mag,"\n")
    if (np.isnan(link2_mag) and link2_mag_prev > L1 or outOfBoundsMax):
        outOfBoundsMax = True
        #DEBUG: print("out of bounds (max)")
        thetaOutMax = np.arctan2(y_splinetrace[i], x_splinetrace[i])
        #print(thetaOutMax,"\n")
        #plots links with angle of spline that should be traced
        link1.set_data([0,L1*np.cos(thetaOutMax)], [0,L1*np.sin(thetaOutMax)])
        link2.set_data([L1*np.cos(thetaOutMax),L1*np.cos(thetaOutMax)+L2*(np.cos(thetaOutMax))],[L1*np.sin(thetaOutMax),L1*np.sin(thetaOutMax)+L2*(np.sin(thetaOutMax))])
        trace.set_data([L1*np.cos(thetaOutMax)+L2*(np.cos(thetaOutMax))],[L1*np.sin(thetaOutMax)+L2*(np.sin(thetaOutMax))])
        plt.pause(0.001)
        if (np.isnan(link2_mag) == 0):
            outOfBoundsMax = False

    #Boundary handling past minimum
    if (np.isnan(link2_mag) and link2_mag_prev < L1 or outOfBoundsMin):
        outOfBoundsMin = True
        #DEBUG: print("out of bounds (min)")
        thetaOutMin = np.arctan2(y_splinetrace[i], x_splinetrace[i])
        #print(thetaOutMin,"\n")
        #plots links with angle of spline that should be traced
        link1.set_data([0,L1*np.cos(thetaOutMin)], [0,L1*np.sin(thetaOutMin)])
        link2.set_data([L1*np.cos(thetaOutMin),L1*np.cos(thetaOutMin)-L2*(np.cos(thetaOutMin))],[L1*np.sin(thetaOutMin),L1*np.sin(thetaOutMin)-L2*(np.sin(thetaOutMin))])
        trace.set_data([L1*np.cos(thetaOutMin)-L2*(np.cos(thetaOutMin))],[L1*np.sin(thetaOutMin)-L2*(np.sin(thetaOutMin))])
        plt.pause(0.001)
        if (np.isnan(link2_mag) == 0):
           outOfBoundsMin = False
plt.show()
