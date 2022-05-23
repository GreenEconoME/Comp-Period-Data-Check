import pandas as pd
import numpy as np
import streamlit as st


def clean_data(building_metrics, building_usage, current_ebewe):

    # Drop the unnecessary information from generating the reports
    current_ebewe.drop(columns = ['CUSTOMMODULE2 ID'], inplace = True)
    current_ebewe = current_ebewe.iloc[:-3]

    # Drop the ebewe opps that do not have a dbs building id
    current_ebewe.drop(current_ebewe.loc[current_ebewe['DBS Building ID'] == 'nan'].index, inplace = True)

    # Format the LA Building ID columns
    current_ebewe['DBS Building ID'] = [str(x).split('.')[0] for x in current_ebewe['DBS Building ID']]
    building_metrics['Los Angeles Building ID'] = [str(x).split('.')[0] for x in building_metrics['Los Angeles Building ID']]

    # Remove any leading or trailing spaces in the LA Building ID columns
    building_metrics['Los Angeles Building ID'] = building_metrics['Los Angeles Building ID'].replace(r"^ +| +$", r"", regex=True)
    current_ebewe['DBS Building ID'] = current_ebewe['DBS Building ID'].replace(r"^ +| +$", r"", regex=True)

    # Replace the nan strings values with NaNs
    curent_ebewe = current_ebewe.replace('nan', np.nan)

    # Replace the Not Available values with NaNs
    building_metrics = building_metrics.replace('Not Available', np.nan)
    building_usage = building_usage.replace('Not Available', np.nan)

    # Format the month column to datetime
    building_usage['Month'] = pd.to_datetime(building_usage['Month'], format = '%b-%y')

    # Make the usage columns a numeric datatype
    building_usage[['Electricity Use (Grid)  (kBtu)', 'Natural Gas Use  (kBtu)']] = building_usage[['Electricity Use (Grid)  (kBtu)', 'Natural Gas Use  (kBtu)']].apply(pd.to_numeric)

    # Reducing the building metrics df to contain only buildings that are in the current ebewe opp df
    building_metrics = building_metrics.loc[building_metrics['Los Angeles Building ID'].isin(list(current_ebewe['DBS Building ID']))]

    # Reducing the building usage df to only have the properties within the current ebewe opp df
    building_usage = building_usage.loc[building_usage['Property Id'].isin(list(building_metrics['Property Id']))]

    # Populate the la building id column in the building usage df
    for row in building_usage.index:
        building_usage.loc[row, 'Los Angeles Building ID'] = list(building_metrics.loc[building_metrics['Property Id'] == building_usage.loc[row, 'Property Id'], 'Los Angeles Building ID'])[0]

    # Return the cleaned dataframes
    return building_metrics, building_usage