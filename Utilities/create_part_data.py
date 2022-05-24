import pandas as pd

# Create a function that will create the partial electricity dataframes

def create_part_data(cy_df, usage_df, metrics_df):
    # Create a list to hold the dictionaries of data fro each property id
    data_list = []
    
    # Iterate through the unique property IDs and create a dictionary contatining the data for each prop id
    for prop_id in cy_df['Property Id'].unique():
        try:
            data = {}
            data['Property Id'] = prop_id
            data['Property Name'] = list(cy_df.loc[cy_df['Property Id'] == prop_id, 'Property Name'])[0]
            data['Los Angeles Building ID'] = list(cy_df.loc[cy_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
            data['Primary Property Type'] = list(metrics_df.loc[metrics_df['Property Id'] == prop_id, 'Primary Property Type - Self Selected'])[0]
            data['Earliest Gas Data'] = min(usage_df.loc[(usage_df['Property Id'] == prop_id) & 
                                                            ~(usage_df['Natural Gas Use  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
            data['Latest Gas Data'] = max(usage_df.loc[(usage_df['Property Id'] == prop_id) & ~(usage_df['Natural Gas Use  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
            data_list.append(data)
            
        except ValueError:
            pass
        
    partial_df = pd.DataFrame.from_dict(data_list)
    
    return partial_df