import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def create_animation(history, output_filename="diffusion.gif", n_frames=200):
    """
    Creates and saves an animation of particle diffusion.

    Args:
        history (list): A list where each element is a list of Particle objects
                        representing the state at one time step.
        output_filename (str): The path to save the output GIF file.
        n_frames (int): The number of frames to include in the animation.
    """
    if not history:
        print("Cannot create animation from empty history.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    # Determine plot limits from the first and last frames
    all_x = [p.x for frame in (history[0], history[-1]) for p in frame]
    all_y = [p.y for frame in (history[0], history[-1]) for p in frame]
    if not all_x or not all_y:
        print("Cannot determine plot limits from history.")
        return
        
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    padding_x = (x_max - x_min) * 0.1
    padding_y = (y_max - y_min) * 0.1
    ax.set_xlim(x_min - padding_x, x_max + padding_x)
    ax.set_ylim(y_min - padding_y, y_max + padding_y)
    ax.set_aspect('equal')
    ax.set_title("Particle Diffusion")

    # Split particles into two populations for coloring
    num_particles = len(history[0])
    pop1_indices = range(num_particles // 2)
    pop2_indices = range(num_particles // 2, num_particles)

    # Initialize scatter plots for each population
    scatter1 = ax.scatter([], [], alpha=0.7, label="Population 1")
    scatter2 = ax.scatter([], [], alpha=0.7, label="Population 2")
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    ax.legend()

    # Determine which frames to render to match n_frames
    total_steps = len(history)
    if total_steps > n_frames:
        frame_indices = [int(i * (total_steps - 1) / (n_frames - 1)) for i in range(n_frames)]
    else:
        frame_indices = range(total_steps)

    def update(frame_index):
        """Update function for the animation."""
        frame_data = history[frame_index]
        
        # Population 1
        x1 = [frame_data[i].x for i in pop1_indices]
        y1 = [frame_data[i].y for i in pop1_indices]
        scatter1.set_offsets(list(zip(x1, y1)))

        # Population 2
        x2 = [frame_data[i].x for i in pop2_indices]
        y2 = [frame_data[i].y for i in pop2_indices]
        scatter2.set_offsets(list(zip(x2, y2)))

        time_text.set_text(f"Step: {frame_index}")
        return scatter1, scatter2, time_text

    print(f"Generating animation with {len(frame_indices)} frames...")
    anim = FuncAnimation(fig, update, frames=frame_indices, blit=True, interval=50)
    
    # Saving the animation
    print(f"Saving animation to {output_filename}...")
    anim.save(output_filename, writer='pillow', fps=20)
    print("Animation saved.")
    plt.close(fig)
