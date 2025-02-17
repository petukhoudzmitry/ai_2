import math     # Import math module for mathematical functions (e.g., square root)
import random   # Import random module for generating random numbers

import numpy as np  # Import numpy for random integer generation in specified ranges


def compute_distance(point_a, point_b):
    """
        Computes the Euclidean distance between two points.

        Parameters:
            point_a: Tuple representing the first point (x, y).
            point_b: Tuple representing the second point (x, y).

        Returns:
            The Euclidean distance between point_a and point_b.
        """
    # If either point is None, return infinity (indicating invalid distance)
    if point_a is None or point_b is None:
        return float("inf")

    # Calculate Euclidean distance: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def compute_centroid(cluster):
    """
        Computes the centroid (mean) of a cluster of points.

        Parameters:
            cluster: List of tuples representing points in the cluster.

        Returns:
            The coordinates (x, y) of the centroid of the cluster.
        """
    # Extract the x and y coordinates of each point in the cluster
    x_coordinates = [x[0] for x in cluster]
    y_coordinates = [y[1] for y in cluster]

    # Calculate and return the average of the x and y coordinates
    return sum(x_coordinates) / (len(cluster)), sum(y_coordinates) / (len(cluster))


def generate_initial_points(points, amount, x_range, y_range):
    """
       Generates a set of initial random points within specified ranges.

       Parameters:
           points: A set to hold the generated points.
           amount: The number of points to generate.
           x_range: Tuple representing the range for x coordinates (min, max).
           y_range: Tuple representing the range for y coordinates (min, max).

       Returns:
           The updated set of points with the newly generated points.
       """
    # Keep generating points until the set contains the specified amount of points
    while len(points) < amount:
        points.add((
            np.random.randint(x_range[0], x_range[1] + 1),  # Random x within x_range
            np.random.randint(y_range[0], y_range[1] + 1)   # Random y within y_rang
        ))

    # Return the updated set of points
    return points


def generate_points(points, points_initial_amount, points_total_amount, x_range, y_range, x_interval, y_interval):
    """
        Generates a set of points by expanding initial points with random offsets.

        Parameters:
            points: A set to hold the generated points.
            points_initial_amount: The number of initial points to generate.
            points_total_amount: The total number of points to generate.
            x_range: Tuple representing the range for x coordinates (min, max).
            y_range: Tuple representing the range for y coordinates (min, max).
            x_interval: Tuple representing the range for random x offsets.
            y_interval: Tuple representing the range for random y offsets.

        Returns:
            The updated set of points with the newly generated points.
        """
    # Generate the initial points in the specified range
    generate_initial_points(points, points_initial_amount, x_range, y_range)

    # Generate additional points by applying random offsets to existing points
    while len(points) < points_total_amount:
        random_point = random.choice(list(points))  # Randomly select an existing point

        # Apply random offsets within the given intervals
        x_offset = np.random.randint(x_interval[0], x_interval[1] + 1)
        y_offset = np.random.randint(y_interval[0], y_interval[1] + 1)

        # Calculate new x and y coordinates with the applied offsets
        x = random_point[0] + x_offset
        y = random_point[1] + y_offset

        # Ensure that the new point is within the specified x and y range
        new_point = (
            x_range[0] if x < x_range[0] else (x_range[1] if x > x_range[1] else x),
            y_range[0] if y < y_range[0] else (y_range[1] if y > y_range[1] else y)
        )

        # Add the new point to the set of points
        points.add(new_point)