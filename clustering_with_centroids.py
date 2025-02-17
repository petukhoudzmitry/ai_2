from avltree import *   # Import all functions from AVL Tree module
from util import *      # Import utility functions (e.g., compute_distance, compute_centroid)


def clustering(root, k):
    sample_size = k >> 1
    while count_elements(root) > k:
        nodes = tree_to_list(root)
        nodes = random.sample(nodes, sample_size)
        nodes.sort(key=lambda x: compute_distance(x.point, find_closest(root, x).point))

        node_a = nodes[0]
        node_b = find_closest(root, node_a)

        cluster_points = node_a.points + node_b.points
        centroid = compute_centroid(cluster_points)

        root = remove_node(root, node_a)
        root = remove_node(root, node_b)
        root = insert(root, *centroid, cluster_points)


    nodes = tree_to_list(root)
    clusters = {node.point: node.points for node in nodes}

    return clusters


def clustering_with_centroids(data, k):
    data = list(data)
    clusters = []

    chunk_size = len(data) // k

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        root = None
        for point in chunk:
            root = insert(root, *point, [point])
        clusters.append(clustering(root, k))

    root = None
    for cluster in clusters:
        for centroid, points in cluster.items():
            root = insert(root, *centroid, points)

    clusters = {node: [] for node in clustering(root, k)}

    root = None
    for cluster in clusters.keys():
        root = insert(root, *cluster)

    for point in data:
        closest = find_closest(root, AVLNode(*point))
        clusters[closest.point].append(point)

    for cluster in list(clusters.keys()):
        if len(clusters[cluster]) == 0:
            del clusters[cluster]

    return clusters