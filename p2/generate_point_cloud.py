import random

def generate_point_cloud(n, distribution):
    point_cloud = []
    for i in range(n):
        point_cloud.append((distribution, distribution))
    return point_cloud

# print(generate_point_cloud(100))
