import pandas as pd

def analyze_ab_test(file):
    df = pd.read_csv(file)

    groups = df['group'].unique()
    metrics = df.columns.difference(['group', 'user_id'])

    summary = f"Groups: {groups.tolist()}\n\n"
    for metric in metrics:
        group_stats = df.groupby('group')[metric].mean()
        summary += f"\nMetric: {metric}\n"
        for group in groups:
            summary += f" - {group}: {group_stats[group]:.4f}\n"

    return summary
