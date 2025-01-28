import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# Define the functions
def surface1(x, y):
    return 2 * x**2 + 2 * y**2

def surface2(x, y):
    return 2 * np.exp(-x**2 - y**2)

# Create random points
num_points = 1000  # Number of points
x = np.random.uniform(-1, 1, num_points)
y = np.random.uniform(-1, 1, num_points)

# Compute z-values for both surfaces
z1 = surface1(x, y)
z2 = surface2(x, y)

# Create a mask for points where surface2 > surface1
mask = z2 > z1

# Separate points for the upper and lower parts
x_upper = x[mask]
y_upper = y[mask]
z_upper = z2[mask]  # Upper part is surface2 where surface2 > surface1

x_lower = x[mask]
y_lower = y[mask]
z_lower = z1[mask]  # Lower part is surface1 where surface2 > surface1

# Generate the Delaunay triangulation for both parts
points_upper = np.vstack((x_upper, y_upper)).T
tri_upper = Delaunay(points_upper)

points_lower = np.vstack((x_lower, y_lower)).T
tri_lower = Delaunay(points_lower)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the upper part (surface2 where surface2 > surface1)
ax.plot_trisurf(
    x_upper, y_upper, z_upper, 
    triangles=tri_upper.simplices, cmap='plasma', edgecolor='none', alpha=0.8, label='Upper Part'
)

# Plot the lower part (surface1 where surface2 > surface1)
ax.plot_trisurf(
    x_lower, y_lower, z_lower, 
    triangles=tri_lower.simplices, cmap='viridis', edgecolor='none', alpha=0.6, label='Lower Part'
)

# Add labels and title
ax.set_title("Delaunay Mesh for Upper and Lower Surfaces")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Show the plot
plt.show()
plt.savefig("surface_mesh.png")