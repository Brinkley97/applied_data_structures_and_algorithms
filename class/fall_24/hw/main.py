import seat_booking_script as sb
import sys

def execute_command(line, seat_booking_instance):
    """
    Parses a line of text and dynamically calls the corresponding method of SeatBooking.
    """
    try:
        func_name, args = line.strip().split("(")
        args = args.rstrip(")").split(",")
        args = [int(arg.strip()) for arg in args if arg.strip().isdigit()]
        func_name = ''.join(['_' + c.lower() if c.isupper() else c for c in func_name]).lstrip('_')

        if hasattr(seat_booking_instance, func_name):
            func = getattr(seat_booking_instance, func_name)
            func(*args)
        else:
            print(f"Unknown command: {func_name}")
    except Exception as e:
        print(f"Error processing line '{line}': {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python reader.py <test_file>")
        return

    file_name = sys.argv[1]
    seat_booking_instance = sb.SeatBooking()

    try:
        with open(file_name, "r") as file:
            for line in file:
                if line.strip():
                    execute_command(line, seat_booking_instance)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

if __name__ == "__main__":
    main()
