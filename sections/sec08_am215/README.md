# AM215 Section 8: Traffic Flow Modeling & Continuous Integration

In this section, you'll implement the car-following model for traffic flow simulation and learn about continuous integration practices in software development.

---

## Learning Goals
- Implement the car-following model using differential equations
- Visualize traffic dynamics and understand how disturbances propagate
- Learn about continuous integration and automated testing practices

---

## What's in this section directory

    traffic_flow.py              # Car-following model implementation and visualization
    requirements.txt             # Project dependencies
    README.md                    # This file

---

## Prerequisites
- **Python 3.9+**
- **Git**

---

## 0) Clone & set up Python

```bash
git clone https://code.harvard.edu/AM215/main_2025.git
cd main_2025/sections/sec08_am215

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt
```

---

## Part 1: The Car-Following Model

The car-following model describes how each car adjusts its speed based on the distance to the car directly in front of it. We model this as a system of differential equations:

**For each car i:**
- Position changes according to velocity: $\frac{dx_i}{dt} = v_i$
- Velocity changes according to car-following rule: $\frac{dv_i}{dt} = \lambda \left( (x_{i-1} - x_i) - d_0 \right)$

Where:
- $x_i$ = position of car $i$
- $v_i$ = velocity of car $i$ 
- $d_0 = 1$ = desired spacing between cars
- $\lambda = 0.5$ = sensitivity parameter

The leading car (car 0) has a prescribed velocity, while all following cars adjust their speed based on the spacing to the car ahead.

---

## 1) Implement the Car-Following Model

Complete the TODOs in `traffic_flow.py` to implement the car-following model.

### Run:

```bash
python3 traffic_flow.py
```

You should see three plots showing car positions, velocities, and phase space.

---

## 2) Conceptual Question

In this traffic model, each car adjusts its speed based on the distance to the car ahead, aiming to maintain a spacing of 1 unit. 

Suppose the leading car experiences a sudden increase in speed. How would this affect the following cars over time? 

What patterns might you expect to observe in their speeds and positions?

---

## Part 2: Continuous Integration using GitHub Actions

Now that you've implemented the car-following model, let's learn about continuous integration and automated testing practices to ensure the reliability of your code.

---

## 1) Set up your own repository

You'll need your own repository where you can push code and set up CI. You have two options:

### Option A: Fork the repository
1. Go to `code.harvard.edu/AM215/main_2025` and click "Fork"
2. This creates your own copy in the AM215 organization
3. Clone your fork: `git clone https://code.harvard.edu/YOUR_USERNAME/main_2025.git`

### Option B: Use your personal GitHub
1. Create a new repository on your personal GitHub
2. Add it as a remote: `git remote add personal https://github.com/YOUR_USERNAME/YOUR_REPO.git`
3. Push to your personal repo: `git push personal main`

---

## 2) Build the test suite

Complete the TODO in `test_traffic_flow.py` to implement tests for your car-following function.

### Run tests locally:
```bash
python -m pytest test_traffic_flow.py -v
```

---

## 3) Set up the CI pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) and pytest configuration (`pytest.ini`) are already provided in this repository.

---

## 4) Test your CI pipeline

1. Commit and push your completed tests and traffic flow implementation
2. Check the Actions tab in your repository
3. Download the coverage report artifact
4. Verify that your tests pass and coverage is generated

---

## 5) Conceptual Questions

### Question 1: Test Coverage
What does test coverage measure? Why is it important for scientific computing?

### Question 2: CI Benefits
What are the main benefits of continuous integration for mathematical modeling projects?

### Question 3: Test Design
How would you test a function that involves numerical integration? What challenges might you face?
