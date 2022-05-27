import plotly.graph_objects as go
import pandas as pd

def plot_kbtu_data(building_usage, selected_building, part_or_full):
    if part_or_full == 'Partially Electric Buildings':
        trace_1 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Electricity Use (Grid)  (kBtu)'], 
                            name = 'Electricity Use (Grid) kBtu', 
                            meta = 'Electricity Use (Grid) kBtu',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.2f} kBtu<extra></extra>')

        trace_2 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Natural Gas Use  (kBtu)'], 
                            name = 'Natural Gas Use (kBtu)', 
                            meta = 'Natural Gas Use (kBtu)',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.2f} kBtu<extra></extra>')

        data = [trace_1, trace_2]

    else:
        trace_1 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Electricity Use (Grid)  (kBtu)'], 
                            name = 'Electricity Use (Grid) kBtu', 
                            meta = 'Electricity Use (Grid) kBtu',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.2f} kBtu<extra></extra>')

        data = [trace_1]

    fig = go.Figure(data)
    fig.update_layout(
        title = list(building_usage.loc[building_usage['Property Name'] == selected_building, 'Property Name'])[0],
        xaxis_title = 'Date',
        yaxis_title = 'kBtu', 
        showlegend = True)

    return fig