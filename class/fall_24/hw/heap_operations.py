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
        pass 

    # @abstractmethod
    def min_heapify(self, i: int):
        """To maintain the min-heap property of the parent node being smaller than the child node. If the parent node is larger than either of its children, the function "sinks" the parent down the tree, swapping it with the smallest child, until the heap property is restored.
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

class WaitlistHeap(HeapFactory):
    """Store users in waitlist"""