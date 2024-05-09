import matplotlib.pyplot as plt
import numpy as np

FONTSIZE = 12

def get_selection_cut_histograms_and_power(column, df_var, log_scale=False, apply_density=True, N_bins=100, N_bins_metric=20, ax=None, range_=(0,1), power=False):
    if not ax:
        fig, ax = plt.subplots()
        
    # range
    ax.hist(df_var[column].to_list(), bins=N_bins, range=range_, density=apply_density, alpha=0.7, label="All Flat-Band Materials", edgecolor="black", color="orange")
    
    # plot histogram for materials matched to a superconductor
    df_matched = df_var[df_var["matched_to_a_sc"]]
    ax.hist(df_matched[column].to_list(), bins=N_bins_metric, range=range_, density=apply_density, alpha=0.7, label="Matched to a Superconductor", edgecolor="black", color="skyblue")    
    
    ax.set_xlabel(column, fontsize=FONTSIZE)
    ax.set_ylabel("Frequency Density", fontsize=FONTSIZE)
    ax.legend(fontsize=FONTSIZE)
    
    if log_scale:
        ax.set_yscale("log")
        
    
    if power:
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

        cut_values = np.linspace(*range_, 100)

        powers = np.zeros_like(cut_values)

        for i, cut_value in enumerate(cut_values):
            cut_mask = df_var[column]<cut_value
            signal_to_noise_with_cut = df_var[cut_mask].matched_to_a_sc.sum() / cut_mask.sum()
            signal_to_noise_without_cut = df_var.matched_to_a_sc.sum() / len(df_var)

            powers[i] = signal_to_noise_with_cut / signal_to_noise_without_cut
        color = "red"
        
        ax2.plot(cut_values, powers, label="Selection Cut Power", color=color)
        ax2.set_xlim(*range_)
        ax2.set_ylabel('Power', color=color, fontsize=FONTSIZE)
        ax2.tick_params(axis='y', labelcolor=color)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    return ax

def get_selection_cut_histograms_and_power_mit(column, df_var, log_scale=False, apply_density=True, N_bins=100, N_bins_metric=20, ax=None, range_=(0,1), power=False):
    if not ax:
        fig, ax = plt.subplots()
        
    # range
    ax.hist(df_var[column].to_list(), bins=N_bins, range=range_, density=apply_density, alpha=0.7, label="All Flat-Band Materials", edgecolor="black", color="orange")
    
    # plot histogram for materials matched to a superconductor
    df_matched = df_var[df_var["spacegroup_number"].notna()]
    ax.hist(df_matched[column].to_list(), bins=N_bins_metric, range=range_, density=apply_density, alpha=0.7, label="Matched to a SC", edgecolor="black", color="skyblue")    
    
    ax.set_xlabel(column, fontsize=FONTSIZE)
    ax.set_ylabel("Frequency Density", fontsize=FONTSIZE)
    ax.legend(fontsize=FONTSIZE)
    
    if log_scale:
        ax.set_yscale("log")
        
    
    if power:
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

        cut_values = np.linspace(*range_, 100)

        powers = np.zeros_like(cut_values)

        for i, cut_value in enumerate(cut_values):
            cut_mask = df_var[column]<cut_value
            signal_to_noise_with_cut = df_var[cut_mask].spacegroup_number.notna().sum() / cut_mask.sum()
            signal_to_noise_without_cut = df_var.spacegroup_number.notna().sum() / len(df_var)

            powers[i] = signal_to_noise_with_cut / signal_to_noise_without_cut
        color = "red"
        
        ax2.plot(cut_values, powers, label="Selection Cut Power", color=color)
        ax2.set_xlim(*range_)
        ax2.set_ylabel('Power', color=color, fontsize=FONTSIZE)
        ax2.tick_params(axis='y', labelcolor=color)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    return ax


def get_selection_cut_histograms_and_power_mit(column, df_var, log_scale=False, apply_density=True, N_bins=100, N_bins_metric=100, ax=None, range_=(0,1), power=False):
    if not ax:
        fig, ax = plt.subplots()
        
    # range
    ax.hist(df_var[column].to_list(), bins=N_bins, range=range_, density=apply_density, alpha=0.7, label="All Flat-Band Materials", edgecolor="black", color="orange")
    
    # plot histogram for materials matched to a superconductor
    df_matched = df_var[df_var["rcsr_name"].notna()]
    ax.hist(df_matched[column].to_list(), bins=N_bins_metric, range=range_, density=apply_density, alpha=0.7, label="Matched to a Tight-Binding FB", edgecolor="black", color="skyblue")    
    
    ax.set_xlabel(column, fontsize=FONTSIZE)
    ax.set_ylabel("Frequency Density", fontsize=FONTSIZE)
    ax.legend(fontsize=FONTSIZE)
    
    if log_scale:
        ax.set_yscale("log")
        
    
    if power:
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

        cut_values = np.linspace(*range_, 100)

        powers = np.zeros_like(cut_values)

        for i, cut_value in enumerate(cut_values):
            cut_mask = df_var[column]<cut_value
            signal_to_noise_with_cut = df_var[cut_mask].rcsr_name.notna().sum() / cut_mask.sum()
            signal_to_noise_without_cut = df_var.rcsr_name.notna().sum() / len(df_var)

            powers[i] = signal_to_noise_with_cut / signal_to_noise_without_cut
        color = "red"
        
        ax2.plot(cut_values, powers, label="Selection Cut Power", color=color)
        ax2.set_xlim(*range_)
        ax2.set_ylabel('Power', color=color, fontsize=FONTSIZE)
        ax2.tick_params(axis='y', labelcolor=color)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    return ax

def get_selection_cut_histograms_and_power_mit_curated(column, df_var, log_scale=False, apply_density=True, N_bins=100, N_bins_metric=30, ax=None, range_=(0,1), power=False):
    df_var.curated.fillna(value=False, inplace=True)
    
    if not ax:
        fig, ax = plt.subplots()
        
    # range
    ax.hist(df_var[column].to_list(), bins=N_bins, range=range_, density=apply_density, alpha=0.7, label="All Flat-Band Materials", edgecolor="black", color="orange")
    
    # plot histogram for materials matched to a superconductor
    df_matched = df_var[df_var.curated]
    ax.hist(df_matched[column].to_list(), bins=N_bins_metric, range=range_, density=apply_density, alpha=0.7, label="Matched to a Curated Tight-Binding FB", edgecolor="black", color="skyblue")    
    
    ax.set_xlabel(column, fontsize=FONTSIZE)
    ax.set_ylabel("Frequency Density", fontsize=FONTSIZE)
    ax.legend()
    
    if log_scale:
        ax.set_yscale("log")
        
    
    if power:
        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

        cut_values = np.linspace(*range_, 100)

        powers = np.zeros_like(cut_values)

        for i, cut_value in enumerate(cut_values):
            cut_mask = (df_var[column]<cut_value)
            signal_to_noise_with_cut = df_var[cut_mask].curated.sum() / cut_mask.sum()
            signal_to_noise_without_cut = df_var.curated.sum() / len(df_var)

            powers[i] = signal_to_noise_with_cut / signal_to_noise_without_cut
        color = "red"
        
        ax2.plot(cut_values, powers, label="Selection Cut Power", color=color)
        ax2.set_xlim(*range_)
        ax2.set_ylabel('Power', color=color, fontsize=FONTSIZE)
        ax2.tick_params(axis='y', labelcolor=color)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    return ax