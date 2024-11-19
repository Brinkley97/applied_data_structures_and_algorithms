import heap_operations, tree_operations, visualizations, time, sys


class SeatBooking():
    def __init__(self):
        self.unassigned_seats = []  # Store unassigned seats
        # self.users = {}
        self.seat_heap = None
        self.waitlist_heap = None
        self.rbt = None
        # self.root = None
        self.count_seats = 0 #
        
    def initialize(self, seat_count):
        """Initialize the events with the specified number of seats, denoted as “seatCount”. 
        The seat numbers will be sequentially assigned as [1, 2, 3, ..., seatCount] and added to the list of unassigned seats."""
        self.count_seats = seat_count
        
        # If a valid integer is provided 
        #   <seatCount> Seats are made available for reservation 
        if isinstance(seat_count, int) and seat_count > 0:
            
            start_seat = len(self.unassigned_seats) + 1
            new_seats = list(range(start_seat, start_seat + seat_count))
            self.unassigned_seats.extend(new_seats)
            
            # Initialize heap and tree structures
            self.seat_heap = heap_operations.SeatHeap()
            self.waitlist_heap = heap_operations.WaitlistHeap()
            self.rbt = tree_operations.RedBlackTree()

            # Build the heap with unassigned seats
            self.seat_heap.build_heap(self.unassigned_seats)

            print(f"{len(self.unassigned_seats)} seats are made available for reservation")
            # visualizations.visualize_binary_heap(self.seat_heap.network)
        else:
            return "Invalid input. Please provide a valid number of seats."

    def available(self):
        """Print the number of seats that are currently available for reservation and the length of the waitlist
        """
        # Total Seats Available : <available seat count>, Waitlist : <waitlist length> 
        # return f"Total Seats Available : {len(self.unassigned_seats)}, Waitlist : <waitlist length>"
        print(f"Total Seats Available : {self.seat_heap.network_size}, Waitlist : {self.waitlist_heap.network_size}")
        # return f"Total Seats Available : {self.seat_heap.network_size}, Waitlist : {self.waitlist_heap.network_size}"

    def reserve(self, user_id, user_priority):
        """Allow a user to reserve the seat that is available from the unassigned seat list and update the reserved seats tree. If no seats are currently available, create a new entry in the waitlist heap as per the user’s priority and timestamp. Print out the seat number if a seat is assigned. If the user is added to the waitlist, print out a message to the user stating that he is added to the waitlist. 
        """
        # If seat is available for reservation 
        #   User <userID> reserved seat <seatID> 
        if self.seat_heap and self.seat_heap.network_size > 0:
            min_seat = self.seat_heap.extract_min()
            print(f"User {user_id} reserved seat {min_seat}")
            self.rbt.insert(user_id, min_seat)

            # print(f"    1) Insert into Red-Black Tree User {user_id} and Seat {min_seat} with root node color of {self.rbt.root.color} \n       RBT {self.rbt.tree_network} \n    2) Remove {min_seat} from Seat Heap")

            # visualizations.visualize_binary_heap(self.seat_heap.network)
        
        # If the user is added to the waiting list
        #   User <userID> is added to the waiting list
        else:
            current_timestamp = time.time()
            self.waitlist_heap.insert((user_priority, current_timestamp, user_id))  # Insert based on priority and user ID as a tuple
            # self.waitlist_by_time.
            print(f"User {user_id} is added to the waiting list")
            # print(f"    waitlist: {self.waitlist_heap.network}")

    def cancel(self, seat_id, user_id):
        """Reassign the seat to a user from the waitlist heap. If the waitlist is empty, delete the node and add it back to the available seats."""

        # print(f"RBT: {self.rbt.tree_network}")
        
        # Check if reservation exists
        if not self.rbt:
            print("No reservation found.")
            return

        # Search for user in reservation tree
        user_node = self.rbt.search(user_id)
        # print(f"User node: {user_node}")
        # print(f"User {user_node.key} with seat {user_node.value}")
    
        # If the user had a booking prior and the waitlist is empty 
        #   User <userID> canceled their reservation 
        if user_node and self.waitlist_heap.network_size == 0:
            if user_node.value == seat_id:
                print(f"User {user_id} canceled their reservation")
                # print(f"Reinserting seat {seat_id} into seat heap.")

                # Remove reservation for the user and insert seat back into seat heap
                self.rbt.delete(user_id)
                self.seat_heap.insert(seat_id)

                # Visualize the updates
                # print(f"Updated RBT: {self.rbt.tree_network}")
                # visualizations.visualize_binary_heap(self.seat_heap.network)
            else:
                print(f"User {user_id} has no reservation for seat {seat_id} to cancel")


        # If the user had a booking prior and the waitlist is not empty
        #   User <userID> canceled their reservation
        #   User <userIDx> reserved seat <seatIDx>
        elif user_node and self.waitlist_heap.network_size != 0:
            if user_node.value == seat_id:
                print(f"User {user_id} canceled their reservation")
                # print("Pulling from waitlist.")

                # Remove user reservation and insert seat back to seat heap
                self.rbt.delete(user_id)
                self.seat_heap.insert(seat_id)
                
                # Initial priority value to track the highest priority user
                previous_priority = 0
                highest_priority_user = None
                highest_priority_index = -1

                # Iterate over waitlist to find highest priority user
                for idx in range(len(self.waitlist_heap.network)):
                    priority, time, user = self.waitlist_heap.network[idx]
                    
                    # Update highest priority if a higher one is found
                    if priority > previous_priority:
                        previous_priority = priority
                        highest_priority_user = user
                        highest_priority_index = idx

                # If a highest-priority user is identified, reassign them to the seat
                if highest_priority_user is not None:
                    # Get the available seat with the lowest ID and assign it to the highest priority user
                    min_seat = self.seat_heap.extract_min()
                    self.rbt.insert(highest_priority_user, min_seat)
                    print(f"User {highest_priority_user} reserved seat {min_seat}")

                    # Remove only the highest-priority user from waitlist by creating a new list without that entry
                    new_waitlist = []
                    for i, entry in enumerate(self.waitlist_heap.network):
                        if i != highest_priority_index:
                            new_waitlist.append(entry)
                    self.waitlist_heap.network = new_waitlist
                    self.waitlist_heap.network_size -= 1  # Update network size

                    # Print updated waitlist
                    # print(f"Updated Waitlist: {self.waitlist_heap.network}")
                    # print(f"RBT: {self.rbt.tree_network}")
            else:
                print(f"User {user_id} has no reservation for seat {seat_id} to cancel")
                # print(f"Updated Waitlist: {self.waitlist_heap.network}")
                # print(f"RBT: {self.rbt.tree_network}")

        # If the user has no booking prior
        elif not user_node:
            print(f"User {user_id} has no reservation to cancel")

        # Case: Seat does not belong to the user (edge case if specific seat check is needed)
        # elif user_node == user_id and user_node.value != seat_id:
        #     print(f"User {user_id} does not have reservation for seat {seat_id} to cancel")

        else:
            print(f"No case found")

    def exit_waitlist(self, user_id):
        """If the user is in the waiting list, remove him from the waiting list. If the user is already assigned a seat prior to this, the user must use the cancel function to cancel his reservation instead.
        """
        # If the user is in the waiting list 
        #   User <userID> is removed from the waiting list
        # print(f"Waitlist: {self.waitlist_heap.network}")
        # self.waitlist_heap.extract_min()
        for priority_user_idx in range(len(self.waitlist_heap.network)):
            updated_priority_user_idx = priority_user_idx + 1
            # priority_user_idx += 1
            # print(f"idx: {priority_user_idx}")
            priority_user = self.waitlist_heap.network[priority_user_idx]
            # print(priority_user)
            priority, time_reserved, user = priority_user
            # user = self.waitlist_heap.search(user_id)
            if user == user_id:
                # pass
                # print(f"User {user_id} is in waitlist")
                # self.waitlist_heap ---> NEED to write code to remove
                self.waitlist_heap.delete_node(user)
            
            # If the user is not in the waiting list 
            #   User <userID> is not in waitlist
            else:
                print(f"User {user_id} is not in waitlist")
            
            break

    def update_priority(self, user_id, user_priority):
        """Modify the user priority only if the user is in the waitlist heap. Update the heap with this modification.
        """
        # print(f"waitlist: {self.waitlist_heap.network}")
        # Iterate over each item in the waitlist heap to find the user by user_id
        for priority_user_idx in range(len(self.waitlist_heap.network)):
            
            # Get the current (priority, user_id) tuple at the index
            priority_user = self.waitlist_heap.network[priority_user_idx]

            # Unpack the priority and user_id for comparison
            original_priority, time_reserved, user = priority_user
            # print(f"Before update: User {user_id} == {user} priority is {original_priority} \n  {self.waitlist_heap.network}")

            
            # Check if the user_id matches the target user_id
            if user == user_id:
                # If the user is found, update the priority and break out of the loop
                self.waitlist_heap.network[priority_user_idx] = (user_priority, time_reserved, user_id)
                # print(f"After update: User {user_id} priority has been updated to {user_priority} \n  {self.waitlist_heap.network}")
                
                # Optional: Reheapify if necessary after the update
                # self.waitlist_heap.build_heap(self.waitlist_heap.network)
                
                print(f"User {user_id} priority has been updated to {user_priority}")
                
            else:
                print(f"User {user_id} priority is not updated")

                
        # print(f"waitlist: {self.waitlist_heap.network}")
    
    def add_seats(self, counts):
        """We add the new seat numbers to the available seat list. The new seat numbers should follow the previously available range."""
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

            # Priority Handling: Get the user with the maximum priority from the waitlist
            # max_priority_user = None
            # max_priority = -float('inf')  # Initialize to a very low value

            # print(f"waitlist: {self.waitlist_heap.network}")

            # for priority_user in self.waitlist_heap.network:
            #     priority, time_reserved, user = priority_user
            #     if priority > max_priority:
            #         max_priority = priority
            #         max_priority_user = (priority, time_reserved, user)

            self.count_seats = self.count_seats + counts
            # print(f"Max priority user: {max_priority_user}")

            # Continue assigning seats to users with the highest priority until there are no more seats left
            while self.seat_heap.network_size > 0 and self.seat_heap.network_size > 0:
                max_priority_user = self.get_highest_priority_user(self.waitlist_heap.network)
                if max_priority_user is None:
                    break
        
                # print(f"Max priority user: {max_priority_user[2]} with priority {max_priority_user[0]} and timestamp {max_priority_user[1]}")

                # Assign seat to the max priority user
                # print(f"Seat Heaps: {self.seat_heap.network}")
                min_seat = self.seat_heap.extract_min()
                print(f"User {max_priority_user[2]} reserved seat {min_seat}")
                self.rbt.insert(max_priority_user[2], min_seat)
                # print(self.rbt.tree_network)

                # Waitlist Update: Pop the user with the maximum priority from the waitlist
                self.waitlist_heap.network.remove(max_priority_user)
                self.waitlist_heap.network_size = len(self.waitlist_heap.network)
                # print(f"Waitlist after assignment: {self.waitlist_heap.network}")

            # If no more seats are available, print the updated waitlist
            if self.waitlist_heap.network_size > 0:
                # print(f"Remaining waitlist: {self.waitlist_heap.network}")
                pass

    def print_reservations(self):
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

    def release_seats(self, user_id_1, user_id_2):
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
            for user_id in range(user_id_1, user_id_2 + 1):
                # Search for the user in the RBT
                node = self.rbt.search(user_id)

                if isinstance(node, tree_operations.Node):
                    # print(f"Node to delete from RBT: {node.key} : {node.value}")
                    self.rbt.delete(node.key)
                    # print(f"Released seat for user ID: {node.key}")

                    # Add the released seat back to the seat heap
                    self.seat_heap.insert(node.value)
                    # visualizations.visualize_binary_heap(self.seat_heap.network)

                    # If the waitlist is not empty, assign seats to users with the highest priority
                    while self.seat_heap.network_size > 0 and self.waitlist_heap.network_size > 0:
                        max_priority_user = self.get_highest_priority_user(self.waitlist_heap.network)

                        if max_priority_user is None:
                            break

                        # print(f"Max priority user: {max_priority_user[2]} with priority {max_priority_user[0]} and timestamp {max_priority_user[1]}")

                        # Assign the seat to the highest priority user
                        min_seat = self.seat_heap.extract_min()
                        print(f"User {max_priority_user[2]} reserved seat {min_seat}")
                        self.rbt.insert(max_priority_user[2], min_seat)

                        # Remove the assigned user from the waitlist
                        self.waitlist_heap.network.remove(max_priority_user)
                        self.waitlist_heap.network_size -= 1
                        # print(f"Waitlist after assignment: {self.waitlist_heap.network}")

                else:
                    # print(f"User ID {user_id} not found in the RBT")
                    pass

            # print(f"Reservations of the Users in range [{user_id_1}, {user_id_2}] are released")
            # print(f"Post-RBT: {self.rbt.tree_network}")
        else:
            return (f"Invalid range: {user_id_2} must be >= {user_id_1}")

    def quit(self):
        """Anything below this command in the input file will not be processed. The program terminates either when the quit command is read by the system or when it reaches the end of the input commands, which ever happens first."""
        print("Program Terminated!!")
        sys.exit()

    def get_highest_priority_user(self, waitlist):
        """Helper function to find the user with the highest priority and earliest timestamp."""
        if not waitlist:
            return None  # Return None if the waitlist is empty
        
        highest_priority_user = waitlist[0]
        for user in waitlist:
            if user[0] > highest_priority_user[0]:  # Compare priorities
                highest_priority_user = user
            elif user[0] == highest_priority_user[0]:  # Resolve ties by timestamp
                if user[1] < highest_priority_user[1]:
                    highest_priority_user = user
        return highest_priority_user