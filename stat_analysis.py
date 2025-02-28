import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import numpy as np
import scipy.stats as stats
from scipy.stats import ttest_ind, mannwhitneyu
import argparse




def get_csv_files(base_dir, person, resolution, decoding):
    #constructing file path
    csv_path = Path(base_dir) / person / resolution / decoding / "measurements" / "*.csv"

    file_list= glob.glob(str(csv_path))

    return file_list

def calculate_total_energy(file_list):
    # Store total energy values for each test
    total_energy_per_test = []

    # print(f"printing experiment results of {filename}")

    # Process each file separately
    for file in file_list:
        data = pd.read_csv(file)

        filename = os.path.basename(file)


        # Convert time to seconds (assuming nanoseconds in original format)
        data["Time"] = (data["Time"] - data["Time"].min()) / 1e9

        if "PACKAGE_ENERGY (J)" in data.columns:
            total_energy = data["PACKAGE_ENERGY (J)"].iloc[-1] - data["PACKAGE_ENERGY (J)"].iloc[0]
        elif "CPU_ENERGY (J)" in data.columns:
            total_energy = data["CPU_ENERGY (J)"].iloc[-1] - data["CPU_ENERGY (J)"].iloc[0]
        else:
            print(f"Energy column not found in {file}. Please check the column names.")
            exit()

        print(f"{total_energy} - Total energy consumption in file {filename}.")

        
        # if total_energy < 50 and :
        total_energy_per_test.append(total_energy)

    return total_energy_per_test

def save_plot(plt, filename, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    plot_path = os.path.join(output_dir, filename)
    plt.savefig(plot_path)
    plt.show()



def violin_box_plot(df_results, experiment, person, output_dir):
    ### **Plot All Data (Before Outlier Removal)**
    plt.figure(figsize=(10, 6))
    sns.violinplot(y=df_results["Total Energy"], inner=None, color="lightblue", linewidth=1)
    sns.boxplot(y=df_results["Total Energy"], width=0.3, boxprops={'zorder': 2, 'facecolor': 'none'}, showcaps=True, whiskerprops={'linewidth': 2}, medianprops={'color': 'red'}, flierprops={'marker': 'o', 'color': 'black', 'alpha': 0.5})
    sns.stripplot(y=df_results["Total Energy"], color="black", alpha=0.3, size=4)

    plt.ylabel("Total Energy (J)")
    plt.title(f"Violin + Box Plot of Total Energy per Test ({experiment})")
    plt.title(f"Violin + Box Plot of Total Energy per Test ({experiment})")
    plt.grid(True)
  
    save_plot(plt, f"{person}_violin_box_{experiment}.png", output_dir)


def combined_violin_box_plot(df_list, labels, experiment, person, output_dir):
    # Add a column to each DataFrame to indicate the label
    for df, label in zip(df_list, labels):
        df["Label"] = label

    # Combine the DataFrames
    combined_df = pd.concat(df_list)

    plt.figure(figsize=(10, 10))
    sns.violinplot(x="Label", y="Total Energy", data=combined_df, inner=None, linewidth=1)
    sns.boxplot(x="Label", y="Total Energy", data=combined_df, width=0.3, boxprops={'zorder': 2, 'facecolor': 'none'}, showcaps=True, whiskerprops={'linewidth': 2}, medianprops={'color': 'red'}, flierprops={'marker': 'o', 'color': 'black', 'alpha': 0.5})
    sns.stripplot(x="Label", y="Total Energy", data=combined_df, color="black", alpha=0.3, size=4)

    plt.ylabel("Total Energy (J)")
    plt.title(f"Combined Violin + Box Plot of Total Energy per Test {experiment}")
    plt.grid(True)
    plt.legend()

    save_plot(plt, f"{person}_combined_violin_box_{experiment}.png", output_dir)


def outlier_removal(df_results):
    ### **Outlier Removal (Z-score Method)**
    z_scores = stats.zscore(df_results["Total Energy"])
    df_results_filtered = df_results[np.abs(z_scores) < 3]  # Keep only values within 3 standard deviations
    #print(f"Number of outliers removed: {len(df_results) - len(df_results_filtered)}")

    return df_results_filtered

def shapiro_wilk_test(df_results, message):
    shapiro_test = stats.shapiro(df_results["Total Energy"])
    print(f"Shapiro-Wilk Test ({message}): W={shapiro_test.statistic:.4f}, p-value={shapiro_test.pvalue:.4f}")

def perform_welchs_t_test(df1, df2):
    """Performs Welch's t-test for normally distributed data."""
    t_stat, p_value = ttest_ind(df1["Total Energy"], df2["Total Energy"], 
                                equal_var=False, alternative='two-sided')
    print(f"Welch’s T-test Results: t-statistic={t_stat:.4f}, p-value={p_value:.4f}")
    
    if p_value < 0.05:
        print("Statistically significant difference detected (p < 0.05)")
    else:
        print("No statistically significant difference detected (p >= 0.05)")
    return t_stat, p_value

def perform_mann_whitney_u_test(df1, df2):
    """Performs Mann-Whitney U test for non-normal data."""
    u_stat, p_value = mannwhitneyu(df1["Total Energy"], df2["Total Energy"], alternative="two-sided")
    print(f"Mann-Whitney U Test Results: U-statistic={u_stat:.4f}, p-value={p_value:.4f}")
    
    if p_value < 0.05:
        print("Statistically significant difference detected (p < 0.05)")
    else:
        print("No statistically significant difference detected (p >= 0.05)")
    return u_stat, p_value

def calculate_effect_size_normal(df1, df2):
    """Calculates effect size metrics for normally distributed data."""
    mean_exp1 = np.mean(df1["Total Energy"])
    mean_exp2 = np.mean(df2["Total Energy"])
    mean_diff = mean_exp1 - mean_exp2
    percent_change = ((mean_exp1 - mean_exp2) / mean_exp1) * 100
    
    std_exp1 = np.std(df1["Total Energy"], ddof=1)
    std_exp2 = np.std(df2["Total Energy"], ddof=1)
    pooled_std = np.sqrt((std_exp1**2 + std_exp2**2) / 2)
    cohens_d = mean_diff / pooled_std
    
    print("\n--- Effect Size Metrics (Normal Data) ---")
    print(f"Mean Difference: {mean_diff:.4f} J")
    print(f"Percent Change: {percent_change:.2f}%")
    print(f"Cohen’s d: {cohens_d:.4f} (Effect size)")
    
    return mean_diff, percent_change, cohens_d


def calculate_effect_size_non_normal(df1, df2):
    """Calculates effect size metrics for non-normal data."""
    median_exp1 = np.median(df1["Total Energy"])
    median_exp2 = np.median(df2["Total Energy"])
    median_diff = median_exp1 - median_exp2

    median_percentage = 100 - median_exp1 * 100 / median_exp2
    
    # N1 = len(df1)
    # N2 = len(df2)
    # cl_effect_size = u_stat / (N1 * N2)
    
    # Percentage of pairs supporting a conclusion
    # greater_pairs = sum(a > b for a in df1["Total Energy"] for b in df2["Total Energy"])
    # total_pairs = N1 * N2
    # percentage_pairs = greater_pairs / total_pairs
    
    print("\n--- Effect Size Metrics (Non-Normal Data) ---")
    print(f"Median Difference: {median_diff:.4f} J")
    print(f"Median Difference Percentage: {median_percentage}%")
    # print(f"Percentage of pairs where {df1} > {df2}: {percentage_pairs:.4f}")
    


def analyze_statistical_differences(df1, df2, exp1, exp2):
    """Automatically chooses the correct statistical test based on normality."""
    shapiro_test_exp1 = stats.shapiro(df1["Total Energy"])
    shapiro_test_exp2 = stats.shapiro(df2["Total Energy"])
    
    normal_exp1 = shapiro_test_exp1.pvalue >= 0.05
    normal_exp2 = shapiro_test_exp2.pvalue >= 0.05
    
    print(f"Shapiro-Wilk Test {exp1}: W={shapiro_test_exp1.statistic:.4f}, p-value={shapiro_test_exp1.pvalue:.4f}")
    print(f"Shapiro-Wilk Test {exp2}: W={shapiro_test_exp2.statistic:.4f}, p-value={shapiro_test_exp2.pvalue:.4f}")
    
    if normal_exp1 and normal_exp2:
        print("Both datasets are normally distributed. Using Welch’s t-test and Cohen’s d.")
        t_stat, p_value = perform_welchs_t_test(df1, df2)
        return calculate_effect_size_normal(df1, df2)
    else:
        print("At least one dataset is not normally distributed. Using Mann-Whitney U test and CL effect size.")
        u_stat, p_value = perform_mann_whitney_u_test(df1, df2)
        return calculate_effect_size_non_normal(df1, df2, u_stat)


def histogram_plot(df_results, experiment_name, output_dir):
    ### **Histogram of Total Energy (Before Outlier Removal)**
    plt.figure(figsize=(10, 6))
    sns.histplot(df_results["Total Energy"], color="blue", kde=True, bins=20, alpha=0.5)
    plt.xlabel("Total Energy (J)")
    plt.ylabel("Time")
    plt.title(f"Histogram of Total Energy ({experiment_name})")
    plt.grid(True)
    
    save_plot(plt, f"histogram_total_energy_{experiment_name}.png", output_dir)


def qq_plot(df_results, message, output_dir):
    ### **QQ Plot to Check Normality (Before Outlier Removal)**
    plt.figure(figsize=(6, 6))
    stats.probplot(df_results["Total Energy"], dist="norm", plot=plt)
    plt.title(f"QQ Plot of Total Energy ({message})")
    plt.grid(True)

    save_plot(plt, f"qqplot_{message}.png", output_dir)


# Define base directory and subdirectories
base_dir = Path("final_results")  # This can be changed easily
person = "Gijs"
resolution = "1080p"
exp1 = f"decode_{resolution}_h264"
exp2 = f"decode_{resolution}_h265"
experiment = f"decode_{resolution}"

output_dir = os.path.join(f"{person}_graphs", resolution)

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
violin_box_plot(df_results_1, exp1, person, output_dir)
violin_box_plot(df_results_2, exp2, person, output_dir)


#Outlier Removal
df_results_1_filtered = outlier_removal(df_results_1)
df_results_2_filtered = outlier_removal(df_results_2)

combined_violin_box_plot([df_results_1, df_results_2], ["H264", "H265"], experiment, person, output_dir)

#Shapiro-Wilk Test after outlier removal 
# shapiro_wilk_test(df_results_1_filtered, exp1)
# shapiro_wilk_test(df_results_2_filtered, exp2)


### **Shapiro-Wilk Normality Test (Before Outlier Removal)**
shapiro_test_exp1_f = stats.shapiro(df_results_1_filtered["Total Energy"])
shapiro_test_exp2_f = stats.shapiro(df_results_2_filtered["Total Energy"])

print(f"Shapiro-Wilk Test {exp1}: W={shapiro_test_exp1.statistic:.4f}, p-value={shapiro_test_exp1_f.pvalue:.4f}")
print(f"Shapiro-Wilk Test {exp2}: W={shapiro_test_exp2.statistic:.4f}, p-value={shapiro_test_exp2_f.pvalue:.4f}")



### **Plot Data After Outlier Removal**
violin_box_plot(df_results_1_filtered, f"{exp1}_filtered", person, output_dir)
violin_box_plot(df_results_2_filtered, f"{exp2}_filtered", person, output_dir)

combined_violin_box_plot([df_results_1_filtered, df_results_2_filtered], ["H264", "H265"], experiment+" filtered results", person, output_dir)


### **Histogram of Total Energy (Before Outlier Removal)**
histogram_plot(df_results_1, exp1, output_dir)
histogram_plot(df_results_1_filtered, f"{exp1}_filtered", output_dir)

histogram_plot(df_results_2, exp2, output_dir)
histogram_plot(df_results_2_filtered, f"{exp2}_filtered", output_dir)

### **QQ Plot to Check Normality (Before Outlier Removal)**
qq_plot(df_results_1, exp1, output_dir)
qq_plot(df_results_1_filtered, f"{exp1}_filtered", output_dir)


qq_plot(df_results_2, exp1, output_dir)
qq_plot(df_results_2_filtered, f"{exp2}_filtered", output_dir)


###########################



perform_welchs_t_test(df_results_2_filtered, df_results_1_filtered)
calculate_effect_size_normal(df_results_2_filtered, df_results_1_filtered)


u_stat, p_value = perform_mann_whitney_u_test(df_results_1_filtered, df_results_2_filtered)
calculate_effect_size_non_normal(df_results_1_filtered, df_results_2_filtered)


# ### **Measure Differences Between Samples**
# # Mean values
# mean_exp1 = np.mean(df_results_1_filtered["Total Energy"])
# mean_exp2 = np.mean(df_results_2_filtered["Total Energy"])

# # Mean Difference
# mean_diff = mean_exp1 - mean_exp2

# # Percent Change
# percent_change = ((mean_exp1 - mean_exp2) / mean_exp1) * 100

# # Cohen's d
# std_exp1 = np.std(df_results_1_filtered["Total Energy"], ddof=1)  # Standard deviation of full dataset
# std_exp2 = np.std(df_results_2_filtered["Total Energy"], ddof=1)  # Standard deviation of filtered dataset
# pooled_std = np.sqrt((std_exp1**2 + std_exp2**2) / 2)  # Pooled standard deviation
# cohens_d = mean_diff / pooled_std  # Effect size

# ### **Print the Results**
# print(f"\n--- Difference Metrics ---")
# print(f"Mean ({exp1}): {std_exp1:.4f} J")
# print(f"Mean ({exp2}): {std_exp2:.4f} J")
# print(f"Mean Difference: {mean_diff:.4f} J")
# print(f"Percent Change: {percent_change:.2f}%")
# print(f"Cohen’s d: {cohens_d:.4f} (Effect size)")

# # Interpretation of Cohen's d
# if abs(cohens_d) < 0.2:
#     effect_size_interpretation = "Small effect"
# elif abs(cohens_d) < 0.5:
#     effect_size_interpretation = "Medium effect"
# else:
#     effect_size_interpretation = "Large effect"

# print(f"Effect Size Interpretation: {effect_size_interpretation}")
