# Import dependencies
import plotly.graph_objects as go
import pandas as pd

# Define function to plot the kBtu energy data
def plot_kbtu_data(building_usage, selected_building, part_or_full):

    # If the selected building is partially electric - plot both gas and electric data
    if part_or_full == 'Partially Electric Buildings':

        # Create electricity trace
        trace_1 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Electricity Use (Grid)  (kBtu)'], 
                            name = 'Electricity Use (Grid) kBtu', 
                            meta = 'Electricity Use (Grid) kBtu',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.1f} kBtu<extra></extra>')

        # Create gas trace
        trace_2 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Natural Gas Use  (kBtu)'], 
                            name = 'Natural Gas Use (kBtu)', 
                            meta = 'Natural Gas Use (kBtu)',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.1f} kBtu<extra></extra>')

        data = [trace_1, trace_2]

    # If the building is fully electric - plot only the electric data
    else:

        # Create electricity trace
        trace_1 = go.Scatter(x = building_usage.loc[building_usage['Property Name'] == selected_building, 'Month'],
                            y = building_usage.loc[building_usage['Property Name'] == selected_building, 'Electricity Use (Grid)  (kBtu)'], 
                            name = 'Electricity Use (Grid) kBtu', 
                            meta = 'Electricity Use (Grid) kBtu',
                            mode = 'lines+markers', 
                            hovertemplate = '%{meta}<br>Date: %{x}<br>Consumption: %{y:,.1f} kBtu<extra></extra>')

        data = [trace_1]

    # Create the figure and update the layout
    fig = go.Figure(data)
    fig.update_layout(
        title = list(building_usage.loc[building_usage['Property Name'] == selected_building, 'Property Name'])[0],
        xaxis_title = 'Date',
        yaxis_title = 'kBtu', 
        showlegend = True)

    return fig