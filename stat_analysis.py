import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import numpy as np
import scipy.stats as stats
from scipy.stats import ttest_ind
import argparse
from scipy.integrate import simpson



def get_csv_files(base_dir, person, resolution, decoding):
    """
    Constructs a file path dynamically and retrieves all matching CSV files.

    :param base_dir: The base directory where results are stored.
    :param machine: The machine folder on which the experiment run.
    :param resolution: The resolution folder.
    :param experiment: The experiment folder.
    :return: List of CSV file paths.
    """
    #constructing file path
    csv_path = Path(base_dir) / person / resolution / decoding / "measurements" / "*.csv"

    file_list= glob.glob(str(csv_path))

    return file_list

def calculate_total_energy(file_list):
    # Store total energy values for each test
    total_energy_per_test = []

    # Process each file separately
    for file in file_list:
        data = pd.read_csv(file)

        # Convert time to seconds (assuming nanoseconds in original format)
        data["Time"] = (data["Time"] - data["Time"].min()) / 1e9

        if "PACKAGE_ENERGY (J)" in data.columns:
            # Compute the total energy by integrating the area under the curve
            total_energy = simpson(data["PACKAGE_ENERGY (J)"], data["Time"])
        elif "CPU_ENERGY (J)" in data.columns:
            # Compute the total energy by integrating the area under the curve
            total_energy = simpson(data["CPU_ENERGY (J)"], data["Time"])
        else:
            print(f"Energy column not found in {file}. Please check the column names.")
            exit()

        total_energy_per_test.append(total_energy)

    return total_energy_per_test

def violin_box_plot(df_results, experiment, person):
    ### **Plot All Data (Before Outlier Removal)**
    plt.figure(figsize=(10, 6))
    sns.violinplot(y=df_results["Total Energy"], inner=None, color="lightblue", linewidth=1)
    sns.boxplot(y=df_results["Total Energy"], width=0.3, boxprops={'zorder': 2, 'facecolor': 'none'}, showcaps=True, whiskerprops={'linewidth': 2}, medianprops={'color': 'red'}, flierprops={'marker': 'o', 'color': 'black', 'alpha': 0.5})
    sns.stripplot(y=df_results["Total Energy"], color="black", alpha=0.3, size=4)

    plt.ylabel("Total Energy (J)")
    plt.title(f"Violin + Box Plot of Total Energy per Test ({experiment})")
    plt.grid(True)
    # Create the directory if it doesn't exist
    output_dir = f"{person}_graphs"
    os.makedirs(output_dir, exist_ok=True)
    
    plot_name = os.path.join(output_dir, f"{person}_violin_box_{experiment}.png")
    plt.savefig(plot_name)
    plt.show()

    print(f"Violin + Box plot saved as {plot_name}")

def combined_violin_box_plot(df_list, labels, experiment, person):
    # Add a column to each DataFrame to indicate the label
    for df, label in zip(df_list, labels):
        df["Label"] = label

    # Combine the DataFrames
    combined_df = pd.concat(df_list)

    plt.figure(figsize=(10, 6))
    sns.violinplot(x="Label", y="Total Energy", data=combined_df, inner=None, linewidth=1)
    sns.boxplot(x="Label", y="Total Energy", data=combined_df, width=0.3, boxprops={'zorder': 2, 'facecolor': 'none'}, showcaps=True, whiskerprops={'linewidth': 2}, medianprops={'color': 'red'}, flierprops={'marker': 'o', 'color': 'black', 'alpha': 0.5})
    sns.stripplot(x="Label", y="Total Energy", data=combined_df, color="black", alpha=0.3, size=4)

    plt.ylabel("Total Energy (J)")
    plt.title(f"Combined Violin + Box Plot of Total Energy per Test {experiment}")
    plt.grid(True)
    plt.legend()

    # Create the directory if it doesn't exist
    output_dir = f"{person}_graphs"
    os.makedirs(output_dir, exist_ok=True)
    
    plot_name = os.path.join(output_dir, f"{person}_combined_violin_box_{experiment}.png")
    plt.savefig(plot_name)
    plt.show()

    print(f"Combined Violin + Box plot saved as {plot_name}")

def outlier_removal(df_results):
    ### **Outlier Removal (Z-score Method)**
    z_scores = stats.zscore(df_results["Total Energy"])
    df_results_filtered = df_results[np.abs(z_scores) < 3]  # Keep only values within 3 standard deviations
    #print(f"Number of outliers removed: {len(df_results) - len(df_results_filtered)}")

    return df_results_filtered

def shapiro_wilk_test(df_results):
    shapiro_test = stats.shapiro(df_results["Total Energy"])
    print(f"Shapiro-Wilk Test (Filtered Data): W={shapiro_test.statistic:.4f}, p-value={shapiro_test.pvalue:.4f}")

def histogram_plot(df_results, experiment_name):
    ### **Histogram of Total Energy (Before Outlier Removal)**
    plt.figure(figsize=(10, 6))
    sns.histplot(df_results["Total Energy"], color="blue", kde=True, bins=20, alpha=0.5)
    plt.xlabel("Total Energy (J)")
    plt.ylabel("Time")
    plt.title(f"Histogram of Total Energy ({experiment_name})")
    plt.grid(True)
    plt.savefig(f"histogram_total_energy_{experiment_name}.png")
    plt.show()

    print(f"Histogram saved as 'histogram_total_energy_{experiment_name}.png'")

def qq_plot(df_results, message):
    ### **QQ Plot to Check Normality (Before Outlier Removal)**
    plt.figure(figsize=(6, 6))
    stats.probplot(df_results["Total Energy"], dist="norm", plot=plt)
    plt.title(f"QQ Plot of Total Energy ({message})")
    plt.grid(True)
    plt.savefig(f"qqplot_{message}.png")
    plt.show()

    print(f"QQ Plot saved as 'qqplot_{message}.png'")

# Define base directory and subdirectories
base_dir = Path("final_results")  # This can be changed easily
person = "Roberto"
resolution = "1080p"
exp1 ="decode_1080p_h264"
exp2 ="decode_1080p_h265"
experiment = "decode_1080p"

print(f"Analyzing results for {person} at {resolution} resolution")

# Convert Path object to string for glob
file_list_exp1 =  get_csv_files(base_dir, person, resolution, exp1)
file_list_exp2 =  get_csv_files(base_dir, person, resolution, exp2)

if not file_list_exp1 or not file_list_exp2:
    print(f"No CSV files found in the directory. Please check the path.")
    exit()

#process csv files
total_energy_per_test_exp1 = calculate_total_energy(file_list_exp1)
total_energy_per_test_exp2 = calculate_total_energy(file_list_exp2)

# Convert to DataFrame for visualization
df_results_1 = pd.DataFrame({"Total Energy": total_energy_per_test_exp1})
df_results_2 = pd.DataFrame({"Total Energy": total_energy_per_test_exp2})

### **Shapiro-Wilk Normality Test (Before Outlier Removal)**
shapiro_test_exp1 = stats.shapiro(df_results_1["Total Energy"])
shapiro_test_exp2 = stats.shapiro(df_results_2["Total Energy"])

print(f"Shapiro-Wilk Test {exp1}: W={shapiro_test_exp1.statistic:.4f}, p-value={shapiro_test_exp1.pvalue:.4f}")
print(f"Shapiro-Wilk Test {exp2}: W={shapiro_test_exp2.statistic:.4f}, p-value={shapiro_test_exp2.pvalue:.4f}")

# Visualize violin + box plots
violin_box_plot(df_results_1, exp1, person)
violin_box_plot(df_results_2, exp2, person)

combined_violin_box_plot([df_results_1, df_results_2], ["H264", "H265"], experiment, person)

#Outlier Removal
df_results_1_filtered = outlier_removal(df_results_1)
df_results_2_filtered = outlier_removal(df_results_2)

#Shapiro-Wilk Test after outlier removal 
shapiro_wilk_test(df_results_1_filtered)
shapiro_wilk_test(df_results_2_filtered)

### **Welch’s T-test (Two-sided)** (but we will use sample a sample b later, since i have no other results i just use these)
t_stat, p_value = ttest_ind(df_results_1_filtered["Total Energy"], 
                            df_results_2_filtered["Total Energy"], 
                            equal_var=False,  # Welch’s t-test assumption
                            alternative='two-sided')

print(f"Welch’s T-test Results: t-statistic={t_stat:.4f}, p-value={p_value:.4f}")

# Interpretation of p-value
if p_value < 0.05:
    print("Statistically significant difference detected between full dataset and filtered dataset (p < 0.05)")
else:
    print("No statistically significant difference detected (p >= 0.05)")

### **Plot Data After Outlier Removal**
violin_box_plot(df_results_1_filtered, f"{exp1}_filtered", person)
violin_box_plot(df_results_2_filtered, f"{exp2}_filtered", person)

### **Histogram of Total Energy (Before Outlier Removal)**
histogram_plot(df_results_1, exp1)
histogram_plot(df_results_1_filtered, f"{exp1}_filtered")

histogram_plot(df_results_2, exp2)
histogram_plot(df_results_2_filtered, f"{exp2}_filtered")

### **QQ Plot to Check Normality (Before Outlier Removal)**
qq_plot(df_results_1, exp1)
qq_plot(df_results_1_filtered, f"{exp1}_filtered")


qq_plot(df_results_2, exp1)
qq_plot(df_results_2_filtered, f"{exp2}_filtered")


###########################


### **Measure Differences Between Samples**
# Mean values
mean_exp1 = np.mean(df_results_1_filtered["Total Energy"])
mean_exp2 = np.mean(df_results_2_filtered["Total Energy"])

# Mean Difference
mean_diff = mean_exp1 - mean_exp2

# Percent Change
percent_change = ((mean_exp1 - mean_exp2) / mean_exp1) * 100

# Cohen's d
std_exp1 = np.std(df_results_1_filtered["Total Energy"], ddof=1)  # Standard deviation of full dataset
std_exp2 = np.std(df_results_2_filtered["Total Energy"], ddof=1)  # Standard deviation of filtered dataset
pooled_std = np.sqrt((std_exp1**2 + std_exp2**2) / 2)  # Pooled standard deviation
cohens_d = mean_diff / pooled_std  # Effect size

### **Print the Results**
print(f"\n--- Difference Metrics ---")
print(f"Mean (All Data): {std_exp1:.4f} J")
print(f"Mean (Filtered Data): {std_exp2:.4f} J")
print(f"Mean Difference: {mean_diff:.4f} J")
print(f"Percent Change: {percent_change:.2f}%")
print(f"Cohen’s d: {cohens_d:.4f} (Effect size)")

# Interpretation of Cohen's d
if abs(cohens_d) < 0.2:
    effect_size_interpretation = "Small effect"
elif abs(cohens_d) < 0.5:
    effect_size_interpretation = "Medium effect"
else:
    effect_size_interpretation = "Large effect"

print(f"Effect Size Interpretation: {effect_size_interpretation}")
