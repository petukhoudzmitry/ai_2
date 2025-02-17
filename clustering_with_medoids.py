import random   # Import random module for selecting random medoids

from avltree import insert, AVLNode, find_closest, tree_to_list
from clustering_with_centroids import clustering_with_centroids
from util import compute_distance   # Import compute_distance function to calculate Euclidean distance


def assign_points_to_medoids(points, medoids):
    """
        Assign each point to the closest medoid.

        Parameters:
        - points: List of points to be assigned to clusters.
        - medoids: List of current medoids (cluster centers).

        Returns:
        - clusters: A dictionary mapping each medoid to its corresponding points.
        """
    clusters = {medoid: [] for medoid in medoids}   # Initialize clusters as an empty list for each medoid

    root = None
    for medoid in medoids:
        root = insert(root, *medoid)

    for point in points:
        # Find the closest medoid by computing the distance between the point and each medoid
        if point not in medoids:
            closest_medoid = find_closest(root, AVLNode(*point)).point
            clusters[closest_medoid].append(point)  # Assign the point to the closest medoid's cluster
    return clusters


def calculate_total_cost(clusters):
    """
        Calculate the total cost (sum of distances from points to their assigned medoids).

        Parameters:
        - clusters: A dictionary of clusters where keys are medoids and values are lists of points.
        - medoids: A list of current medoids.

        Returns:
        - total_cost: The total sum of distances of points to their assigned medoids.
        """
    total_cost = 0
    # Iterate through each medoid and its corresponding points
    for medoid, points in clusters.items():
        # Calculate the sum of distances from each point to the medoid
        total_cost += sum(compute_distance(point, medoid) for point in points)
    return total_cost


def update_medoids(clusters):
    """
        Update medoids by finding the medoid that minimizes the total distance to all points in the cluster.

        Parameters:
        - clusters: A dictionary of clusters where keys are medoids and values are lists of points.

        Returns:
        - new_medoids: A list of updated medoids.
        """
    new_medoids = []
    for medoid, points in clusters.items():
        # For each cluster, find the point that minimizes the sum of distances to other points in the cluster
        # sorted_points = sorted(points, key=lambda x: sum(compute_distance(x, cluster_point) for cluster_point in points))
        best_medoid = find_real_center(points) if len(points) > 0 else medoid
        new_medoids.append(best_medoid) # Update the medoid with the best point

    return new_medoids


def find_real_center(points):
    return min(points, key=lambda x: sum(compute_distance(x, point) for point in points))


def clustering(points, k, max_iterations, medoids = None):
    medoids = random.sample(points, k) if medoids is None else random.sample(medoids, k)

    for _ in range(max_iterations):
        clusters = assign_points_to_medoids(points, medoids)
        old_cost = calculate_total_cost(clusters)

        new_medoids = update_medoids(clusters)
        new_clusters = assign_points_to_medoids(points, new_medoids)
        new_cost = calculate_total_cost(new_clusters)

        if new_cost >= old_cost:
            break  # Stop if no improvement in cost
        medoids = new_medoids

    return medoids


def clustering_with_medoids(points, k, max_iterations=100):
    """Perform the k-medoids clustering algorithm."""

    # points = sorted(points)

    root = None
    for point in points:
        root = insert(root, *point)

    points = [node.point for node in tree_to_list(root)]

    chunk_size = len(points) // k

    medoids = []

    for i in range(0, len(points), chunk_size):
        medoids.extend(clustering(points[i: i + chunk_size], k, max_iterations))

    best_medoids = [centroid for centroid in clustering_with_centroids(medoids, k).keys()]

    root = None
    for medoid in medoids:
        root = insert(root, *medoid)

    clusters = {find_closest(root, AVLNode(*medoid)).point: [] for medoid in best_medoids}

    root = None
    for medoid in clusters.keys():
        root = insert(root, *medoid)

    for point in points:
        closest_medoid = find_closest(root, AVLNode(*point)).point
        clusters[closest_medoid].append(point)

    return clusters