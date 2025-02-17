import time # Import time module for measuring execution time
from math import log10

from clustering_with_centroids import clustering_with_centroids  # Import centroid-based clustering algorithm
from clustering_with_medoids import clustering_with_medoids  # Import k-medoids clustering algorithm
from plotter import plot_points, plot_clusters  # Import functions for visualizing points and clusters
from util import generate_points, compute_distance  # Import function to generate random points


def main():
    # Configuration for the clustering task
    k = 20  # Number of clusters
    random_points = 20_000  # Total number of points to generate
    fig_size_value = int(5 * log10(random_points))
    fig_size = (fig_size_value, fig_size_value) # Size of the plot for visualizations
    initial_points = 20 # Number of initial points to generate
    min_range, max_range = -5000, 5000  # Range for the x and y coordinates
    min_interval, max_interval = -100, 100  # Interval for random offsets applied to points
    x_range = (min_range, max_range)    # x-coordinate range
    y_range = (min_range, max_range)    # y-coordinate range
    x_interval = (min_interval, max_interval)   # x-coordinate offset range
    y_interval = (min_interval, max_interval)   # y-coordinate offset range
    max_distance_allowed = 500

    points = set()  # Initialize an empty set to store the generated points

    # Generate points in the given ranges and with specified intervals
    generate_points(points, initial_points, random_points + initial_points, x_range, y_range, x_interval, y_interval)

    print(f"Input data: points = {len(points)}, clusters = {k}")

    # Plot the generated points
    plot_points(points, fig_size)

    # print("Provide k:")
    # k = int(input())


    # Measure the time taken for clustering with centroids
    start_time = int(time.time() * 1000)
    solution_a = clustering_with_centroids(points, k)   # Perform clustering with centroids
    print(f"Clustering with centroids: {(int(time.time() * 1000) - start_time) / 1000} s")  # Print time taken

    flag = True
    for cluster, cluster_points in solution_a.items():
        flag = False if sum([compute_distance(cluster, point) for point in cluster_points]) / len(cluster_points) > max_distance_allowed else True
        if not flag:
            break

    print("Clustering with centroids: success" if flag else "Clustering with centroids: fail")

    # Measure the time taken for clustering with medoids
    start_time = int(time.time() * 1000)
    solution_b = clustering_with_medoids(points, k)   # Perform clustering with medoids
    print(f"Clustering with medoids: {(int(time.time() * 1000) - start_time) / 1000} s")    # Print time taken

    flag = True
    for cluster, cluster_points in solution_b.items():
        flag = False if sum([compute_distance(cluster, point) for point in cluster_points]) / len(cluster_points) > max_distance_allowed else True
        if not flag:
            break

    print("Clustering with medoids: success" if flag else "Clustering with medoids: fail")

    # Plot the results of clustering with centroids
    labels_a = []
    for point in points:
        for idx, (cluster, cluster_points) in enumerate(solution_a.items()):
            if point in cluster_points:
                labels_a.append(idx)


    plot_clusters(solution_a.keys(), points, labels_a, fig_size)


    # Plot the results of clustering with medoids
    labels_b = []
    for point in points:
        for idx, (cluster, cluster_points) in enumerate(solution_b.items()):
            if point in cluster_points:
                labels_b.append(idx)

    plot_clusters(solution_b.keys(), points, labels_b, fig_size)



if __name__ == '__main__':
    main()  # Run the main function if this script is executed directly