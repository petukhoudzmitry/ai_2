from matplotlib import pyplot as plt    # Import the pyplot module from matplotlib for plotting


def plot_points(arr, figsize = (50, 50), title='Initial points'):
    """
        Plot the initial set of points.

        Parameters:
        - arr: List of points to be plotted.
        - figsize: Size of the plot (default is (50, 50)).
        - title: Title of the plot (default is 'Initial points').
        """
    plt.figure(figsize=figsize) # Create a figure with the specified size
    # Scatter plot of points, using the x and y coordinates of the points in 'arr'
    plt.scatter([i[0] for i in arr], [i[1] for i in arr], c='blue')
    plt.title(title)    # Set the title of the plot
    plt.show()  # Display the plot


def plot_clusters(clusters, points, labels, figsize = (50, 50), title='Clusters'):
    """
        Plot the clusters, with points colored according to their cluster label and medoids marked.

        Parameters:
        - clusters: The cluster centers (medoids) to be plotted.
        - points: List of points to be plotted.
        - labels: List of labels corresponding to the points, indicating their cluster assignment.
        - figsize: Size of the plot (default is (50, 50)).
        - title: Title of the plot (default is 'Clusters').
        """
    plt.figure(figsize=figsize) # Create a figure with the specified size
    # Scatter plot of the points, with color representing their assigned cluster label
    plt.scatter([i[0] for i in points], [i[1] for i in points], c=labels, cmap="tab20b")
    # Scatter plot of the medoids (cluster centers) with a black color and larger size
    plt.scatter([i[0] for i in clusters], [i[1] for i in clusters], s=100, c="black")
    plt.title(title)    # Set the title of the plot
    plt.show()  # Display the plot