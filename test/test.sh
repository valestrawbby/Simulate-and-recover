
#!/bin/bash
set -x  # Turn on shell debugging to show each command as it's run

echo "Running the test script..."
cd "$(dirname "$0")/.."
echo "Changed directory to $(pwd)"

echo "Running the simulation..."
./src/main.sh


#!/bin/bash
set -x  # Trace every command

echo "Starting test script..."

# Navigate to the project root (adjust if needed)
cd "$(dirname "$0")/.."
echo "Changed directory to $(pwd)"

echo "Running simulation..."

# Run the main simulation script and capture the output
./src/main.sh
echo "Main script ran"

if [ $? -ne 0 ]; then
    echo "Error: main.sh execution failed!"
    exit 1
fi

# Check if results directory exists
RESULTS_DIR="./results"
echo "Checking results directory..."
if [ ! -d "$RESULTS_DIR" ]; then
    echo "Error: Results directory not found!"
    exit 1
fi

echo "Results directory exists."

# List all result files
RESULT_FILES=("results_N_10.txt" "results_N_40.txt" "results_N_4000.txt")

# Loop through the result files and check if they exist
for RESULT_FILE in "${RESULT_FILES[@]}"; do
    echo "Checking if $RESULT_FILE exists in the results directory..."

    if [ ! -f "$RESULTS_DIR/$RESULT_FILE" ]; then
        echo "Error: $RESULT_FILE not found!"
        exit 1
    fi

    echo "$RESULT_FILE exists."

    # Check if the output file is empty
    echo "Checking if $RESULT_FILE is empty..."
    if [ ! -s "$RESULTS_DIR/$RESULT_FILE" ]; then
        echo "Error: $RESULT_FILE is empty!"
        exit 1
    fi

    echo "$RESULT_FILE is not empty."

    # Display the results
    echo "Displaying content of $RESULT_FILE:"
    cat "$RESULTS_DIR/$RESULT_FILE" || { echo "Failed to display $RESULT_FILE"; exit 1; }
done

echo "All tests passed successfully!"
exit 0

#organization helped by ChatGPT
