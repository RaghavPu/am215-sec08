#!/usr/bin/env python3
"""
Analysis of NYC Marathon winning times using Extreme Value Theory.

Demonstrates application of Gumbel distribution to real data, with attention
to assumptions and limitations.
"""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


class MarathonData:
    """
    Load and analyze marathon winning times.
    
    This class handles:
    - Loading CSV data
    - Parsing time strings (various formats)
    - Computing yearly extrema (minima, since we want fastest times)
    - Fitting Gumbel_L distribution
    
    Parameters
    ----------
    csv_path : str
        Path to CSV file with marathon data
    division : str, optional
        Filter by division ('Men', 'Women', or None for all)
    """
    
    def __init__(self, csv_path, division='Men'):
        self.csv_path = csv_path
        self.division = division
        self.df = None
        self.yearly_best_times = None
        self._load_data()
    
    def _load_data(self):
        """Load CSV and validate required columns."""
        self.df = pd.read_csv(self.csv_path)
        
        # Validate columns
        required = ['year', 'time']
        for col in required:
            if col not in self.df.columns:
                raise ValueError(f"CSV must contain '{col}' column")
        
        # Filter by division if specified
        if self.division and 'division' in self.df.columns:
            self.df = self.df[self.df['division'] == self.division].copy()
            print(f"Loaded {len(self.df)} rows ({self.division} division) from {self.csv_path}")
        else:
            print(f"Loaded {len(self.df)} rows from {self.csv_path}")
    
    def parse_time(self, time_str):
        """
        Convert time string to seconds.
        
        Handles formats like:
        - "2:05:34" (hh:mm:ss)
        - "1:23:45" (hh:mm:ss)
        - Numeric values (already in seconds)
        
        TODO: Implement robust time parsing.
        Steps:
          1. Check if input is pd.isna() → return np.nan
          2. Check if already numeric → return as float
          3. For strings: split by ':', handle hh:mm:ss format
          4. Convert to total seconds: hours*3600 + minutes*60 + seconds
          5. Use try/except to return np.nan on errors
        
        Returns
        -------
        float
            Time in seconds, or np.nan if invalid
        """
        # TODO: Implement time parsing
        raise NotImplementedError("Students need to implement parse_time()")
    
    @property
    def yearly_best(self):
        """
        Get the best (minimum) time for each year.
        
        TODO: Implement this property.
        Steps:
          1. Parse all times using self.df['time'].apply(self.parse_time)
          2. Store in self.df['time_seconds']
          3. Group by 'year', take .min() of 'time_seconds'
          4. Drop NaN values and sort by index
          5. Store in self.yearly_best_times and return it
        
        Hint: Use df.groupby('year')['column'].min().dropna().sort_index()
        
        Returns
        -------
        pd.Series
            Best time (seconds) for each year, indexed by year
        """
        if self.yearly_best_times is None:
            # TODO: Implement yearly best calculation
            raise NotImplementedError("Students need to implement yearly_best property")
        
        return self.yearly_best_times
    
    def fit_gumbel_left(self):
        """
        Fit Gumbel_L (left-skewed) distribution to yearly best times.
        
        We use gumbel_l because we're modeling MINIMA (fastest times).
        
        Returns
        -------
        tuple
            (loc, scale) parameters of fitted Gumbel_L
        """
        times = self.yearly_best.values
        loc, scale = stats.gumbel_l.fit(times)
        return loc, scale
    
    def plot_histogram_with_fit(self, ax=None, time_units='hours'):
        """
        Plot histogram of yearly best times with Gumbel_L fit.
        
        Parameters
        ----------
        ax : matplotlib axis or None
        time_units : str
            'hours' or 'seconds'
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        times_sec = self.yearly_best.values
        
        # Convert to desired units
        if time_units == 'hours':
            times_plot = times_sec / 3600.0
            unit_label = 'hours'
            conversion = 3600.0
        else:
            times_plot = times_sec
            unit_label = 'seconds'
            conversion = 1.0
        
        # Fit Gumbel_L (on seconds)
        loc, scale = self.fit_gumbel_left()
        
        # Plot histogram
        bins = max(12, int(np.sqrt(len(times_plot))))
        ax.hist(times_plot, bins=bins, density=True, alpha=0.6,
                edgecolor='k', label='Yearly best times')
        
        # Overlay fitted PDF (with Jacobian adjustment for unit conversion)
        x_plot = np.linspace(times_plot.min() * 0.98, times_plot.max() * 1.02, 400)
        pdf_values = stats.gumbel_l.pdf(x_plot * conversion, loc=loc, scale=scale) * conversion
        
        ax.plot(x_plot, pdf_values, linewidth=2, color='red',
                label=f'Gumbel_L fit\n(loc={loc/conversion:.3f}, scale={scale/conversion:.3f})')
        
        division_str = f" - {self.division}" if self.division else ""
        
        ax.set_xlabel(f'Winning time ({unit_label})')
        ax.set_ylabel('Density')
        ax.set_title(f'NYC Marathon Winning Times{division_str} (n={len(times_sec)} years)')
        ax.legend()
        ax.grid(alpha=0.3)
        
        return ax
    
    def summary_statistics(self):
        """Print summary statistics of the data."""
        times_sec = self.yearly_best.values
        times_hr = times_sec / 3600.0
        
        division_str = f" ({self.division} Division)" if self.division else ""
        
        print("=" * 60)
        print(f"NYC Marathon Winning Times{division_str} - Summary")
        print("=" * 60)
        print(f"Number of years: {len(times_sec)}")
        print(f"Year range: {int(self.yearly_best.index.min())} - {int(self.yearly_best.index.max())}")
        print()
        print(f"Mean winning time:   {times_hr.mean():.3f} hours ({times_sec.mean():.1f} sec)")
        print(f"Std deviation:       {times_hr.std(ddof=1):.3f} hours ({times_sec.std(ddof=1):.1f} sec)")
        print(f"Fastest time:        {times_hr.min():.3f} hours ({times_sec.min():.1f} sec)")
        print(f"Slowest time:        {times_hr.max():.3f} hours ({times_sec.max():.1f} sec)")
        print("=" * 60)


def main():
    """Main analysis routine for marathon data."""
    
    print("=" * 70)
    print("Extreme Value Analysis: NYC Marathon Winning Times")
    print("=" * 70)
    print()
    
    # Load data
    csv_path = 'data/nyc_marathon.csv'
    print(f"Loading data from: {csv_path}\n")
    
    # Analyze Men's division
    try:
        marathon_men = MarathonData(csv_path, division='Men')
    except FileNotFoundError:
        print(f"\nError: Could not find {csv_path}")
        print("Make sure you're running this script from the sec06_am215/ directory")
        return
    
    print()
    marathon_men.summary_statistics()
    print()
    
    # Fit Gumbel_L for Men
    print("Fitting Gumbel_L distribution to Men's yearly best times...")
    loc_m, scale_m = marathon_men.fit_gumbel_left()
    print(f"  Fitted parameters (seconds): loc={loc_m:.2f}, scale={scale_m:.2f}")
    print(f"  Fitted parameters (hours):   loc={loc_m/3600:.3f}, scale={scale_m/3600:.3f}")
    print()
    
    # Optional: Also analyze Women's division
    print("-" * 70)
    print("\nOptional: Analyzing Women's division for comparison...\n")
    
    marathon_women = MarathonData(csv_path, division='Women')
    print()
    marathon_women.summary_statistics()
    print()
    
    loc_w, scale_w = marathon_women.fit_gumbel_left()
    print("Fitting Gumbel_L distribution to Women's yearly best times...")
    print(f"  Fitted parameters (seconds): loc={loc_w:.2f}, scale={scale_w:.2f}")
    print(f"  Fitted parameters (hours):   loc={loc_w/3600:.3f}, scale={scale_w/3600:.3f}")
    print()
    
    # Visualize both
    print("-" * 70)
    print("\nCreating visualizations...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    marathon_men.plot_histogram_with_fit(ax=axes[0], time_units='hours')
    marathon_women.plot_histogram_with_fit(ax=axes[1], time_units='hours')
    
    plt.tight_layout()
    
    output_file = 'marathon_gumbel_fit.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    plt.show()
    
    print()
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("Questions to consider:")
    print("  1. Why do we use Gumbel_L (left-skewed) instead of Gumbel_R?")
    print("  2. Are yearly winning times truly IID?")
    print("  3. What factors might violate EVT assumptions?")
    print("     (training technology, course changes, selection effects)")
    print("  4. How would you test goodness-of-fit? (Q-Q plot, KS test)")
    print("  5. Why do we analyze Men's and Women's divisions separately?")
    print("     What would happen if we mixed them?")
    print("=" * 70)


if __name__ == "__main__":
    main()

