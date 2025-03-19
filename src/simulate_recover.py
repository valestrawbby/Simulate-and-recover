import numpy as np

# Define parameter ranges
BOUNDARY_RANGE = (0.5, 2)
DRIFT_RANGE = (0.5, 2)
NONDECISION_RANGE = (0.1, 0.5)

def generate_parameters():
    """Randomly generate EZ diffusion model parameters within the given ranges."""
    a = np.random.uniform(*BOUNDARY_RANGE)  # Boundary separation
    v = np.random.uniform(*DRIFT_RANGE)     # Drift rate
    t = np.random.uniform(*NONDECISION_RANGE)  # Non-decision time
    return a, v, t

def simulate_data(a, v, t, N):
    """Simulate reaction times based on the EZ diffusion model for N trials."""
    rt = a / v + t + np.random.normal(0, 0.1, N)  # Add noise
    return rt

def recover_parameters(rt):
    """Recover parameters from reaction time data using the EZ model equations."""
    mean_rt = np.mean(rt)
    std_rt = np.std(rt)
    
    v_hat = 1 / mean_rt  # Approximation of drift rate
    a_hat = std_rt * 2    # Approximation of boundary separation
    t_hat = mean_rt - (a_hat / v_hat)  # Approximation of non-decision time
    
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

    return avg_bias, avg_squared_error

if __name__ == "__main__":
    Ns = [10, 40, 4000]
    results = {N: run_simulation(N) for N in Ns}

    for N, (bias, error) in results.items():
        print(f"N = {N}: Bias = {bias}, Squared Error = {error}")
