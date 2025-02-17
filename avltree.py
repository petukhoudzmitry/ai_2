from util import compute_distance

spaces_increment_value = 5

class AVLNode:
    """Represents a node in an AVL Tree with a 2D point (x, y) and properties for height and children nodes."""
    def __init__(self, x, y, points = None):
        self.point = (x, y) # Point represented as a tuple
        self.height = 1     # Height of the node in the tree for balancing
        self.left = None    # Left child
        self.right = None   # Right child
        self.points = points if points is not None else [] # Cluster points

    def __repr__(self):
        return str(f"{self.point, self.points}")

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return hash(self.point)

    def copy(self):
        return AVLNode(*self.point, self.points)


def get_height(node):
    """Returns the height of a node, or 0 if the node is None."""
    return node.height if node is not None else 0


def find_closest(root, node, best = None):
    """Finds the closest node to a given node in the AVL tree."""
    if root is None or node is None:
        return best

    if root != node:
        distance = compute_distance(root.point, node.point)
        # Update best if current node is closer and not the same as the input node
        if best is None or distance < compute_distance(node.point, best.point):
            best = root

    if node.point < root.point:
        next_node = root.left
        last_node = root.right
    else:
        next_node = root.right
        last_node = root.left

    # Recurse to find a closer point
    temp = find_closest(next_node, node, best)
    best = temp if temp is not None else best

    # Check if exploring the other subtree might yield a closer node
    if abs(node.point[0] - root.point[0]) < compute_distance(node.point, best.point):
        temp = find_closest(last_node, node, best)
        best = temp if temp is not None else best

    return best


def get_balance(node):
    """Calculates the balance factor of a node to help maintain AVL tree balance."""
    return get_height(node.left) - get_height(node.right)


def update_height(node):
    """Updates the height of a node based on its children's heights."""
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def count_elements(node):
    """Counts the total number of nodes in the tree."""
    if not node:
        return 0
    return 1 + count_elements(node.left) + count_elements(node.right)


def rotate_right(node):
    """Performs a right rotation on the given node."""
    l = node.left
    lr = l.right
    l.right = node
    node.left = lr
    update_height(node)
    update_height(l)

    return l


def rotate_left(node):
    """Performs a left rotation on the given node."""
    r = node.right
    rl = r.left
    r.left = node
    node.right = rl
    update_height(node)
    update_height(r)

    return r


def insert(node, x, y, points = None):
    """Inserts a point (x, y) as a new node into the AVL tree, maintaining balance."""
    if node is None:
        return AVLNode(x, y, points)

    # Insert based on the point's comparison with the current node's point
    if (x, y) < node.point:
        node.left = insert(node.left, x, y, points)
    elif (x, y) > node.point:
        node.right = insert(node.right, x, y, points)

    # Update height and balance the tree if necessary
    update_height(node)

    balance = get_balance(node)

    # Perform rotations if the tree is unbalanced
    if balance > 1:
        if get_balance(node.left) < 0:
            node.left = rotate_left(node.left)
        return rotate_right(node)

    if balance < -1:
        if get_balance(node.right) > 0:
            node.right = rotate_right(node.right)
        return rotate_left(node)

    return node


def min_value_node(node):
    """Finds the node with the minimum point value in the AVL tree."""
    current = node

    while current.left is not None:
        current = current.left

    return current


def remove_node(root, node):
    """Removes a given node from the AVL tree and rebalances if necessary."""
    if root is None or node is None:
        return root

    # Recursive node removal
    if node.point < root.point:
        root.left = remove_node(root.left, node)
    elif node.point > root.point:
        root.right = remove_node(root.right, node)
    else:
        # Node with one or no child
        if root.left is None or root.right is None:
            temp = root.left if root.left is not None else root.right
            del root
            root = temp
        else:
            # Node with two children
            temp = min_value_node(root.right)
            root.point = temp.point
            root.points = temp.points
            root.right = remove_node(root.right, temp)

    if root is None:
        return root

    # Update height and balance tree after removal
    update_height(root)
    balance = get_balance(root)

    # Rebalance if necessary
    if balance > 1:
        if get_balance(root.left) < 0:
            root.left = rotate_left(root.left)
        return rotate_right(root)
    elif balance < -1:
        if get_balance(root.right) > 0:
            root.right = rotate_right(root.right)
        return rotate_left(root)

    return root


def tree_to_list(root, tree_list = None):
    """Converts the AVL tree to a sorted list of nodes using an in-order traversal."""
    if root is None:
        return tree_list

    if tree_list is None:
        tree_list = []

    tree_to_list(root.left, tree_list)
    tree_list.append(root)
    tree_to_list(root.right, tree_list)

    return tree_list