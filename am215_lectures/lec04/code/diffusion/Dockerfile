# Container specifically for running the particle simulation.
# This is intended to be built from *within* the main lecture container.
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulation source code
COPY particle.py walkers.py animate.py run_simulation.py ./

# Define the default command to run the simulation
CMD ["python", "run_simulation.py"]
