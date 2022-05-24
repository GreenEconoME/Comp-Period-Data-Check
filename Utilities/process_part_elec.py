# Import dependencies
import pandas as pd
import datetime as dt
import streamlit as st

# Import helper functions
from Utilities.create_part_data import create_part_data
from Utilities.divide_cy_ids import divide_cy_ids

def process_part_elec(building_metrics, building_usage):

    # Create a list of the LA Building IDs for properties that are partially electric
    part_elec_ids = list(building_metrics.loc[~(building_metrics['Percent Electricity'].isnull()) 
                                            & (building_metrics['Percent Electricity'] != 100), 
                                            'Los Angeles Building ID'].unique())

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
    all_partials = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(cy_2021)) 
                                & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                & (building_usage['Month'] >= '2016-01-01')
                                & (building_usage['Month'] <= '2020-12-01')]
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

    # Create lists to hold the property ids of buildings with full data (complete) or are missing data (incomplete)
    partial_21_full_data, partial_21_missing_data = divide_cy_ids(partial_21, 2021)
    partial_22_full_data, partial_22_missing_data = divide_cy_ids(partial_22, 2022)
    partial_23_full_data, partial_23_missing_data = divide_cy_ids(partial_23, 2023)
    partial_24_full_data, partial_24_missing_data = divide_cy_ids(partial_24, 2024)
    partial_25_full_data, partial_25_missing_data = divide_cy_ids(partial_25, 2025)

    # Create dataframes for the full and missing data buildings for each compliance year
    partials_df = building_metrics.loc[building_metrics['Property Id'].isin(list(building_metrics.loc[building_metrics['Los Angeles Building ID'].isin(part_elec_ids), 'Property Id']))]

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

    all_partials_data = create_part_data(partials_df, building_usage)
    ind_part_21_full_df = create_part_data(partial_21_full_df, building_usage)
    ind_part_21_miss_df = create_part_data(partial_21_miss_df, building_usage)
    ind_part_22_full_df = create_part_data(partial_22_full_df, building_usage)
    ind_part_22_miss_df = create_part_data(partial_22_miss_df, building_usage)
    ind_part_23_full_df = create_part_data(partial_23_full_df, building_usage)
    ind_part_23_miss_df = create_part_data(partial_23_miss_df, building_usage)
    ind_part_24_full_df = create_part_data(partial_24_full_df, building_usage)
    ind_part_24_miss_df = create_part_data(partial_24_miss_df, building_usage)
    ind_part_25_full_df = create_part_data(partial_25_full_df, building_usage)
    ind_part_25_miss_df = create_part_data(partial_25_miss_df, building_usage)

    #############################
    # Return the partially electric dataframes for buildings with full data, and those with missing data
    return all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df