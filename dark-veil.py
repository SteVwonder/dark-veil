import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

def simulate_dark_veil_rolls(num_dice, num_rolls, num_simulations=10000):
    """
    Simulate Dark Veil dice rolls.
    Returns a list of success counts from all simulations.
    -1 menas a critical failure happened (all dice were burned)
    """
    all_successes = []
    
    for _ in range(num_simulations):
        successes = 0
        burned_dice = set()  # Track which dice positions are burned
        active_dice = []
        
        for roll in range(num_rolls):
            # Roll all non-burned dice
            active_dice = [i for i in range(num_dice) if i not in burned_dice]
            if len(active_dice) == 0:
                break
                
            rolls = np.random.randint(1, 7, size=len(active_dice))
            
            # Process this roll
            for i, die in enumerate(active_dice):
                if rolls[i] == 6:
                    successes += 1
                    # Explode: roll again
                    while True:
                        new_roll = np.random.randint(1, 7)
                        if new_roll == 6:
                            successes += 1
                        elif new_roll >= 5:
                            successes += 1
                            break
                        elif new_roll == 1:
                            burned_dice.add(die)
                            break
                        else:
                            break
                elif rolls[i] == 5:
                    successes += 1
                elif rolls[i] == 1:
                    burned_dice.add(die)
        
        if len(burned_dice) == num_dice:
            successes = -1
        all_successes.append(successes)
    
    return all_successes

def plot_probability_distribution(success_counts, num_dice, num_rolls, max_successes, max_probability):
    """Plot the probability distribution of successes."""
    # Calculate probability distribution
    counts = defaultdict(int)
    for success in success_counts:
        counts[success] += 1
    
    total = len(success_counts)
    x = sorted(counts.keys())
    y = [counts[k] / total for k in x]
    
    # Create custom x-axis labels for all possible values up to max_successes
    x_labels = []
    x_ticks = []
    for val in range(-1, max_successes + 1):
        x_ticks.append(val + 0.5)
        if val == -1:
            x_labels.append('Fail')
        else:
            x_labels.append(str(val))
    
    # Plot with bars shifted right by 0.5
    bars = plt.bar([val + 0.5 for val in x], y, width=0.75)
    plt.title(f'{num_dice} dice, {num_rolls} actions')
    plt.xlabel('Number of Successes')
    plt.ylabel('Probability')
    plt.xlim(-1.5, max_successes + 0.5)  # Adjust x-axis to include -1
    plt.ylim(0, max_probability)  # Set consistent y-axis limit
    plt.xticks(x_ticks, x_labels, rotation=90)
    plt.grid(True, alpha=0.3)
    
    # Add count labels on top of each bar
    for bar, count in zip(bars, [counts[k] for k in x]):
        percentage = (count / total) * 100
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f'{percentage:.2f}%', ha='center', va='bottom', rotation=90)

def main():
    parser = argparse.ArgumentParser(description="Simulate and plot Dark Veil dice rolls.")
    parser.add_argument('--plot', action='store_true', help='Save the plot to dark-veil.png instead of displaying it')
    args = parser.parse_args()

    # Parameters to test
    dice_counts = [1, 2, 3, 4, 5]
    roll_counts = [1, 2, 3]
    
    # First, find the maximum possible successes and maximum probability across all simulations
    max_successes = 0
    max_probability = 0
    
    # Store all success counts for each combination
    all_success_counts = {}
    
    for num_rolls in roll_counts:
        for num_dice in dice_counts:
            success_counts = simulate_dark_veil_rolls(num_dice, num_rolls)
            all_success_counts[(num_rolls, num_dice)] = success_counts
            current_max = max(success_counts)
            max_successes = max(max_successes, current_max)
            
            # Calculate probability distribution for this combination
            counts = defaultdict(int)
            for success in success_counts:
                counts[success] += 1
            total = len(success_counts)
            current_max_prob = max(counts.values()) / total
            max_probability = max(max_probability, current_max_prob)
    
    # Add a small padding to the maximum probability
    max_probability = min(1.0, max_probability + 0.15)
    
    # Create a single figure with subplots
    fig, axes = plt.subplots(len(roll_counts), len(dice_counts), figsize=(20, 12))
    
    # Simulate and plot for each combination
    for i, num_rolls in enumerate(roll_counts):
        for j, num_dice in enumerate(dice_counts):
            plt.sca(axes[i, j])  # Set current axis
            success_counts = all_success_counts[(num_rolls, num_dice)]
            plot_probability_distribution(success_counts, num_dice, num_rolls, max_successes, max_probability)
    
    plt.tight_layout(pad=3.0, h_pad=2.0)  # Increased padding between subplots
    if args.plot:
        plt.savefig('dark-veil.png')
        print('Plot saved to dark-veil.png')
    else:
        plt.show()

if __name__ == "__main__":
    main()

