import matplotlib.pyplot as plt

def render_bar_chart(chart_data, selected_metric):
    data = chart_data.get(selected_metric, {})
    if not data:
        return None

    fig, ax = plt.subplots()
    groups = list(data.keys())
    values = list(data.values())
    ax.bar(groups, values)
    ax.set_ylabel(selected_metric)
    ax.set_title(f"{selected_metric} by Group")
    return fig
