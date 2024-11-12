import heap_operations, tree_operations, visualizations

class SeatBooking():
    def __init__(self):
        self.unassigned_seats = []
        self.users = {}
        self.seat_heap = None
        self.waitlist_heap = None
        self.rbt = None
        self.root = None
        
    def initialize(self, seat_count):
        """Initialize the events with the specified number of seats, denoted as “seatCount”. The seat numbers will be sequentially assigned as [1, 2, 3, ..., seatCount] and added to the list of unassigned seats.
        """
        
        # If a valid integer is provided 
        #   <seatCount> Seats are made available for reservation 
        if isinstance(seat_count, int) and seat_count > 0:
            self.unassigned_seats = list(range(1, seat_count + 1))
            
            # Initialize heap and tree structures
            self.seat_heap = heap_operations.SeatHeap()
            self.waitlist_heap = heap_operations.WaitlistHeap()
            self.rbt = tree_operations.RedBlackTree()

            # Build the heap with unassigned seats
            self.seat_heap.build_heap(self.unassigned_seats)

            print(f"{self.seat_heap.network_size} seats are made available for reservation")
            visualizations.visualize_binary_heap(self.seat_heap.network)
        else:
            return "Invalid input. Please provide a valid number of seats."

    def available(self):
        """Print the number of seats that are currently available for reservation and the length of the waitlist
        """
        # Total Seats Available : <available seat count>, Waitlist : <waitlist length> 
        # return f"Total Seats Available : {len(self.unassigned_seats)}, Waitlist : <waitlist length>"
        return f"Total Seats Available : {self.seat_heap.network_size}, Waitlist : {self.waitlist_heap.network_size}"

    def reserve(self, user_id, user_priority):
        """Allow a user to reserve the seat that is available from the unassigned seat list and update the reserved seats tree. If no seats are currently available, create a new entry in the waitlist heap as per the user’s priority and timestamp. Print out the seat number if a seat is assigned. If the user is added to the waitlist, print out a message to the user stating that he is added to the waitlist. 
        """
        # If seat is available for reservation 
        #   User <userID> reserved seat <seatID> 
        if self.seat_heap and self.seat_heap.network_size > 0:
            min_seat = self.seat_heap.extract_min()
            print(f"User {user_id} reserved seat {min_seat}")
            self.rbt.insert(user_id, min_seat)

            print(f"    1) Insert into Red-Black Tree User {user_id} and Seat {min_seat} with root node color of {self.rbt.root.color} \n       RBT {self.rbt.tree_network} \n    2) Remove {min_seat} from Seat Heap")

            visualizations.visualize_binary_heap(self.seat_heap.network)
        
        # If the user is added to the waiting list
        #   User <userID> is added to the waiting list
        else:
            self.waitlist_heap.insert((user_priority, user_id))  # Insert based on priority and user ID as a tuple
            print(f"User {user_id} is added to the waiting list")

    def cancel(self, seat_id, user_id):
        """Reassign the seat to user from the waitlist heap. If the waitlist is empty, delete the node and add it back to the available seats. 
        """
        if not self.rbt:
            print("No reservation found.")
            return

        user_node = self.rbt.search(user_id)
        print(f"User node {user_node}")
        # If the user had a booking prior and the waitlist is empty 
        #   User <userID> canceled their reservation 
        if user_node and self.waitlist_heap.network_size == 0:
            print(f"User {user_id} canceled their reservation, so reinsert seat {seat_id} into seat heap")

            print(f"RBT {self.rbt.tree_network}")
            # visualizations.visualize_red_black_tree(self.rbt.tree_network)
            # Need to remove node from tree!!!!
            self.rbt.delete(user_id)
            self.seat_heap.insert(seat_id)

            print(f"RBT {self.rbt.tree_network}")
            visualizations.visualize_binary_heap(self.seat_heap.network)

        # If the user had a booking prior and the waitlist is not empty
        #   User <userID> canceled their reservation
        #   User <userIDx> reserved seat <seatIDx> 
        elif user_node and self.waitlist_heap.network_size != 0:
            pass

        # If the user has no reservation 
        #   User <userID> has no reservation to cancel 
        elif user_node == False:
            print(f"User {user_id} has no reservation to cancel")
        
        # The seat does not belong to the user 
        #   User <userID> has no reservation for seat <seatID> to cancel
        elif user_node == False:
            pass
        else: 
            return "No case found"

    def exit_waitlist(user_id):
        """If the user is in the waiting list, remove him from the waiting list. If the user is already assigned a seat prior to this, the user must use the cancel function to cancel his reservation instead.
        """
        # If the user is in the waiting list 
        #   User <userID> is removed from the waiting list
        
        # If the user is not in the waiting list 
        #   User <userID> is not in waitlist

    def update_priority(user_id, user_priority):
        """Modify the user priority only if he is in the waitlist heap. Update the heap with this modification.
        """

        # If the user is in the waiting list 
        #   User <userID> priority has been updated to <userPriority> 
        
        # If the user is not in the waiting list 
        #   User <userID> priority is not updated

    def add_seats(counts):
        """We add the new seat numbers to the available seat list. The new seat numbers should follow the previously available range.
        """

        # If a valid integer is provided and the waitlist is empty
        #   Additional <count> Seats are made available for reservation 
        
        # If a valid integer is provided and the waitlist is not empty 
        #   Additional <count> Seats are made available for reservation 
        #   User <userID1> reserved seat <seatID1> 
        #   User <userID2> reserved seat <seatID2>
        #   .
        #   .
        #   .

        # If invalid integer is provided 
        #   Invalid input. Please provide a valid number of seats. 

    # def print_reservations(self):
    #     """We print the information of all the assigned seats and the users they are assigned to ordered by the seat Numbers. 
    #     """
    #     for reservation in self.reservations:
    #         seat_id, user_id = reservation
    #         print(f"[seat {seat_id}, user {user_id}]")
    #     # [<seatID1>, <userID1>]
    #     # [<seatID2>, <userID2>]
    #     # [<seatID3>, <userID3>]
    #     #   .
    #     #   .
    #     #   .

    # def print_reservations(self):
    #     nodes = [f"(seat={node.value}, user={node.key})" for node in self.rbt.tree_network]
    #     print("RBT", nodes)

    def print_reservations(self):
        # Initialize a list to store tuples with (seat_number, formatted_string)
        nodes_with_seats = []
        
        # Iterate through each node in the red-black tree's network
        for node in self.rbt.tree_network:
            # Format the node as a string in the desired format
            formatted_node = f"(seat={node.value}, user={node.key})"
            
            # Append a tuple containing the seat number and formatted string to the list
            nodes_with_seats.append((node.value, formatted_node))
        
        # Sort the list of tuples by seat number (first element in each tuple)
        nodes_with_seats.sort()
        
        # Extract the formatted strings in sorted order and store in a new list
        sorted_nodes = []
        for _, formatted_node in nodes_with_seats:
            sorted_nodes.append(formatted_node)
        
        # Print the final sorted list of formatted nodes
        print("RBT", sorted_nodes)


    def release_seats(user_id_1, user_id_2):
        """We release all the seats assigned to the users whose ID falls in the range [userID1, userID2]. It is guaranteed that user_id_2 >= user_id_1. We even remove the users from the waitlist if they are present there. The status of the change should be printed ordered by userID’s in the range.
        """
        # If a valid range is provided and the waitlist is empty
        #   Reservations/waitlist of the users in the range [userID1, userID2] have been released 
        
        # If a valid range is provided and the waitlist is not empty
        #   Reservations of the Users in the range [userID1, userID2] are released
        #   User <userIDa> reserved seat <seatIDa>
        #   User <userIDb> reserved seat <seatIDb>
        # .
        # .
        # . 
        
        # If invalid range is provided 
        #   Invalid input. Please provide a valid range of users.

    def quit(self):
        """Anything below this command in the input file will not be processed. The program terminates either when the quit command is read by the system or when it reaches the end of the input commands, which ever happens first."""
        print("Program Terminated!!")


# Red-Black tree is separate
#   Connect to this main code; book ticket (call reserve) to call red black tree function
# Binary Min-Heap tree is separate
#   Connect to this main code waitlist
