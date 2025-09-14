import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_dimension(df, dimension):
    data = df[df['dimension'] == dimension]
    grouped = data.groupby('num_points')
    
    Ns = grouped['num_points'].first().values
    mean_estimates = grouped['estimate'].mean().values
    std_estimates = grouped['estimate'].std().values
    true_volume = data['true_volume'].iloc[0]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    ax1.plot(Ns, np.ones_like(Ns) * true_volume, 'r-', label='True Volume')
    ax1.plot(Ns, mean_estimates, 'ko--', label='MC Estimate')
    ax1.fill_between(Ns, mean_estimates - std_estimates, 
                     mean_estimates + std_estimates, 
                     alpha=0.3, color='gray', label='±1 Std Dev')

    ax1.set_xscale('log')
    ax1.set_xlabel('Number of Points')
    ax1.set_ylabel('Volume Estimate')
    ax1.set_title(f"Volume of a {dimension}D Hypersphere")
    ax1.grid(alpha=0.2)
    ax1.legend()

    error = np.abs(mean_estimates - true_volume)
    ax2.loglog(Ns, error, 'ko--', label='MC Error')
    theory_line = error[0] * np.sqrt(Ns[0] / Ns)
    ax2.loglog(Ns, theory_line, 'r-', label='1/√N Scaling')

    ax2.set_xlabel('Number of Points')
    ax2.set_ylabel('Error / Standard Deviation')
    ax2.set_title(f"Error Scaling for {dimension}D Hypersphere")
    ax2.grid(alpha=0.2)
    ax2.legend(loc='lower left')

    plt.tight_layout()
    plt.savefig(f'volume_estimate_{dimension}D.png')
    plt.close()

df = pd.read_csv('results.csv', header=None, names=['dimension','num_points','estimate','true_volume'])

for dimension in df['dimension'].unique():
    plot_dimension(df, dimension)

print("Visualization complete. PNG files generated for each dimension.")
