from abc import ABC, abstractmethod

class Node:
    def __init__(self, key=None, color="red", left=None, right=None, parent=None):
        self.key = key          # The value stored in the node (e.g., 5, 10, etc.)
        self.color = color      # Used for red-black trees
        self.parent = parent    # Reference to the parent node
        self.left = left        # Reference to the left child
        self.right = right      # Reference to the right child

class TreeFactory(ABC):
    """To create tree objects and perform tree operations"""

    def __init__(self):
        self.tree_network = []  # The structure holding nodes
        self.tree_network_size = len(self.tree_network)

    @abstractmethod
    def insert(self, key):
        pass

class RedBlackTree(TreeFactory):
    """A Red-Black Tree implementation"""

    def __init__(self):
        super().__init__()
        self.nil = Node(color="black")  # Sentinel NIL node
        self.root = self.nil  # Initially, the tree root is the NIL node

    def insert(self, key):
        """Insert a node with the specified key into the Red-Black Tree"""

        # Create a new red node
        new_node = Node(key=key, color="red", left=self.nil, right=self.nil)
        
        # Start insertion at the root
        current_node = self.root # Current node starts at root node for traversal of tree
        parent_node = self.nil  # Initially, 'parent_node' is set to nil, as we haven't started traversing.

        # Traverse the tree to find the correct position for the new node.
        while current_node != self.nil:
            parent_node = current_node  # Keep track of 'current_node' as 'parent_node' before moving.

            # '.key' attribute is the node's value, thus
            #   new_node.key is value of the new node that you're trying to insert
            #   current_node.key is value of the current node.
            if new_node.key < current_node.key:
                current_node = current_node.left # Update current node to it's left child
            else:
                current_node = current_node.right # Update current node to it's right child

        # After the loop, parent_node is the parent of the new node
        new_node.parent = parent_node

        # If parent_node is NIL, it means the tree is empty and new_node will be the root
        if parent_node == self.nil:
            self.root = new_node
        elif new_node.key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        # Fix the Red-Black Tree properties after insertion
        self.rb_insert_fixup(new_node)

    def rb_insert_fixup(self, new_node):
        # While the parent of the node is red, violations exist
        while new_node.parent.color == "red":
            # Case when the parent is the left child of the grandparent
            if new_node.parent == new_node.parent.parent.left:
                # y is the uncle of the new_node
                uncle = new_node.parent.parent.right
                
                # Case 1: If the uncle is red, we only need to recolor
                if uncle.color == "red":
                    new_node.parent.color = "black"      # Recolor parent to black
                    uncle.color = "black"               # Recolor uncle to black
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



