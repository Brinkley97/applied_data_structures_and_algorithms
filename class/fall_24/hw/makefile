# Variables
PYTHON := python3
READER := main.py
TEST_FILE ?= testCase_input.txt  # Default test file if not provided
OUTPUT_FILE := $(basename $(TEST_FILE))_output.txt  # Output file based on TEST_FILE name

# Default target
run:
	$(PYTHON) $(READER) $(TEST_FILE) > $(OUTPUT_FILE)
	@echo "Output saved to $(OUTPUT_FILE)"

# Cleanup target
clean:
	@rm -f $(TEST_FILE)
	@echo "Cleaned up file: $(TEST_FILE)"

# Help target
help:
	@echo "Available commands:"
	@echo "  make TEST_FILE=<file> - Run the Python script with the specified test file."
	@echo "  make clean            - Remove the specified test file."
	@echo "  make help             - Show this help message."
