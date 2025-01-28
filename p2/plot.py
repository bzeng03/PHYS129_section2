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
x_filtered = x[mask]
y_filtered = y[mask]
z_filtered = z2[mask]

# Generate the Delaunay triangulation only for the filtered points
points_filtered = np.vstack((x_filtered, y_filtered)).T
tri = Delaunay(points_filtered)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot only the meshed surface where surface2 > surface1
ax.plot_trisurf(
    x_filtered, y_filtered, z_filtered, 
    triangles=tri.simplices, cmap='plasma', edgecolor='none', alpha=0.8
)

# Add labels and title
ax.set_title("Delaunay Mesh for Region Where Surface2 > Surface1")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Show the plot
plt.show()
plt.savefig("delaunay_filtered_mesh.png")