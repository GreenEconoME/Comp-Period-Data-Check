# Import dependencies
import pandas as pd
import datetime as dt
import streamlit as st

def process_part_elec(building_metrics, building_usage):

    # Create a list of the LA Building IDs for properties that are partially electric
    part_elec_ids = list(building_metrics.loc[~(building_metrics['Percent Electricity'].isnull()) & (building_metrics['Percent Electricity'] != 100), 'Los Angeles Building ID'].unique())

    # Create subsets of building ids that are partially electric - seperated by compliance year
    cy_2021 = []
    cy_2022 = []
    cy_2023 = []
    cy_2024 = []
    cy_2025 = []

    # Loop through the partially electric building id's and categorize them into compliance year buildings
    for building in part_elec_ids:
        if building[-1] in ['0', '1']:
            cy_2021.append(building)
            
        elif building[-1] in ['2', '3']:
            cy_2022.append(building)
            
        elif building[-1] in ['4', '5']:
            cy_2023.append(building)
            
        elif building[-1] in ['6', '7']:
            cy_2024.append(building)
            
        elif building[-1] in ['8', '9']:
            cy_2025.append(building)


    # Break the various partially electric buildings into seperate dataframes
    partial_21 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2021)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2016-01-01')
                                    & (building_usage['Month'] <= '2020-12-01')]
    partial_22 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2022)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2017-01-01')
                                    & (building_usage['Month'] <= '2021-12-01')]
    partial_23 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2023)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2018-01-01')
                                    & (building_usage['Month'] <= '2022-12-01')]
    partial_24 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2024)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2019-01-01')
                                    & (building_usage['Month'] <= '2023-12-01')]
    partial_25 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2025)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2020-01-01')
                                    & (building_usage['Month'] <= '2024-12-01')]

    # Create lists to hold the dataframes of buildings with full data (complete) or are missing data (incomplete)

    # Populate the 2021 cy buildings
    partial_21_full_data = []
    partial_21_missing_data = []

    for prop_id in partial_21['Property Id'].unique():
        if len(partial_21.loc[partial_21['Property Id'] == prop_id]) == 60:
            partial_21_full_data.append(prop_id)
        
        else:
            partial_21_missing_data.append(prop_id)

    # Populate the 2022 cy buildings
    partial_22_full_data = []
    partial_22_missing_data = []

    for prop_id in partial_22['Property Id'].unique():
        if len(partial_22.loc[partial_22['Property Id'] == prop_id]) == 60:
            partial_22_full_data.append(prop_id)
        
        else:
            partial_22_missing_data.append(prop_id)

    # Populate the 2023 cy buildings
    # Since 2023 cy is from jan 2018 - dec 2022, will check if have full data until april 2022
    partial_23_full_data = []
    partial_23_missing_data = []

    for prop_id in partial_23['Property Id'].unique():
        if len(partial_23.loc[partial_23['Property Id'] == prop_id]) == 52:
            partial_23_full_data.append(prop_id)
        
        else:
            partial_23_missing_data.append(prop_id)

    # Populate the 2024 cy buildings, check if have data until april 2022
    partial_24_full_data = []
    partial_24_missing_data = []

    for prop_id in partial_24['Property Id'].unique():
        if len(partial_24.loc[partial_24['Property Id'] == prop_id]) == 40:
            partial_24_full_data.append(prop_id)
        
        else:
            partial_24_missing_data.append(prop_id)

    # Populate the 2025 cy buildings, check if have data until april 2022
    partial_25_full_data = []
    partial_25_missing_data = []

    for prop_id in partial_25['Property Id'].unique():
        if len(partial_25.loc[partial_25['Property Id'] == prop_id]) == 28:
            partial_25_full_data.append(prop_id)
        
        else:
            partial_25_missing_data.append(prop_id)

    # Create dataframes for the full and missing data buildings for each compliance year
    partial_21_full_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_21_full_data)]
    partial_21_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_21_missing_data)]

    partial_22_full_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_22_full_data)]
    partial_22_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_22_missing_data)]

    partial_23_full_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_23_full_data)]
    partial_23_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_23_missing_data)]

    partial_24_full_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_24_full_data)]
    partial_24_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_24_missing_data)]

    partial_25_full_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_25_full_data)]
    partial_25_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(partial_25_missing_data)]

    # Create dataframes to save with the building and their earliest and latest gas billing data

    # Creating the dataframes for compliance year 21 with and without complete data
    # Creating full data for 21 compliance year
    ind_part_21_full_data = []
    for prop_id in partial_21_full_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_21_full_df.loc[partial_21_full_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_21_full_df.loc[partial_21_full_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_21_full_data.append(data)
        
    ind_part_21_full_df = pd.DataFrame.from_dict(ind_part_21_full_data)

    # Creating missing data for 21 compliance year
    ind_part_21_miss_data = []
    for prop_id in partial_21_miss_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_21_miss_df.loc[partial_21_miss_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_21_miss_df.loc[partial_21_miss_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_21_miss_data.append(data)
        
    ind_part_21_miss_df = pd.DataFrame.from_dict(ind_part_21_miss_data)

    #########

    # Creating the dataframes for compliance year 22 with and without complete data
    # Creating full data for 22 compliance year
    ind_part_22_full_data = []
    for prop_id in partial_22_full_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_22_full_df.loc[partial_22_full_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_22_full_df.loc[partial_22_full_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_22_full_data.append(data)
        
    ind_part_22_full_df = pd.DataFrame.from_dict(ind_part_22_full_data)

    # Creating missing data for 22 compliance year
    ind_part_22_miss_data = []
    for prop_id in partial_22_miss_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_22_miss_df.loc[partial_22_miss_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_22_miss_df.loc[partial_22_miss_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_22_miss_data.append(data)
        
    ind_part_22_miss_df = pd.DataFrame.from_dict(ind_part_22_miss_data)

    #########

    # Creating the dataframes for compliance year 23 with and without complete data
    # Creating full data for 23 compliance year
    ind_part_23_full_data = []
    for prop_id in partial_23_full_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_23_full_df.loc[partial_23_full_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_23_full_df.loc[partial_23_full_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_23_full_data.append(data)
        
    ind_part_23_full_df = pd.DataFrame.from_dict(ind_part_23_full_data)

    # Creating missing data for 23 compliance year
    ind_part_23_miss_data = []
    for prop_id in partial_23_miss_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_23_miss_df.loc[partial_23_miss_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_23_miss_df.loc[partial_23_miss_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_23_miss_data.append(data)
        
    ind_part_23_miss_df = pd.DataFrame.from_dict(ind_part_23_miss_data)

    #########

    # Creating the dataframes for compliance year 24 with and without complete data
    # Creating full data for 24 compliance year
    ind_part_24_full_data = []
    for prop_id in partial_24_full_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_24_full_df.loc[partial_24_full_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_24_full_df.loc[partial_24_full_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_24_full_data.append(data)
        
    ind_part_24_full_df = pd.DataFrame.from_dict(ind_part_24_full_data)

    # Creating missing data for 24 compliance year
    ind_part_24_miss_data = []
    for prop_id in partial_24_miss_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_24_miss_df.loc[partial_24_miss_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_24_miss_df.loc[partial_24_miss_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_24_miss_data.append(data)
        
    ind_part_24_miss_df = pd.DataFrame.from_dict(ind_part_24_miss_data)

    #########

    # Creating the dataframes for compliance year 25 with and without complete data
    # Creating full data for 25 compliance year
    ind_part_25_full_data = []
    for prop_id in partial_25_full_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_25_full_df.loc[partial_25_full_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_25_full_df.loc[partial_25_full_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_25_full_data.append(data)
        
    ind_part_25_full_df = pd.DataFrame.from_dict(ind_part_25_full_data)

    # Creating missing data for 25 compliance year
    ind_part_25_miss_data = []
    for prop_id in partial_25_miss_df['Property Id'].unique():
        data = {}
        
        data['Property Id'] = prop_id
        
        data['Property Name'] = list(partial_25_miss_df.loc[partial_25_miss_df['Property Id'] == prop_id, 'Property Name'])[0]
        
        data['Los Angeles Building ID'] = list(partial_25_miss_df.loc[partial_25_miss_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
        
        data['Earliest Gas Data'] = dt.datetime.date(min(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        data['Latest Gas Data'] = dt.datetime.date(max(building_usage.loc[(building_usage['Property Id'] == prop_id) 
                                                                                            & ~(building_usage['Natural Gas Use  (kBtu)'].isna()), 'Month'])).strftime('%b, %Y')
        
        ind_part_25_miss_data.append(data)
        
    ind_part_25_miss_df = pd.DataFrame.from_dict(ind_part_25_miss_data)

    #############################
    # Return the partially electric dataframes for buildings with full data, and those with missing data
    return ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df