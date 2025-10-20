import copy
from particle import Particle
from walkers import RandomWalker
from animate import create_animation

# --- Simulation Parameters ---
N_PARTICLES_PER_POP = 50
N_STEPS = 500
WALKER_TYPE = "StandardWalker" # Can be "StandardWalker" or "BiasedWalker"

def run_simulation():
    """Sets up and runs the particle diffusion simulation."""
    
    # --- Initialization ---
    # Population 1 starts on the left
    pop1 = [Particle(-10, 0) for _ in range(N_PARTICLES_PER_POP)]
    # Population 2 starts on the right
    pop2 = [Particle(10, 0) for _ in range(N_PARTICLES_PER_POP)]
    
    particles = pop1 + pop2
    
    # Get the walker class from the registry
    WalkerClass = RandomWalker.WALKER_REGISTRY.get(WALKER_TYPE)
    if not WalkerClass:
        raise ValueError(f"Unknown walker type: {WALKER_TYPE}. Available: {list(RandomWalker.WALKER_REGISTRY.keys())}")
        
    # Create a walker instance for each particle
    walkers = [WalkerClass() for _ in particles]
    
    history = []

    # --- Simulation Loop ---
    print(f"Running simulation with {len(particles)} particles for {N_STEPS} steps using {WALKER_TYPE}...")
    for step in range(N_STEPS):
        # Store a deep copy of the current state
        history.append(copy.deepcopy(particles))
        
        # Move each particle
        for i, p in enumerate(particles):
            walkers[i].move(p)
            
    print("Simulation finished.")
    
    # --- Generate Animation ---
    create_animation(history, output_filename=f"diffusion_{WALKER_TYPE}.gif")

if __name__ == "__main__":
    run_simulation()
