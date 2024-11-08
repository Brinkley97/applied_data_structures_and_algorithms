class SeatBooking():
    def __init__(self):
        self.unassigned_seats = []
        self.users = {}
        self.
        
    def initialize(self, seat_count):
        """Initialize the events with the specified number of seats, denoted as “seatCount”. The seat numbers will be sequentially assigned as [1, 2, 3, ..., seatCount] and added to the list of unassigned seats.
        """
        
        # If a valid integer is provided 
        #   <seatCount> Seats are made available for reservation 
        if type(seat_count) == int:
            self.unassigned_seats = []
            for seat_count_i in range(seat_count):
                seat_count_i = seat_count_i + 1
                self.unassigned_seats.append(seat_count_i)
            
            return self.unassigned_seats
        
        # If invalid integer is provided 
        #   Invalid input. Please provide a valid number of seats.
        else:
            return "Invalid input. Please provide a valid number of seats."

    def available(self):
        """Print the number of seats that are currently available for reservation and the length of the waitlist
        """
        # Total Seats Available : <available seat count>, Waitlist : <waitlist length> 
        return f"Total Seats Available : {len(self.unassigned_seats)}, Waitlist : <waitlist length>"

    def reserve(self, user_id, user_priority):
        """Allow a user to reserve the seat that is available from the unassigned seat list and update the reserved seats tree. If no seats are currently available, create a new entry in the waitlist heap as per the user’s priority and timestamp. Print out the seat number if a seat is assigned. If the user is added to the waitlist, print out a message to the user stating that he is added to the waitlist. 
        """
        # If seat is available for reservation 
        #   User <userID> reserved seat <seatID> 
        
        # If the user is added to the waiting list
        #   User <userID> is added to the waiting list

    def cancel(seat_id, user_id):
        """Reassign the seat to user from the waitlist heap. If the waitlist is empty, delete the node and add it back to the available seats. 
        """
        # If the user had a booking prior and the waitlist is empty 
        #   User <userID> canceled their reservation 
        
        # If the user had a booking prior and the waitlist is not empty
        #   User <userID> canceled their reservation
        #   User <userIDx> reserved seat <seatIDx> 
        
        # If the user has no reservation 
        #   User <userID> has no reservation to cancel 
        
        # The seat does not belong to the user 
        #   User <userID> has no reservation for seat <seatID> to cancel

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

    def print_reservations():
        """We print the information of all the assigned seats and the users they are assigned to ordered by the seat Numbers. 
        """
        # [<seatID1>, <userID1>]
        # [<seatID2>, <userID2>]
        # [<seatID3>, <userID3>]
        #   .
        #   .
        #   .

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

    def quit():
        """Anything below this command in the input file will not be processed. The program terminates either when the quit command is read by the system or when it reaches the end of the input commands, which ever happens first."""