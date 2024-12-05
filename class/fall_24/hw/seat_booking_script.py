import heap_operations, tree_operations, visualizations, time, sys

class SeatBooking():
    """A class to manage seat creation, reservations, cancelations, and more."""
    def __init__(self):
        self.unassigned_seats = []  # Store unassigned seats
        # self.users = {}
        self.seat_heap = None # Min heap to track available seats
        self.waitlist_heap = None # Min heap to track when no seats are available
        self.rbt = None # Red Black Tree to track assigned seats
        # self.root = None
        self.count_seats = 0 # Track when seats are inilialized and more are added later
        
    def initialize(self, seat_count: int):
        """Initialize the events with the specified number of seats, denoted as “seatCount”. 
        The seat numbers will be sequentially assigned as [1, 2, 3, ..., seatCount] and added to the list of unassigned seats.
        
        Parameter:
        ----------
        seat_count: `int`
            The #seats to be initally unassigned

        """
        self.count_seats = seat_count
        
        # If a valid integer is provided 
        #   <seatCount> Seats are made available for reservation 
        if isinstance(seat_count, int) and seat_count > 0:
            
            # Make seats available for reservation
            start_seat = len(self.unassigned_seats) + 1
            new_seats = list(range(start_seat, start_seat + seat_count))
            self.unassigned_seats.extend(new_seats)
            
            # Initialize heap and tree structures
            self.seat_heap = heap_operations.SeatHeap()
            self.waitlist_heap = heap_operations.WaitlistHeap()
            self.rbt = tree_operations.RedBlackTree()

            # Build the heap with unassigned seats to show which seats are available
            self.seat_heap.build_heap(self.unassigned_seats)
            print(f"{len(self.unassigned_seats)} seats are made available for reservation")
            # visualizations.visualize_binary_heap(self.seat_heap.network)
        else:
            print(f"Invalid input. Please provide a valid number of seats.")

    def available(self):
        """Print the number of seats that are currently available for reservation and the length of the waitlist."""
        print(f"Total Seats Available : {self.seat_heap.network_size}, Waitlist : {self.waitlist_heap.network_size}")
        # return f"Total Seats Available : {self.seat_heap.network_size}, Waitlist : {self.waitlist_heap.network_size}"

    def reserve(self, user_id: int, user_priority: int):
        """Allow a user to reserve the seat that is available from the unassigned seat list and update the reserved seats tree. If no seats are currently available, create a new entry in the waitlist heap as per the user’s priority and timestamp. Print out the seat number if a seat is assigned. If the user is added to the waitlist, print out a message to the user stating that he is added to the waitlist.

        Parameters:
        -----------
        user_id: `int`
            The user that wants to reserve a seat

        user_priority: `int`
            The priority of the user that want wants to reserve a seat
        """

        # If seat is available for reservation 
        #   User <userID> reserved seat <seatID> 
        if self.seat_heap and self.seat_heap.network_size > 0:
            min_seat = self.seat_heap.extract_min() # Remove and heapify min heap to store which seats are available
            print(f"User {user_id} reserved seat {min_seat}")
            self.rbt.insert(user_id, min_seat) # Update seats tree with user and corresponding seat

            # print(f"    1) Insert into Red-Black Tree User {user_id} and Seat {min_seat} \n       RBT {self.rbt.tree_network} \n    2) Remove {min_seat} from Seat Heap")

            # visualizations.visualize_binary_heap(self.seat_heap.network)
        
        # If the user is added to the waiting list
        #   User <userID> is added to the waiting list
        else:
            current_timestamp = time.time() # If two users have same priority, we need to know which reserved a seat first. First come first serve.
            self.waitlist_heap.insert((user_priority, current_timestamp, user_id))
            print(f"User {user_id} is added to the waiting list")

    def cancel(self, seat_id: int, user_id: int):
        """Reassign the seat to a user from the waitlist heap. If the waitlist is empty, delete the node and add it back to the available seats.
        
        Parameters:
        -----------
        seat_id: `int`
            The seat to remove for user and to insert into available seats heap

        user_id: `int`
            The user that wants to reserve a seat

        """
        
        # Check if reserved seats tree exists as if not, then not possible for any user to cancel
        if not self.rbt.tree_network_size == 0:
            print("No reservation found.")
            return

        user_node = self.rbt.search(user_id) # Search for user in reserved seats tree
        # if isinstance(user_node.value, tree_operations.Node):
        #     print(f"User node: {type(user_node)}")

        # self.available()
        # visualizations.visualize_binary_heap(self.seat_heap.network)
        # visualizations.visualize_binary_heap(self.waitlist_heap.network)

        # If the user isn't found
        if not user_node:
            print(f"User {user_id} has no reservation to cancel")
            return
    
        if user_node.value == seat_id: # Ensure user is assigned to seat of interests
            # If the user had a booking prior and the waitlist is empty 
            #   User <userID> canceled their reservation 
            if self.waitlist_heap.network_size == 0:
                
                print(f"User {user_id} canceled their reservation")
                    # print(f"Reinserting seat {seat_id} into seat heap.")
                self.rbt.delete(user_id) # Remove reservation for the user
                self.seat_heap.insert(seat_id) # Insert seat back into seat min heap and heapify to have min as root node
            
            # If the user had a booking prior and the waitlist is not empty
            #   User <userID> canceled their reservation
            #   User <userIDx> reserved seat <seatIDx>
            elif self.waitlist_heap.network_size != 0:
                self.rbt.delete(user_id) # Remove reservation for the user
                self.seat_heap.insert(seat_id) # Insert seat back into seat min heap and heapify to have min as root nodes
                print(f"User {user_id} canceled their reservation")
                self.assign_higest_priority_user()
                
                # print("Pull a new user from waitlist.")
            else:
                print(f"Invalid waitlist heap. Check to see type or if any elements are stored.")

            # visualizations.visualize_binary_heap(self.seat_heap.network)
            # visualizations.visualize_binary_heap(self.waitlist_heap.network)

        else: # User is NOT assigned to seat of interest
            print(f"User {user_id} has no reservation for seat {seat_id} to cancel")

    def exit_waitlist(self, user_id: int):
        """If the user is in the waiting list, remove him from the waiting list. If the user is already assigned a seat prior to this, the user must use the cancel function to cancel his reservation instead.
        
        Parameter:
        ----------
        user_id: `int`
            The user that wants to exit the waitlist heap
        """
        # print(f"Waitlist: {self.waitlist_heap.network}")
        # self.waitlist_heap.extract_min()

        # Check if user has a seat assigned (using Red-Black Tree)
        user_in_rbt = self.rbt.search(user_id)
        if user_in_rbt == False:
            self.waitlist_heap.delete_node(user_id)
        else:
            # print(f"User {user_id} has a seat prior to this, so use cancel function.")
            print(f"User {user_id} is not in waitlist")
        
        # print(f"Waitlist: {self.waitlist_heap.network}")

    def update_priority(self, user_id: int, user_priority: int):
        """Modify the user priority only if the user is in the waitlist heap. Update the heap with this modification.

        Parameters:
        -----------
        user_id: `int`
            The user that wants to reserve a seat
        
        user_priority: `int`
            The new priority level to assign to user

        """
        
        if self.waitlist_heap and self.waitlist_heap.network_size > 0:
            # print(f"waitlist: {self.waitlist_heap.network}")
            # If the user is in the waiting list
            idx_of_user, is_user_in_waitlist = self.waitlist_heap.search(user_id)
            if is_user_in_waitlist == True:
                priority, time, user = self.waitlist_heap.network[idx_of_user]
                # print(f"Before update: {priority}, {time}, {user}")
                self.waitlist_heap.network[idx_of_user] = (user_priority, time, user)
                # print(f"After update: {self.waitlist_heap.network}")
                print(f"User {user_id} priority has been updated to {user_priority}")
            else:
                print(f"User {user_id} priority is not updated")

        else:
            print(f"Check waitlist heap to see if it's initialized or the size of it.")

    def add_seats(self, counts: int):
        """We add the new seat numbers to the available seat list. The new seat numbers should follow the previously available range.
        
        Parameter:
        ----------
        counts: `int`
            The total #new seats to add to available seats list
        """
        # If a valid integer is provided and the waitlist is empty
        #   Additional <count> Seats are made available for reservation 
        # print(f"Previous #seats: {self.count_seats}")
        # print(f"Updated Waitlist: {self.waitlist_heap.network}")
        if isinstance(counts, int) and counts > 0 and self.waitlist_heap.network_size == 0:
            self.unassigned_seats = list(range(1, counts + 1))
            print(self.unassigned_seats)

        # If a valid integer is provided and the waitlist is not empty
        #   Additional <count> Seats are made available for reservation 
        #   User <userID1> reserved seat <seatID1> 
        #   User <userID2> reserved seat <seatID2>
        elif isinstance(counts, int) and counts > 0 and self.waitlist_heap.network_size != 0:
            # Initialize the unassigned seats starting from the next available seat
            # visualizations.visualize_binary_heap(self.seat_heap.network)
            
            # Insert the new seats into the seat heap
            for seat in range(self.count_seats + 1, self.count_seats + counts + 1):
                self.seat_heap.insert(seat)
                # print(f"Inserted seat {seat} into seat heap")
            #     visualizations.visualize_binary_heap(self.seat_heap.network)
            # visualizations.visualize_binary_heap(self.seat_heap.network)

            print(f"Additional {counts} seats are made available for reservation")
            self.seat_heap.network_size = counts
            # print(f"#Available seats: {self.seat_heap.network_size}")
            self.count_seats = self.count_seats + counts
            # print(f"Max priority user: {max_priority_user}")
            self.assign_higest_priority_user()

    def print_reservations(self):
        """Print reservations"""
        # Initialize a list to store tuples with (seat_number, formatted_string)
        nodes_with_seats = []
        
        # Iterate through each node in the red-black tree's network
        for node in self.rbt.tree_network:
            # Format the node as a string in the desired format
            formatted_node = f"Seat {node.value}, User {node.key}"
            
            # Append a tuple containing the seat number and formatted string to the list
            nodes_with_seats.append((node.value, formatted_node))
            # nodes_with_seats.append((" ", " "))
        
        # Sort the list of tuples by seat number (first element in each tuple)
        nodes_with_seats.sort()
        
        # Extract the formatted strings in sorted order and store in a new list
        # Print the sorted formatted strings
        for _, formatted_node in nodes_with_seats:
            print(formatted_node)
        
        # Print the final sorted list of formatted nodes
        # print("RBT", sorted_nodes)

    def release_seats(self, user_id_1: int, user_id_2: int):
        """
        Release all the seats assigned (in Red-Black Tree) to users whose IDs fall 
        in the range [user_id_1, user_id_2]. It is guaranteed that user_id_2 >= user_id_1.
        Remove users from the waitlist if they are present there. The status of the change 
        should be printed ordered by user IDs in the range.

        Once removed from the RBT, insert seats back into the seat heap to make them available.
        """
        # print(f"Pre-RBT: {self.rbt.tree_network}")
        # print(f"Waitlist: {self.waitlist_heap.network}")
        print(f"Reservations of the Users in range [{user_id_1}, {user_id_2}] are released")

        # Validate the range
        if user_id_2 >= user_id_1:
            # Iterate through the range of user IDs
            # print(range(user_id_1, user_id_2 + 1))
            for user_id in range(user_id_1, user_id_2 + 1):
                # print(f"Delete user: {user_id}")

                # _, user_in_waitlist = self.waitlist_heap.search(user_id)
                # print(f"user {user_id} in waitlist: {user_in_waitlist}")
                # if user_in_waitlist == True:
                #     self.waitlist_heap.delete_node(user_id)
                
                # Search for the user in the RBT
                rbt_node = self.rbt.search(user_id)
                # print(node)


                # remove all in waiting list first, then update
                # TA: Chittireddy, Chethan Reddy
                # Let us say we call ReleaseSeats(7,9). Your implementation only works( sometimes) if 1 or more seats have a prior successful reservation and is in the rbt.
 
                # If we have a scenario where all the users 7, 8, 9 are in waiting list, your program would not work as intended and remove none of the users from the waiting list.
                
                # Let’s assume one of the users for example 7 is already assigned a seat and 8, 9 are in the waitlist. There is no guarantee that the chaining of removal would happen and at the end we remove both 8 and 9 from the system(rbt and waitlist), because there could be two other users lets say 10, 11 who had a priority than users 8, 9 and are in waiting list.

                if isinstance(rbt_node, tree_operations.Node):
                    # print(f"Node to delete from RBT: {node.key} : {node.value}")
                    # print(f"{self.rbt.tree_network}")
                    self.rbt.delete(rbt_node.key)
                    # print(f"{self.rbt.tree_network}")
                    # print(f"Released seat for user ID: {node.key}")

                    # Add the released seat back to the seat heap
                    self.seat_heap.insert(rbt_node.value)
                    # visualizations.visualize_binary_heap(self.seat_heap.network)
      
                    self.assign_higest_priority_user()
        else:
            return (f"Invalid input. Please provide a valid range of users")

    def quit(self):
        """Anything below this command in the input file will not be processed. The program terminates either when the quit command is read by the system or when it reaches the end of the input commands, which ever happens first."""
        print("Program Terminated!!")
        sys.exit(0)
        return

    def get_highest_priority_user(self, waitlist: list):
        """Helper function to find the user with the highest priority and earliest timestamp."""
        if not waitlist:
            return None  # Return None if the waitlist is empty
        
        highest_priority_user = waitlist[0]
        for idx, user in enumerate(waitlist):
            if user[0] > highest_priority_user[0]:  # Compare priorities
                highest_priority_user = user
            elif user[0] == highest_priority_user[0]:  # Resolve ties by timestamp
                if user[1] < highest_priority_user[1]:
                    highest_priority_user = user
        return idx - 1, highest_priority_user
    
    def assign_higest_priority_user(self):
        """Helper function to assign the user with the highest priority and earliest timestamp and to perform neccessary actions."""

        # print(f"Waitlist heap: {self.waitlist_heap.network}")

        while self.waitlist_heap.network_size > 0 and self.seat_heap.network_size > 0:
            idx, max_priority_user = self.get_highest_priority_user(self.waitlist_heap.network)
            # print(f"Max priority user: {max_priority_user} at index {idx}")
            if max_priority_user is None: # No user as waitlist is empty
                break
            
            min_seat = self.seat_heap.extract_min() # Get min available seat to assign
            print(f"User {max_priority_user[2]} reserved seat {min_seat}")
            self.rbt.insert(max_priority_user[2], min_seat) # Insert user with corresponding seat

            self.waitlist_heap.network.remove(max_priority_user)
            self.waitlist_heap.network_size = len(self.waitlist_heap.network)