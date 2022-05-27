# Import dependencies
import pandas as pd
import datetime as dt
import streamlit as st
import numpy as np

# Import helper functions
from Utilities.create_part_and_full_data import create_energy_data
from Utilities.divide_cy_ids import divide_cy_ids

def process_part_full_elec(building_metrics, building_usage, building_compliance):

    # Create a list of the LA Building IDs for properties that are partially electric
    part_elec_ids = list(building_metrics.loc[~(building_metrics['Percent Electricity'].isnull()) 
                                            & (building_metrics['Percent Electricity'] != 100), 
                                            'Los Angeles Building ID'].unique())

    # Create a list of LA Building IDs for properties that are fully electric
    full_elec_ids = []

    for dbs_id in building_metrics.loc[building_metrics['Percent Electricity'] == 100, 'Los Angeles Building ID'].unique():
        if dbs_id not in part_elec_ids:
            full_elec_ids.append(dbs_id)

    # Create subsets of building ids that are partially electric - divided by compliance year
    part_cy_21 = []
    part_cy_22 = []
    part_cy_23 = []
    part_cy_24 = []
    part_cy_25 = []

    # Create subsets of building ids that are fully electric - divided by compliance year
    full_elec_cy_21 = []
    full_elec_cy_22 = []
    full_elec_cy_23 = []
    full_elec_cy_24 = []
    full_elec_cy_25 = []

    # Loop through the partially electric building id's and categorize them into compliance year buildings
    for building in part_elec_ids:
        if building[-1] in ['0', '1']:
            part_cy_21.append(building)
            
        elif building[-1] in ['2', '3']:
            part_cy_22.append(building)
            
        elif building[-1] in ['4', '5']:
            part_cy_23.append(building)
            
        elif building[-1] in ['6', '7']:
            part_cy_24.append(building)
            
        elif building[-1] in ['8', '9']:
            part_cy_25.append(building)
            
    # Loop through the fully electric building id's and categorize them into compliance year buildings
    for building in full_elec_ids:
        if building[-1] in ['0', '1']:
            full_elec_cy_21.append(building)
            
        elif building[-1] in ['2', '3']:
            full_elec_cy_22.append(building)
            
        elif building[-1] in ['4', '5']:
            full_elec_cy_23.append(building)
            
        elif building[-1] in ['6', '7']:
            full_elec_cy_24.append(building)
            
        elif building[-1] in ['8', '9']:
            full_elec_cy_25.append(building)


    # Break the various partially electric buildings into seperate dataframes
    all_partials = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_21)) 
                                & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                & (building_usage['Month'] >= '2016-01-01')
                                & (building_usage['Month'] <= '2020-12-01')]
    partial_21 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_21)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2016-01-01')
                                    & (building_usage['Month'] <= '2020-12-01')]
    partial_22 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_22)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2017-01-01')
                                    & (building_usage['Month'] <= '2021-12-01')]
    partial_23 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_23)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2018-01-01')
                                    & (building_usage['Month'] <= '2022-12-01')]
    partial_24 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_24)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2019-01-01')
                                    & (building_usage['Month'] <= '2023-12-01')]
    partial_25 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(part_cy_25)) 
                                    & ~(building_usage['Natural Gas Use  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2020-01-01')
                                    & (building_usage['Month'] <= '2024-12-01')]

    # Break the various fully electric buildings into seperate dataframes
    all_fully_elec = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_ids)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2016-01-01')
                                    & (building_usage['Month'] <= '2020-12-01')]
    full_elec_21 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_cy_21)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2016-01-01')
                                    & (building_usage['Month'] <= '2020-12-01')]
    full_elec_22 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_cy_22)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2017-01-01')
                                    & (building_usage['Month'] <= '2021-12-01')]
    full_elec_23 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_cy_23)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2018-01-01')
                                    & (building_usage['Month'] <= '2022-12-01')]
    full_elec_24 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_cy_24)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2019-01-01')
                                    & (building_usage['Month'] <= '2023-12-01')]
    full_elec_25 = building_usage.loc[(building_usage['Los Angeles Building ID'].isin(full_elec_cy_25)) 
                                    & ~(building_usage['Electricity Use (Grid)  (kBtu)'].isna())
                                    & (building_usage['Month'] >= '2020-01-01')
                                    & (building_usage['Month'] <= '2024-12-01')]

    # Create lists to hold the property ids of buildings with full data (complete) or are missing data (incomplete)
    partial_21_full_data, partial_21_missing_data = divide_cy_ids(partial_21, 2021)
    partial_22_full_data, partial_22_missing_data = divide_cy_ids(partial_22, 2022)
    partial_23_full_data, partial_23_missing_data = divide_cy_ids(partial_23, 2023)
    partial_24_full_data, partial_24_missing_data = divide_cy_ids(partial_24, 2024)
    partial_25_full_data, partial_25_missing_data = divide_cy_ids(partial_25, 2025)

    # Create lists to hold the property ids of fully electric buildings with full data (complete) or are missing data (incomplete)
    elec_21_full_data, elec_21_missing_data = divide_cy_ids(full_elec_21, 2021)
    elec_22_full_data, elec_22_missing_data = divide_cy_ids(full_elec_22, 2022)
    elec_23_full_data, elec_23_missing_data = divide_cy_ids(full_elec_23, 2023)
    elec_24_full_data, elec_24_missing_data = divide_cy_ids(full_elec_24, 2024)
    elec_25_full_data, elec_25_missing_data = divide_cy_ids(full_elec_25, 2025)

    # Create dataframes for the full and missing data partially electric buildings for each compliance year
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

    # Create dataframes for the full and missing data fully electric buildings for each compliance year
    full_elec_df = building_metrics.loc[building_metrics['Property Id'].isin(list(building_metrics.loc[building_metrics['Los Angeles Building ID'].isin(full_elec_ids), 'Property Id']))]

    elec_21_full_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_21_full_data)]
    elec_21_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_21_missing_data)]

    elec_22_full_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_22_full_data)]
    elec_22_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_22_missing_data)]

    elec_23_full_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_23_full_data)]
    elec_23_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_23_missing_data)]

    elec_24_full_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_24_full_data)]
    elec_24_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_24_missing_data)]

    elec_25_full_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_25_full_data)]
    elec_25_miss_df = building_metrics.loc[building_metrics['Property Id'].isin(elec_25_missing_data)]

    # Create dataframes to save with the building and their earliest and latest gas/electric billing data
    ind_part_21_full_df = create_energy_data(partial_21_full_df, building_usage, building_metrics, building_compliance, 2021, True)
    ind_part_21_miss_df = create_energy_data(partial_21_miss_df, building_usage, building_metrics, building_compliance, 2021, True)
    ind_part_22_full_df = create_energy_data(partial_22_full_df, building_usage, building_metrics, building_compliance, 2022, True)
    ind_part_22_miss_df = create_energy_data(partial_22_miss_df, building_usage, building_metrics, building_compliance, 2022, True)
    ind_part_23_full_df = create_energy_data(partial_23_full_df, building_usage, building_metrics, building_compliance, 2023, True)
    ind_part_23_miss_df = create_energy_data(partial_23_miss_df, building_usage, building_metrics, building_compliance, 2023, True)
    ind_part_24_full_df = create_energy_data(partial_24_full_df, building_usage, building_metrics, building_compliance, 2024, True)
    ind_part_24_miss_df = create_energy_data(partial_24_miss_df, building_usage, building_metrics, building_compliance, 2024, True)
    ind_part_25_full_df = create_energy_data(partial_25_full_df, building_usage, building_metrics, building_compliance, 2025, True)
    ind_part_25_miss_df = create_energy_data(partial_25_miss_df, building_usage, building_metrics, building_compliance, 2025, True)
    all_partials_data = pd.concat([ind_part_21_full_df,
                                    ind_part_21_miss_df,
                                    ind_part_22_full_df,
                                    ind_part_22_miss_df,
                                    ind_part_23_full_df,
                                    ind_part_23_miss_df,
                                    ind_part_24_full_df,
                                    ind_part_24_miss_df,
                                    ind_part_25_full_df,
                                    ind_part_25_miss_df])

    # Create dataframes to save with the building and their earliest and latest electric billing data
    ind_elec_21_full_df = create_energy_data(elec_21_full_df, building_usage, building_metrics, building_compliance, 2021, False)
    ind_elec_21_miss_df = create_energy_data(elec_21_miss_df, building_usage, building_metrics, building_compliance, 2021, False)
    ind_elec_22_full_df = create_energy_data(elec_22_full_df, building_usage, building_metrics, building_compliance, 2022, False)
    ind_elec_22_miss_df = create_energy_data(elec_22_miss_df, building_usage, building_metrics, building_compliance, 2022, False)
    ind_elec_23_full_df = create_energy_data(elec_23_full_df, building_usage, building_metrics, building_compliance, 2023, False)
    ind_elec_23_miss_df = create_energy_data(elec_23_miss_df, building_usage, building_metrics, building_compliance, 2023, False)
    ind_elec_24_full_df = create_energy_data(elec_24_full_df, building_usage, building_metrics, building_compliance, 2024, False)
    ind_elec_24_miss_df = create_energy_data(elec_24_miss_df, building_usage, building_metrics, building_compliance, 2024, False)
    ind_elec_25_full_df = create_energy_data(elec_25_full_df, building_usage, building_metrics, building_compliance, 2025, False)
    ind_elec_25_miss_df = create_energy_data(elec_25_miss_df, building_usage, building_metrics, building_compliance, 2025, False)
    all_electric_data = pd.concat([ind_elec_21_full_df,
                                    ind_elec_21_miss_df,
                                    ind_elec_22_full_df,
                                    ind_elec_22_miss_df,
                                    ind_elec_23_full_df,
                                    ind_elec_23_miss_df,
                                    ind_elec_24_full_df,
                                    ind_elec_24_miss_df,
                                    ind_elec_25_full_df,
                                    ind_elec_25_miss_df])

    #############################
    # Return the partially electric dataframes for buildings with full data, and those with missing data
    return (all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, 
            ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, 
            ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, 
            ind_part_25_full_df, ind_part_25_miss_df, all_electric_data, 
            ind_elec_21_full_df, ind_elec_21_miss_df, ind_elec_22_full_df, 
            ind_elec_22_miss_df, ind_elec_23_full_df, ind_elec_23_miss_df, 
            ind_elec_24_full_df, ind_elec_24_miss_df, ind_elec_25_full_df, 
            ind_elec_25_miss_df)