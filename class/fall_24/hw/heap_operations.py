from abc import ABC, abstractmethod

class HeapFactory(ABC):
    """To create heap objects and perform heap operations. Each function below will contain either one or both parameters. 
    
    Parameters:
    -----------
    i: `int`
        The index of a node
    
    key: `int`
        The value of a node

    """

    def __init__(self):
        self.network = []
        self.network_size = len(self.network)

    def get_root_node(self, i: int):
        """Get root node of heap"""

        return i // 2

    def get_left_node(self, i: int):
        """Get left child node of heap"""

        return 2 * i

    def get_right_node(self, i: int):
        """Get right child node of heap"""

        return 2 * i + 1

    # @abstractmethod
    def insert(self, key: int):
        """Insert a new key (priority, time_reserved, user_id) into the min-heap."""
        pass

    def decrease_heap_key(self, i: int, key: int):
        """Decrease the key value at index i to the new key, maintaining the min-heap property."""
        pass
         
    # @abstractmethod
    def extract_min(self):
        pass

    def delete_node(self, key: int):
        """Delete any key in min-heap"""

        idx_of_node, _ = self.search(key)
        if idx_of_node == -1:
            print(f"Node {key} not found in waiting list")
            return

        last_node = self.network[-1] # Get last node to swap node to delete with it
        self.network[idx_of_node] = last_node # Swap by placing last node in spot of node to delete
        self.network.pop() # Remove node to delete
        self.min_heapify(idx_of_node) # Heapify on original idx on node we deleted
        print(f"User {key} is removed from waiting list")

    def build_heap(self):
        """Take an unordered list of n elements. 
        O(log n): Call min_heapify() which worse case traverses the height of the heap log_2 (n) to restore heap property
        O(n): For every element, we call min_heapify()
        """

        pass 

    def search(self, key):
        """Search for a key (user) in the heap."""
        
        for i in range(self.network_size):
            _, _, user = self.network[i]
            if user == key:
                return i, True
        return -1, False

    def min_heapify(self, i: int):
        """To maintain the min-heap property of the parent node being smaller than the child node. If the parent node is larger than either of its children, the function "sinks" the parent down the tree, swapping it with the smallest child, until the heap property is restored.

        O(log n): Call min_heapify() which worse case traverses the height of the heap log_2 (n) to restore heap property
        O(i=1): For element i, call min_heapify()
        """
    
        l = self.get_left_node(i)
        r = self.get_right_node(i)

        if l < len(self.network) and self.network[l] < self.network[i]:
            smallest = l
        else:
            smallest = i
        if r < len(self.network) and self.network[r] < self.network[smallest]:
            smallest = r
            
        if smallest != i:
            # Swap elements
            self.network[i], self.network[smallest] = self.network[smallest], self.network[i]
            
            # Recursively heapify the affected sub-tree
            self.min_heapify(smallest)

class SeatHeap(HeapFactory):
    """Inherit functions from the HeapFactory class. Use this class to store available seats and to perform other operations that are in functions below."""

    def build_heap(self, available_seats: list):
        """Take an unordered list of n elements to place into a heap data structure."""

        self.network = available_seats
        self.network_size = len(self.network)

        for node in range((self.network_size // 2) - 1, -1, -1):
            self.min_heapify(node)
        
        return self.network
    
    def extract_min(self):
        """Extract root node as it's the min node."""

        if self.network_size < 1:
            return "Heap underflow"
        
        min_node = self.network[0] # Min node is root node, so 1
        self.network[0] = self.network[-1] # Replace root node with last node to maintain the complete binary tree structure, so [5, 2, 3, 4, 5]
        self.network.pop() # Remove last element, so [5, 2, 3, 4]
        self.network_size = len(self.network) # Update size, so 4
        self.min_heapify(0)  # self.network = [2, 3, 4, 5]

        return min_node
    
    def insert(self, seat_id: int):
        """Insert a new seat_id into the min-heap without priority."""

        # Increase network size for new insertion
        self.network_size += 1
        # Append seat_id as a placeholder
        self.network.append(seat_id)
        i = self.network_size - 1
        # Bubble up to maintain min-heap property
        while i > 0 and self.network[self.get_root_node(i)] > self.network[i]:
            # Swap with the parent node
            parent = self.get_root_node(i)
            self.network[i], self.network[parent] = self.network[parent], self.network[i]
            i = parent
        
class WaitlistHeap(HeapFactory):
    """Inherit functions from the HeapFactory class. Use this class to store users in waitlist and to perform other operations that are in functions below.."""

    def build_heap(self, waitlist_seats: list):
        """Take an unordered list of n elements to place into a heap data structure."""

        self.network = waitlist_seats
        self.network_size = len(self.network)

        for node in range((self.network_size // 2) - 1, -1, -1):
            self.min_heapify(node)
        
        return self.network
    
    def insert(self, key: int):
        """Insert a new key (priority, user_id) into the min-heap."""

        # Increase network size for new insertion and append a placeholder
        # self.network_size += 1
        
        self.network.append((float('inf'), None))  # Extend with a tuple placeholder
        self.network_size = len(self.network)
        # print(self.network_size)
        self.decrease_heap_key(self.network_size - 1, key)  # Use network_size - 1 for correct index

    def decrease_heap_key(self, i: int, key: int):
        """Decrease the key value at index i to the new key, maintaining the min-heap property."""
        
        # print(f"{key} vs Network size - 1: {i} vs Network size: {self.network_size}")
        # print(f"{key} vs {self.network[i]}")
        if key > self.network[i]:
            raise ValueError("New key is larger than current key")
        
        # Set the key at the specified index
        self.network[i] = key

        # Bubble up to maintain the min-heap property
        while i > 0 and self.network[(i - 1) // 2] > self.network[i]:
            # Swap with the parent node
            self.network[i], self.network[(i - 1) // 2] = self.network[(i - 1) // 2], self.network[i]
            i = (i - 1) // 2