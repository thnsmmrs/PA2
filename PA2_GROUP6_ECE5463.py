"""
Missing code sections PA2
 1. Integrate clicking input with px py arrays
 2. Use IK equations to solve for theta1 and theta2 arrays based on px py
 3. Simulation
 """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Section 1: integrate clicking input with px, py arrays
# After line 25 in PA2.py, add the following:
print("\nUser clicked points:")
for i in range(len(px)):
    print(f"  Point {i+1}: ({px[i]:.3f}, {py[i]:.3f})")

# Section 2: Using IK equations to solve for theta1 and theta2 arrays based on px, py
# After line 39 (ys = sy(su)), add the following
r = np.sqrt(xs**2 + ys**2)
theta1 = np.arctan2(ys,xs) - np.arccos((r**2 + L1**2 - L2**2) / (2 * r * L1))
theta2 = np.pi - np.arccos((L1**2 + L2**2 - r**2) / (2 * L1 * L2))

print(f"\nInverse kinematics solved for {len(theta1)} configurations")

# Section 3: Create animation (goes after all plotting/IK code/spline)

def forward_kinematics(theta1_val, theta2_val):
    """
    Calculating the link positions from joint angles

    theta1_val = Joint 1 angle (radians)
    theta2_val = Joint 2 angle (radians)

    The function returns:
    - Positions (x0, y0, x1, y1, x2, y2), where (x0, y0) = base position,
    (x1, y1) = joint 1 position, (x2, y2) = end-effector position
    """
    # Base position at origin
    x0,y0 = 0,0

    # Joint 1 position
    x1 = L1 * np.cos(theta1_val)
    y1 = L1 * np.sin(theta1_val)

    # End-effector position
    x2 = x1 + L2 * np.cos(theta1_val + theta2_val)
    y2 = y1 + L2 * np.sin(theta1_val + theta2_val)

    # Return everything
    return x0, y0, x1, y1, x2, y2
