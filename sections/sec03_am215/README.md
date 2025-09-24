# AM215 Section 3: Random Walks — NBA Finals Simulation

In class, we saw that the residuals between the linear increase in a team's score and their actual score resembles gaussian noise. We will explore this concept further in this section.

In both 2015 and 2016, the NBA Finals featured the same two teams: the Golden State Warriors and the Cleveland Cavaliers. However, these two series had significantly different outcomes, and one of the main reasons for this was the difference in team rosters.

In the 2015 Finals, the Cleveland Cavaliers were missing two key players: Kyrie Irving and Kevin Love. Without these critical pieces, the Cavaliers were at a significant disadvantage, and while they put up a strong fight, they eventually lost the series to the Warriors.

In 2016, however, Cleveland was back to full strength, and the Cavaliers, led by LeBron James, mounted an incredible comeback to win the championship, becoming the first team in NBA history to come back from a 3-1 deficit in the Finals.

In this section, we will investigate whether we can see a difference in the two series by comparing the game-by-game score progressions using a random walk model. By looking at the slopes and variances of the scores for each team in both 2015 and 2016, we aim to see how the absence of key players in 2015 influenced the behavior of the random walk that models the score progression. Through this analysis, we can explore how the random elements and structural changes in team dynamics affect the outcome of such high-stakes games.

This introduction sets up the context of the comparison between the two Finals series and introduces the concept of using a random walk model to study the differences in score progression. A much better model than the one we use in this section can be developed, and might be a good direction for a project.

---

## 0) Clone & set up Python

```bash
git clone https://code.harvard.edu/AM215/main_2025.git
cd main_2025/sections/sec03_am215
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

---


## 1) Plot Real Finals Game Progressions

We’ll start by visualizing the **ground-truth score trajectories** for each NBA Finals game (GSW vs. CLE) in **2014–15** and **2015–16**.  
This gives us a baseline picture of pace and momentum before we fit any models.


### Run

```bash
python plot_finals_progress.py
```


### What This Script Does

- Loads Finals metadata and play-by-play score progressions.  
- For each game, plots cumulative score vs. time (seconds) for both teams:  
  - **Solid line** = Golden State Warriors (GSW)  
  - **Dashed line** = Cleveland Cavaliers (CLE)  
- Produces one figure per season with all games overlaid (distinct colors per game).


### Outputs

- plots/score_progress_2014-15.png  
- plots/score_progress_2015-16.png  

---

## 2) Calculate Residuals and Slopes

After plotting the raw Finals score progressions, the next step is to compute some **summary statistics** of the trajectories.  
We focus on **residuals** (deviation from linear fit) and **slopes** (rate of scoring momentum).

### TODOs
- In `calculate_residual_variance_with_slope()`:
  - Fill in the missing linear regression steps for **GSW** and **CLE**:
    - Compute slope and intercept (e.g., via `np.polyfit`).  
    - Predict fitted values.  
    - Compute residuals = actual − predicted.  

### Run

```bash
python calc_residuals_and_slope.py
```

### What This Script Does
- For each game and each team:
  - Fits a simple **linear regression** of score vs. time (up to regulation = 2880 sec).  
  - Computes the **slope** (points per second).  
  - Calculates **residuals** = actual score − linear fit.  
  - Estimates the **residual variance**.  
- Aggregates all residuals across games and overlays histograms with Normal fits.  
- Saves per-game CSVs, residual arrays, and JSON summaries for later modeling.  

### Outputs
- per-game CSVs, residual arrays, and JSON summaries
- plots/residuals_normal_2014-15.png  
- plots/residuals_normal_2015-16.png  

Please see the fitted histograms and Normal overlays to assess how well residuals approximate Gaussian noise.

--- 

## 3) Simulate Games from Saved Means

Using the per-season summary statistics saved in Section 2, we can now simulate **entire basketball games**. This provides a baseline “random walk with drift” model that approximates scoring trajectories for both GSW and CLE.

### TODOs
- In `simulate_basketball_game()`:
  - Generate random perturbations for GSW and CLE (e.g., `np.random.normal`).  
  - Update the loop so each new score = previous score + (drift × time_step) + noise.  

### Run
```bash
python simulate_game.py
```

### What This Script Does
- Simulates score progression for both teams as a **random walk with drift**:  
  - Drift = average slope × time.  
  - Noise = Gaussian perturbations scaled by residual variance.  
- Produces simulated trajectories for each season.  
- Saves plots of simulated GSW vs. CLE games, using solid (GSW) and dashed (CLE) lines.  

### Outputs
- plots/simulated_2014-15.png  
- plots/simulated_2015-16.png  

Please see these simulated plots to compare modeled score dynamics against the real Finals trajectories.

---


## 4) Simulate Best-of-7 Finals Series

Finally, we extend the single-game simulations into **ensembles of full Finals series**.  
By repeatedly simulating games with the fitted slopes and variances, we estimate how often each team (GSW or CLE) would win a best-of-7 series.

### Run

```bash
python simulate_best_of_seven.py
```

### What This Script Does
- Simulates best-of-7 Finals series between GSW and CLE:  
  - Each simulated game produces a final score.  
  - The winner is the team with the higher final score.  
  - First team to 4 wins takes the series.  
- Repeats this process for an ensemble of series (default = 1000).  
- Reports how often each team wins the Finals under this model.

## 5) Final Conceptual Question

### Conceptual question
In basketball the existence of momentum—when one team seems to dominate for a stretch— and its impact on games is highly controversial in the study of sports analytics, with some arguing it’s a myth and others believing it can shift the outcome of a game. The score progression in a game might mostly follow a random walk, but momentum introduces periods where the “random” movement is biased, with one team scoring more rapidly.

Let’s say you believe momentum exists and want to prove that it affects the randomness of a game—how would you go about proving this, and what methods would you use to quantify and analyze its impact?

Hint: Think about how the difference between what actually happens and what a simple model predicts (i.e., the residuals) might tell you something about momentum. What would it mean if there were large discrepancies between expected and actual scores at certain points in the game?