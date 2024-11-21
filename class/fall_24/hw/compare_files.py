import sys

def compare_files(file1, file2):
    """
    Compare two files to see if they are identical.
    
    Args:
    - file1: path to the first file.
    - file2: path to the second file.
    
    Returns:
    - True if the files are identical, False otherwise.
    """
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()

            # Compare the lines in the two files
            if file1_lines == file2_lines:
                print("The files are identical.")
                return True
            else:
                print("The files are different.")
                return False

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

def main():
    # Check if we have enough arguments (the two file names)
    if len(sys.argv) != 3:
        print("Usage: python compare_files.py <file1> <file2>")
        sys.exit(1)

    # Get the file paths from the command line arguments
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    # Compare the files
    compare_files(file1, file2)

if __name__ == "__main__":
    main()
