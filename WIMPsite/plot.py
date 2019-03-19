import plotly.graph_objs as go

from plotly.offline import plot


def plot_graph(x, y, title):
    trace1 = go.Scatter(x=x, y=y)

    data = [trace1]
    layout = go.Layout(xaxis=dict(autorange=True), yaxis=dict(autorange=True), title=title)

    fig = go.Figure(data=data, layout=layout)

    return plot(fig, output_type='div', include_plotlyjs=False)
