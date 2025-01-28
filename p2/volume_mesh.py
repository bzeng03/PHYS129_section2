import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.interpolate import griddata

# Define the two surfaces:
def surface1(x, y):
    return 2.0 * x**2 + 2.0 * y**2

def surface2(x, y):
    return 2.0 * np.exp(-x**2 - y**2)

# ---------------------------
# 1) Define a sampling domain
# ---------------------------
N = 20  # number of points along each axis
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)

# -------------------------
# 2) Compute surface values
# -------------------------
Z1 = surface1(X, Y)
Z2 = surface2(X, Y)

# ----------------------------------
# 3) Mask the region where Z2 > Z1
# ----------------------------------
mask = (Z2 > Z1)

# We only keep the points that satisfy the inequality
valid_x = X[mask]
valid_y = Y[mask]

# ------------------------------
# 4) Triangulate in the XY-plane
# ------------------------------
points_2d = np.column_stack([valid_x, valid_y])
tri = Delaunay(points_2d)

# Compute the corresponding z-values for the top and bottom surfaces
top_z = surface2(points_2d[:, 0], points_2d[:, 1])
bot_z = surface1(points_2d[:, 0], points_2d[:, 1])

# -----------------
# 5) Plot in 3D
# -----------------
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the "top" surface (surface2)
ax.plot_trisurf(points_2d[:,0],
                points_2d[:,1],
                top_z,
                triangles=tri.simplices,
                color='blue',
                alpha=0.6,
                edgecolor='none')

# Plot the "bottom" surface (surface1)
ax.plot_trisurf(points_2d[:,0],
                points_2d[:,1],
                bot_z,
                triangles=tri.simplices,
                color='red',
                alpha=0.6,
                edgecolor='none')

# Label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.tight_layout()
plt.show()
plt.savefig("volume_mesh.png")