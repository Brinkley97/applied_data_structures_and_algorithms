import seat_booking_script as sb
import sys

class GatorTicketMaster:
    def __init__(self):
        self.store_output = []

    def write_output(self, output_text):
        """
        Adds text to the output buffer to be written to the file later.
        """
        self.store_output.append(output_text)

    def save_output(self, output_filename):
        """
        Saves all accumulated output lines to the specified output file.
        """
        with open(output_filename, "w") as f:
            for line in self.store_output:
                f.write(line + "\n")

def execute_command(line, seat_booking_instance, gator):
    """
    Parses a line of text and dynamically calls the corresponding method of SeatBooking.
    """
    try:
        # Check for quit command
        if line.strip() == "quit()":
            sys.exit(0)

        # Parse function name and arguments
        func_name, args = line.strip().split("(")
        args = args.rstrip(")").split(",")
        args = [int(arg.strip()) for arg in args if arg.strip().isdigit()]
        func_name = ''.join(['_' + c.lower() if c.isupper() else c for c in func_name]).lstrip('_')

        # Dynamically call the function and capture its output
        if hasattr(seat_booking_instance, func_name):
            func = getattr(seat_booking_instance, func_name)
            result = func(*args)
            if result is not None:  # Capture return values if present
                gator.write_output(result)
        else:
            gator.write_output(f"Unknown command: {func_name}")
    except Exception as e:
        gator.write_output(f"Error processing line '{line}': {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gatorTicketMaster.py <test_file>")
        return

    input_filename = sys.argv[1]
    # Generate output filename dynamically
    output_filename = f"{input_filename.rsplit('.', 1)[0]}_output_file.txt"

    seat_booking_instance = sb.SeatBooking()
    gator = GatorTicketMaster()

    try:
        with open(input_filename, "r") as file:
            for line in file:
                if line.strip():
                    execute_command(line, seat_booking_instance, gator)

        # Save all output to the file
        gator.save_output(output_filename)
        # print(f"Output saved to {output_filename}")

    except FileNotFoundError:
        print(f"File '{input_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
