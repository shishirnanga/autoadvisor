import pandas as pd
from scipy.stats import chi2_contingency

def analyze_ab_test(file):
    df = pd.read_csv(file)

    groups = df['group'].unique()
    metrics = df.columns.difference(['group', 'user_id'])

    summary = ""
    chart_data = {}

    for metric in metrics:
        group_stats = df.groupby('group')[metric].mean()
        summary += f"\nMetric: {metric}\n"
        for group in groups:
            value = group_stats[group]
            summary += f" - {group}: {value:.4f}\n"
            chart_data.setdefault(metric, {})[group] = value

        if metric.lower() == "conversion_rate":
            contingency = pd.crosstab(df['group'], df[metric])
            if contingency.shape == (2, 2):
                _, p, _, _ = chi2_contingency(contingency)
                summary += f"   (p-value: {p:.4f}) {'🔹 Significant' if p < 0.05 else '🔸 Not significant'}\n"

    return summary.strip(), chart_data

