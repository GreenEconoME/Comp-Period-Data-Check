# Import dependencies
import pandas as pd

# Create a function that will divide the property IDs into full/missing lists of property ids for the given compliance year
def divide_cy_ids(partial_cy_df, cy):

    # Create lists to hold the property ids for the full and missing data buildings, respectively
    full_data_list = []
    missing_data_list = []

    # Calculate the number of months needed for full data
    # Either all months to current if compliance period is not completed, or 60 months for five full years of data during the compliance period
    full_length = min(((pd.to_datetime('today').year - pd.to_datetime(f'1/1/{cy - 5}').year) * 12 
                   + (pd.to_datetime('today').month - pd.to_datetime(f'1/1/{cy - 5}').month)), 60)

    # Check the number of entries against the full length variable to divide the properties into full or missing data lists
    for prop_id in partial_cy_df['Property Id'].unique():
        # Check if >= full length because SCG will add an entry of 0 therms before the month is over
        # So the number of datapoints will be one more than what a full data period should be
        if len(partial_cy_df['Property Id'].loc[partial_cy_df['Property Id'] == prop_id]) >= full_length:
            full_data_list.append(prop_id)
        else:
            missing_data_list.append(prop_id)

    return full_data_list, missing_data_list