import matplotlib.pyplot as plt

def plot_node(x, y, value, ax):
    """Plot a single node."""
    ax.text(x, y, str(value), ha='center', va='center', 
            bbox=dict(facecolor='skyblue', boxstyle='circle'))

def plot_edge(x1, y1, x2, y2, ax):
    """Plot an edge between two nodes."""
    ax.plot([x1, x2], [y1, y2], 'k-')

def visualize_binary_heap(arr):
    n = len(arr)
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Define coordinates for the nodes
    coords = {}

    # Level and x-offset configuration for neat positioning
    levels = int(n.bit_length())  # Number of levels in the binary tree
    x_offset = 2 ** (levels + 1)  # Horizontal distance between nodes
    
    # Recursively place the nodes
    def place_node(i, x, y, dx):
        if i < n:
            # Plot current node
            plot_node(x, y, arr[i], ax)
            coords[i] = (x, y)
            
            # Place left child
            if 2 * i + 1 < n:
                plot_edge(x, y, x - dx, y - 3, ax)  # Adjusted vertical distance
                place_node(2 * i + 1, x - dx, y - 3, dx / 2)  # Adjusted vertical distance
            
            # Place right child
            if 2 * i + 2 < n:
                plot_edge(x, y, x + dx, y - 3, ax)  # Adjusted vertical distance
                place_node(2 * i + 2, x + dx, y - 3, dx / 2)  # Adjusted vertical distance
    
    # Initial call to place the root
    place_node(0, 0, 0, x_offset / 2)

    # Clean up plot
    ax.set_axis_off()
    ax.set_xlim(-x_offset, x_offset)
    ax.set_ylim(-levels * 3 - 1, 1)  # Adjusted ylim for more vertical space
    plt.show()


def visualize_red_black_tree(tree):
    """
    Visualize the Red-Black Tree using matplotlib.

    Parameters:
    -----------
    tree : `RedBlackTree`
        The root of the Red-Black Tree structure to visualize.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    levels = tree.height() + 1  # Number of levels, based on tree height
    x_offset = 2 ** (levels + 1)  # Horizontal distance between nodes

    def traverse_and_plot(node, x, y, dx):
        if node and node != tree.nil:  # Ensure we don’t plot nil nodes
            # Plot the current node
            plot_node(x, y, node.key, node.color, ax)

            # Plot left child
            if node.left and node.left != tree.nil:
                plot_edge(x, y, x - dx, y - 3, ax)
                traverse_and_plot(node.left, x - dx, y - 3, dx / 2)
            
            # Plot right child
            if node.right and node.right != tree.nil:
                plot_edge(x, y, x + dx, y - 3, ax)
                traverse_and_plot(node.right, x + dx, y - 3, dx / 2)
    
    # Initial call to plot from the root
    traverse_and_plot(tree.root, 0, 0, x_offset / 2)

    # Adjust plot limits
    ax.set_xlim(-x_offset, x_offset)
    ax.set_ylim(-levels * 3 - 1, 1)  # Adjust for enough vertical space
    plt.show()