from abc import ABC, abstractmethod

class Node:
    def __init__(self, key=None, value=None, color="red", left=None, right=None, parent=None):
        self.key = key          # The key to be used for comparison in the tree
        self.value = value      # The value associated with the key
        self.color = color      # Used for red-black trees
        self.parent = parent    # Reference to the parent node
        self.left = left        # Reference to the left child
        self.right = right      # Reference to the right child

    def __repr__(self):
        # Custom string representation for the node
        return f"Node(User={self.key}, Seat={self.value}, color={self.color})"

class TreeFactory(ABC):
    """To create tree objects and perform tree operations"""

    def __init__(self):
        self.tree_network = []  # The structure holding nodes
        self.tree_network_size = len(self.tree_network)

    @abstractmethod
    def insert(self, key, value):
        pass

    def rebalance(self, new_node):
        pass

    def search(self, key):
        """Search for a node with the given key in the Red-Black Tree."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        """Helper function that recursively searches for the node with the given key."""
        # print(f"Seats: {self.tree_network}")
        # print(f"Node {node} with key {node.key}")
        if node is None or node.key is None:
            return f"User has no prior booking"  # Key not found
        
        if key == node.key:
            return node  # Key found, return the node

        # Recursively search in the left or right subtree
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def delete(self, key):
        """Delete a node with the specified key from the Red-Black Tree."""
        node_to_delete = self.search(key)

        # If the node doesn't exist or the tree is empty, return.
        if not node_to_delete or node_to_delete == self.nil:
            print("Node not found or tree is empty.")
            return
        
            # Remove the node from the tree_network list if it exists
        if node_to_delete in self.tree_network:
            self.tree_network.remove(node_to_delete)

        y = node_to_delete
        y_original_color = y.color
        if node_to_delete.left == self.nil:
            x = node_to_delete.right
            self._transplant(node_to_delete, node_to_delete.right)
        elif node_to_delete.right == self.nil:
            x = node_to_delete.left
            self._transplant(node_to_delete, node_to_delete.left)
        else:
            # Find the minimum node in the right subtree
            y = self._minimum(node_to_delete.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node_to_delete:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y
            self._transplant(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y
            y.color = node_to_delete.color

        # Fix violations if a black node was deleted
        if y_original_color == "black":
            self._delete_fix(x)

        # Confirm removal from `tree_network`
        if node_to_delete in self.tree_network:
            self.tree_network.remove(node_to_delete)


    def _transplant(self, u, v):
        """Replace the subtree rooted at u with the subtree rooted at v."""
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """Find the minimum node in a subtree rooted at node."""
        while node.left != self.nil:
            node = node.left
        return node

    def _delete_fix(self, x):
        """Fix the Red-Black Tree properties after deletion."""
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.right.color == "black":
                        sibling.left.color = "black"
                        sibling.color = "red"
                        self.right_rotate(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    sibling.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == "red":
                    sibling.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    sibling = x.parent.left
                if sibling.left.color == "black" and sibling.right.color == "black":
                    sibling.color = "red"
                    x = x.parent
                else:
                    if sibling.left.color == "black":
                        sibling.right.color = "black"
                        sibling.color = "red"
                        self.left_rotate(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = "black"
                    sibling.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "black"


class RedBlackTree(TreeFactory):
    """A Red-Black Tree implementation"""

    def __init__(self):
        super().__init__()
        self.nil = Node(color="black")  # Sentinel NIL node
        self.root = self.nil  # Initially, the tree root is the NIL node

    def insert(self, key, value):
        """Insert a node with the specified key and value into the Red-Black Tree"""

        # Create a new red node with both key and value
        new_node = Node(key=key, value=value, color="red", left=self.nil, right=self.nil)
        
        # Start insertion at the root
        current_node = self.root  # Current node starts at root node for traversal of tree
        parent_node = self.nil  # Initially, 'parent_node' is set to nil, as we haven't started traversing.

        # Traverse the tree to find the correct position for the new node.
        while current_node != self.nil:
            parent_node = current_node  # Keep track of 'current_node' as 'parent_node' before moving.

            # '.key' attribute is the node's key, thus
            #   new_node.key is the key of the new node that you're trying to insert
            #   current_node.key is the key of the current node.
            if new_node.key < current_node.key:
                current_node = current_node.left  # Update current node to its left child
            else:
                current_node = current_node.right  # Update current node to its right child

        # After the loop, parent_node is the parent of the new node
        new_node.parent = parent_node

        # If parent_node is NIL, it means the tree is empty and new_node will be the root
        if parent_node == self.nil:
            self.root = new_node
        elif new_node.key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        # Append the new node to tree_network
        self.tree_network.append(new_node)  # Add the node to the network
        # Fix the Red-Black Tree properties after insertion
        self.rebalance(new_node)

    def rebalance(self, new_node):
        # While the parent of the node is red, violations exist
        while new_node.parent.color == "red":
            # Case when the parent is the left child of the grandparent
            if new_node.parent == new_node.parent.parent.left:
                # y is the uncle of the new_node
                uncle = new_node.parent.parent.right
                
                # Case 1: If the uncle is red, we only need to recolor
                if uncle.color == "red":
                    new_node.parent.color = "black"      # Recolor parent to black
                    uncle.color = "black"                # Recolor uncle to black
                    new_node.parent.parent.color = "red" # Recolor grandparent to red
                    new_node = new_node.parent.parent   # Move up the tree to fix violations higher up
                else:
                    # Case 2: If new_node is a right child, perform a left rotation
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)  # Rotate new_node to the left to prepare for case 3
                    
                    # Case 3: Recolor and right rotate the grandparent
                    new_node.parent.color = "black"        # Recolor parent to black
                    new_node.parent.parent.color = "red"   # Recolor grandparent to red
                    self.right_rotate(new_node.parent.parent) # Rotate grandparent to the right to balance the tree

            # Case when the parent is the right child of the grandparent
            else:
                # y is the uncle of the new_node (left child of the grandparent)
                uncle = new_node.parent.parent.left
                
                # Case 1: If the uncle is red, recolor
                if uncle.color == "red":
                    new_node.parent.color = "black"       # Recolor parent to black
                    uncle.color = "black"                # Recolor uncle to black
                    new_node.parent.parent.color = "red"  # Recolor grandparent to red
                    new_node = new_node.parent.parent    # Move up the tree to fix violations higher up
                else:
                    # Case 2: If new_node is a left child, perform a right rotation
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)   # Rotate new_node to the right to prepare for case 3
                    
                    # Case 3: Recolor and left rotate the grandparent
                    new_node.parent.color = "black"         # Recolor parent to black
                    new_node.parent.parent.color = "red"    # Recolor grandparent to red
                    self.left_rotate(new_node.parent.parent) # Rotate grandparent to the left to balance the tree
        
        # Ensure the root is always black
        self.root.color = "black"
    
    def left_rotate(self, current_node):
        """Perform a left rotation on the given node in a Red-Black Tree."""
        parent_node = current_node.right
        current_node.right = parent_node.left
        if parent_node.left != self.nil:
            parent_node.left.parent = current_node
        
        parent_node.parent = current_node.parent
        if current_node.parent == self.nil:
            self.root = parent_node
        elif current_node == current_node.parent.left:
            current_node.parent.left = parent_node
        else:
            current_node.parent.right = parent_node
        
        parent_node.left = current_node
        current_node.parent = parent_node

    def right_rotate(self, parent_node):
        """Perform a right rotation on the given node in a Red-Black Tree."""
        current_node = parent_node.left
        parent_node.left = current_node.right
        if current_node.right != self.nil:
            current_node.right.parent = parent_node
        
        current_node.parent = parent_node.parent
        if parent_node.parent == self.nil:
            self.root = current_node
        elif parent_node == parent_node.parent.right:
            parent_node.parent.right = current_node
        else:
            parent_node.parent.left = current_node
        
        current_node.right = parent_node
        parent_node.parent = current_node