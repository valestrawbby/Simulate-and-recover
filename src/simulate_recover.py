import numpy as np
from scipy.optimize import curve_fit

# Define parameter ranges
BOUNDARY_RANGE = (0.5, 2)  # Boundary separation (a)
DRIFT_RANGE = (0.5, 2)     # Drift rate (v)
NONDECISION_RANGE = (0.1, 0.5)  # Non-decision time (t)

def generate_parameters():
    """Randomly generate EZ diffusion model parameters within the given ranges."""
    a = np.random.uniform(*BOUNDARY_RANGE)  # Boundary separation
    v = np.random.uniform(*DRIFT_RANGE)     # Drift rate
    t = np.random.uniform(*NONDECISION_RANGE)  # Non-decision time
    return a, v, t

def simulate_data(a, v, t, N):
    """Simulate reaction times based on the EZ diffusion model for N trials."""
    rt = a / v + t + np.random.normal(0, 0.1, N)  # Add noise to the data
    return rt

def ez_diffusion_model(rt, a, v, t):
    """EZ Diffusion model equation used for curve fitting."""
    return a / v + t + np.random.normal(0, 0.1, len(rt))  # Simulate reaction times

def recover_parameters(rt):
    """Recover parameters from reaction time data using curve fitting."""
    # Initial guess for parameters (boundary separation, drift rate, non-decision time)
    initial_guess = [1, 1, 0.2]
    
    # Fit the reaction time data to the EZ model using curve fitting
    popt, _ = curve_fit(ez_diffusion_model, np.zeros(len(rt)), rt, p0=initial_guess)
    a_hat, v_hat, t_hat = popt
    
    return a_hat, v_hat, t_hat

def run_simulation(N, iterations=1000):
    """Run the simulate-and-recover experiment for N trials over multiple iterations."""
    biases = []
    squared_errors = []
    
    for _ in range(iterations):
        true_a, true_v, true_t = generate_parameters()
        rt = simulate_data(true_a, true_v, true_t, N)
        est_a, est_v, est_t = recover_parameters(rt)

        # Compute bias and squared error
        bias = (est_a - true_a, est_v - true_v, est_t - true_t)
        squared_error = (bias[0]**2, bias[1]**2, bias[2]**2)

        biases.append(bias)
        squared_errors.append(squared_error)
    
    avg_bias = np.mean(biases, axis=0)
    avg_squared_error = np.mean(squared_errors, axis=0)

    # Save the results to a file
    with open(f"results_N_{N}.txt", "a") as file:
        file.write(f"N = {N}: Bias = {avg_bias}, Squared Error = {avg_squared_error}\n")

    return avg_bias, avg_squared_error

if __name__ == "__main__":
    Ns = [10, 40, 4000]
    results = {N: run_simulation(N) for N in Ns}

    for N, (bias, error) in results.items():
        print(f"N = {N}: Bias = {bias}, Squared Error = {error}")

import os

# Ensure the "results" directory exists
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Path for the output file
output_file = os.path.join(RESULTS_DIR, "simulation_results.txt")

# Open the file and write results
with open(output_file, "w") as f:
    for N, (bias, error) in results.items():
        result_str = f"N = {N}: Bias = {bias}, Squared Error = {error}\n"
        print(result_str)  # Still prints to the terminal
        f.write(result_str)  # Saves to file

print(f"Results saved to {output_file}")


