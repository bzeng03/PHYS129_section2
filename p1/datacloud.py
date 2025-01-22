import numpy as np
import matplotlib.pyplot as plt

class DataCloud:
    def __init__(self, points):
        """Initialize the DataCloud object with a set of points."""
        self.points = np.array(points)

    @staticmethod
    def orientation(p, q, r):
        """Determine the orientation of the triplet (p, q, r)."""
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise

    def graham_scan(self):
        """Find the convex hull using the Graham Scan algorithm."""
        points = sorted(self.points, key=lambda x: (x[0], x[1]))
        
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(tuple(p))

        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(tuple(p))

        return lower[:-1] + upper[:-1]

    def jarvis_march(self):
        """Find the convex hull using the Jarvis March algorithm."""
        n = len(self.points)
        if n < 3:
            return []

        hull = []
        l = np.argmin(self.points[:, 0])
        p = l
        while True:
            hull.append(tuple(self.points[p]))
            q = (p + 1) % n
            for i in range(n):
                if self.orientation(self.points[p], self.points[i], self.points[q]) == 2:
                    q = i
            p = q
            if p == l:
                break

        return hull

    def quickhull(self):
        """Find the convex hull using the Quickhull algorithm."""
        def cross(o, a, b):
            """Compute the cross product of vectors OA and OB."""
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        def add_hull(points, p1, p2):
            """Recursively find points on one side of the line p1-p2."""
            if not points:
                return []
            
            # Find the farthest point from the line p1-p2
            farthest_point = max(points, key=lambda p: abs(cross(p1, p2, p)))
            
            # Split points into two subsets: left of p1-farthest_point and farthest_point-p2
            left_of_line = [p for p in points if cross(p1, farthest_point, p) > 0]
            right_of_line = [p for p in points if cross(farthest_point, p2, p) > 0]

            return (add_hull(left_of_line, p1, farthest_point) +
                    [tuple(farthest_point)] +
                    add_hull(right_of_line, farthest_point, p2))
        
        # Start with the leftmost and rightmost points
        points = sorted(self.points, key=lambda p: (p[0], p[1]))
        min_point, max_point = points[0], points[-1]
        
        # Split the remaining points into two sets
        left_set = [p for p in points if cross(min_point, max_point, p) > 0]
        right_set = [p for p in points if cross(max_point, min_point, p) > 0]
        
        # Combine the convex hull segments
        return ([tuple(min_point)] +
                add_hull(left_set, min_point, max_point) +
                [tuple(max_point)] +
                add_hull(right_set, max_point, min_point))

    def monotone_chain(self):
        """Find the convex hull using the Monotone Chain algorithm."""
        points = sorted(self.points, key=lambda x: (x[0], x[1]))
        
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for p in points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(tuple(p))

        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(tuple(p))

        return lower[:-1] + upper[:-1]
    
def file_to_tuples(file_path):
    tuples_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip header if present (assuming first line has "X Y")
            if line.strip().startswith("X Y"):
                continue
            # Split the line into two numbers and convert to float
            x, y = map(float, line.split())
            # Append as a tuple
            tuples_list.append((x, y))
    return tuples_list



def plot_convex_hull(points, hull, title):
    # Extract x and y coordinates from points
    x_coords, y_coords = zip(*points)

    # Extract x and y coordinates for hull points (close the hull loop for plotting)
    hull_x, hull_y = zip(*hull + [hull[0]])

    # Plot all points
    plt.scatter(x_coords, y_coords, label="Points", color="blue", s=20)

    # Plot convex hull
    plt.plot(hull_x, hull_y, label="Convex Hull", color="red", linewidth=2)

    # Add labels and legend
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
     file_path = "mesh.dat"
     points = file_to_tuples(file_path)
     print(points)
     cloud = DataCloud(points)
    
     print("Graham Scan:", cloud.graham_scan())
     plot_convex_hull(points, cloud.graham_scan(), "Graham Scan")

     print("Jarvis March:", cloud.jarvis_march())
     plot_convex_hull(points, cloud.jarvis_march(), "Jarvis March")

     print("Quickhull:", cloud.quickhull())
     plot_convex_hull(points, cloud.quickhull(), "Quickhull")

     print("Monotone Chain:", cloud.monotone_chain())
     plot_convex_hull(points, cloud.monotone_chain(), "Monotone Chain")
