import numpy as np
import matplotlib.pyplot as pt

# Parameters
L1 = 1
L2 = 0.5
theta = np.linspace(0, 2 * np.pi, 100)
# Creating circles for plot
bigx = (L1+L2)*np.cos(theta)
bigy = (L1+L2)*np.sin(theta)
smallx = (L1-L2)*np.cos(theta)
smally = (L1-L2)*np.sin(theta)

# Plot
fig, ax = pt.subplots()
ax.fill(bigx, bigy, color='gray', zorder=0)
ax.fill(smallx, smally, color='white', zorder=1)
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_title("Click 5 points")
ax.set_xlabel("X(m)")
ax.set_ylabel("Y(m)")
plot = pt.ginput(5, timeout=-1)
pt.pause(1)
pt.show()
