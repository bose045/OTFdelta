import os
import numpy as np
import matplotlib.pyplot as plt

# Function to create a histogram from data
def create_histogram(data, bin_range, folder_name):
    plt.figure()
    plt.hist(data, bins=50, range=bin_range)
    plt.title(f"Histogram for {folder_name}")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig(f"{folder_name}/histogram_merged_data_{lower_bound}_{upper_bound}.pdf")


# Ask user for histogram brackets
lower_bound = float(input("Enter lower bound for histogram: "))
upper_bound = float(input("Enter upper bound for histogram: "))
brackets = (lower_bound, upper_bound)


# Process each merged file
for j in range(8):
    folder_name = f"sys{j}"
    merged_file = os.path.join(folder_name, "merged_data.out")

    # Read column 5 data
    data = []
    with open(merged_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 5:
                try:
                    value = float(parts[4])  # Column 5
                    if lower_bound <= value <= upper_bound:
                        data.append(value)
                except ValueError:
                    continue  # Skip lines that don't have a valid number in column 5

    # Create histogram
    create_histogram(data, brackets, folder_name)

