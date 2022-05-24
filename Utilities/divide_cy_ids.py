# Import dependencies
import pandas as pd

# Create a function that will divide the property IDs into full/missing lists of property ids for the given compliance year
def divide_cy_ids(partial_cy_df, cy):
    full_data_list = []
    missing_data_list = []
    full_length = min(((pd.to_datetime('today').year - pd.to_datetime(f'1/1/{cy - 5}').year) * 12 
                   + (pd.to_datetime('today').month - pd.to_datetime(f'1/1/{cy - 5}').month)), 60)
    for prop_id in partial_cy_df['Property Id'].unique():
        if len(partial_cy_df['Property Id'].loc[partial_cy_df['Property Id'] == prop_id]) == full_length:
            full_data_list.append(prop_id)
        else:
            missing_data_list.append(prop_id)
    return full_data_list, missing_data_list