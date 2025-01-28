from datacloud import *
from generate_point_cloud import *
import time
import matplotlib.pyplot as plt

def time_function(f):
    start_time = time.time()
    f
    end_time = time.time()
    return end_time - start_time




n_lst = [10, 50, 100, 200, 400, 800, 1000]

def plot_time(dist, name):
    graham_scan_time = []
    jarvis_march_time = []
    quickhull_time = []
    monotone_chain_time = []

    for n in n_lst:
        points = generate_point_cloud(n, distribution=dist)
        cloud = DataCloud(points)
        graham_scan_time.append(time_function(cloud.graham_scan()))
        jarvis_march_time.append(time_function(cloud.jarvis_march()))
        quickhull_time.append(time_function(cloud.quickhull()))
        monotone_chain_time.append(time_function(cloud.monotone_chain()))


    plt.plot(n_lst, graham_scan_time, label="Graham Scan")
    plt.plot(n_lst, jarvis_march_time, label="Jarvis March")
    plt.plot(n_lst, quickhull_time, label="Quickhull")
    plt.plot(n_lst, monotone_chain_time, label="Monotone Chain")
    plt.legend()

    plt.savefig(f"{name}.png", format="png", dpi=300)
    plt.show()

    plt.clf()

# uniform distribution in [0, 1]
plot_time(dist=random.uniform(0, 1), name="time_complexity_1")

# uniform distribution in [-5, 5]
plot_time(dist=random.uniform(-5, 5), name="time_complexity_2")

# Gaussian distribution centered at the origin with variance 1
plot_time(dist=random.gauss(mu=0, sigma=1), name="time_complexity_3")

def plot_hist(dist):
    graham_scan_time = []
    jarvis_march_time = []
    quickhull_time = []
    monotone_chain_time = []

    for i in range(100):
        points = generate_point_cloud(50, distribution=dist)
        cloud = DataCloud(points)
        graham_scan_time.append(time_function(cloud.graham_scan()))
        jarvis_march_time.append(time_function(cloud.jarvis_march()))
        quickhull_time.append(time_function(cloud.quickhull()))
        monotone_chain_time.append(time_function(cloud.monotone_chain()))

    plt.hist(graham_scan_time)
    plt.savefig("graham_scan.png", format="png")
    plt.clf()

    plt.hist(jarvis_march_time)
    plt.savefig("jarvis_march.png", format="png")
    plt.clf()

    plt.hist(quickhull_time)
    plt.savefig("quickhull.png", format="png")
    plt.clf()

    plt.hist(monotone_chain_time)
    plt.savefig("monotone_chain.png", format="png")
    plt.clf()

plot_hist(dist=random.uniform(-5, 5))

