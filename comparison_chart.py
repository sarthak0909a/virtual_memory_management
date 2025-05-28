import matplotlib.pyplot as plt

def plot_comparison(results):
    plt.style.use('ggplot')

    algorithms = list(results.keys())
    faults = [results[algo]['faults'] for algo in algorithms]
    hits = [results[algo]['hits'] for algo in algorithms]

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotting lines with markers
    ax.plot(algorithms, faults, label='Page Faults', marker='o', linestyle='-', color='#e74c3c', linewidth=2.5, markersize=9)
    ax.plot(algorithms, hits, label='Page Hits', marker='o', linestyle='-', color='#27ae60', linewidth=2.5, markersize=9)

    # Annotating data points
    for i, (fault, hit) in enumerate(zip(faults, hits)):
        ax.text(i, fault + 0.8, str(fault), ha='center', va='bottom', fontsize=10, color='#c0392b', fontweight='bold')
        ax.text(i, hit + 0.8, str(hit), ha='center', va='bottom', fontsize=10, color='#229954', fontweight='bold')

    # Axis and title
    ax.set_xlabel("Algorithm", fontsize=13, fontweight='bold')
    ax.set_ylabel("Count", fontsize=13, fontweight='bold')
    ax.set_title("Page Replacement Algorithms: Faults vs Hits", fontsize=16, fontweight='bold')
    ax.set_xticks(range(len(algorithms)))
    ax.set_xticklabels(algorithms, rotation=30, fontsize=11)
    ax.tick_params(axis='y', labelsize=11)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)

    # Highlighting best algorithm (by lowest faults)
    min_faults = min(faults)
    best_index = faults.index(min_faults)
    ax.axvspan(best_index - 0.15, best_index + 0.15, color='lightgreen', alpha=0.2, label='Best Faults')

    ax.legend(fontsize=11)

    # --- Table Section ---

    # Increase bottom space
    plt.subplots_adjust(left=0.1, bottom=0.4)  # << Adjusted bottom space
    plt.tight_layout()
    plt.show(block=False)
