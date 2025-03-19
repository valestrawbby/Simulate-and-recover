
#!/bin/bash

echo "Activating virtual environment..."

# Activate the virtual environment (go up one directory from 'src' to 'venv')
source ../venv/bin/activate

echo "Virtual environment activated. Running the script..."

# Ensure the results directory exists
mkdir -p ../results

# Run the script and redirect its output to the results folder
python simulate_recover.py > ../results/output.log 2>&1

echo "Script has finished. Results saved in results/output.log"

# Deactivate the virtual environment
deactivate





if __name__ == "__main__":
    print("Starting simulation...")  # Add this to see if the script reaches here
    Ns = [10, 40, 4000]
    results = {N: run_simulation(N) for N in Ns}

    for N, (bias, error) in results.items():
        print(f"N = {N}: Bias = {bias}, Squared Error = {error}")
