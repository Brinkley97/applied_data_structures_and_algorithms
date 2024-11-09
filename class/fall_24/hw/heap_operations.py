from abc import ABC, abstractmethod

class HeapFactory(ABC):
    """To create heap objects and perform heap operations"""

    def __init__(self):
        self.network = []
        self.network_size = len(self.network)

    # def get_root_node(i):
    #     return 
    def get_left_node(self, i):
        return 2 * i

    def get_right_node(self, i):
        return 2 * i + 1

    # @abstractmethod
    def insert(self):
        pass

    # @abstractmethod
    def extract_min(self):
        pass

    # @abstractmethod
    def build_heap(self):
        """Take an unordered list of n elements. 
        O(log n): Call min_heapify() which worse case traverses the height of the heap log_2 (n) to restore heap property
        O(n): For every element, we call min_heapify()
        """
        pass 

    # @abstractmethod
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
    """Store available seats"""

    def build_heap(self, available_seats: list):
        self.network = available_seats
        self.network_size = len(self.network)

        for node in range((self.network_size // 2) - 1, -1, -1):
            self.min_heapify(node)
        
        return self.network
    
    def extract_min(self):
        """
        Example with self.network = [1, 2, 3, 4, 5]
            self.network_size = 5
        """
        if self.network_size < 1:
            return "Heap underflow"
        
        min_node = self.network[0] # Min node is root node, so 1
        self.network[0] = self.network[-1] # Replace root node with last node to maintain the complete binary tree structure, so [5, 2, 3, 4, 5]
        self.network.pop() # Remove last element, so [5, 2, 3, 4]
        self.network_size = len(self.network) # Update size, so 4
        self.min_heapify(0)  # self.network = [2, 3, 4, 5]

        return min_node

class WaitlistHeap(HeapFactory):
    """Store users in waitlist"""

    def build_heap(self):
        return super().build_heap()