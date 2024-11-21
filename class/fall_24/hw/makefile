# Variables
PYTHON := python3
READER := gatorTicketMaster.py
TEST_FILE ?= testCase1.txt  # Default test file if not provided
OUTPUT_FILE := $(basename $(TEST_FILE))_output_file.txt  # Output file based on TEST_FILE name

# Default target
run:
	$(PYTHON) $(READER) $(TEST_FILE) > $(OUTPUT_FILE)
	@echo "Output saved to $(OUTPUT_FILE)"

python_run:
	python3 $(READER) $(TEST_FILE) > $(OUTPUT_FILE)
	@echo "Output saved to $(OUTPUT_FILE)"

# Help target
help:
	@echo "Available commands:"
	@echo "  make PROGRAM_NAME=<file> 	- Run the Python script as an executable"
	@echo "  make TEST_FILE=<file> 		- Run the Python script with the specified test file."
	@echo "  make help             		- Show this help message."
