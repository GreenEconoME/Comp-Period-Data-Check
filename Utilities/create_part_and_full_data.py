import pandas as pd
import numpy as np
import math
import streamlit as st

# Defining a helper function to find the min of a list of tuples based on first element of tuple, and return the second value of tuple
def filter_tuple_list(given_list, target_value):
    for x, y in given_list:
        if x == target_value:
            return y

def create_energy_data(cy_df, usage_df, metrics_df, building_compliance, comp_year, has_gas):
    # Create a list to hold the dictionaries of data fro each property id
    data_list = []
    
    # Iterate through the unique property IDs and create a dictionary contatining the data for each prop id
    for prop_id in cy_df['Property Id'].unique():
        try:
            # Create a dictionary to hold the information for each property
            data = {}
            
            # Gather the property details
            data['Property Id'] = prop_id
            data['Property Name'] = list(cy_df.loc[cy_df['Property Id'] == prop_id, 'Property Name'])[0]
            data['Los Angeles Building ID'] = list(cy_df.loc[cy_df['Property Id'] == prop_id, 'Los Angeles Building ID'])[0]
            data['Primary Property Type'] = list(metrics_df.loc[metrics_df['Property Id'] == prop_id, 'Primary Property Type - Self Selected'])[0]
            
            # Gather the earliest and latest dates for energy data
            data['Earliest Electric Data'] = min(usage_df.loc[(usage_df['Property Id'] == prop_id) &
                                                              ~(usage_df['Electricity Use (Grid)  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
            data['Latest Electric Data'] = max(usage_df.loc[(usage_df['Property Id'] == prop_id) &
                                                              ~(usage_df['Electricity Use (Grid)  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
            
            # If the building is partially electric - gather the gas data
            if has_gas:
                data['Earliest Gas Data'] = min(usage_df.loc[(usage_df['Property Id'] == prop_id) & 
                                                                ~(usage_df['Natural Gas Use  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
                data['Latest Gas Data'] = max(usage_df.loc[(usage_df['Property Id'] == prop_id) & 
                                                               ~(usage_df['Natural Gas Use  (kBtu)'].isna()), 'Month']).strftime('%b, %Y')
            
            # Gather Energy Star Score data
            try:
                # Create masks to filter for the Energy Star Scores
                non_null_es = (building_compliance['Property Id'] == prop_id) & ~(building_compliance['ENERGY STAR Score'].isna())
                recent_non_null = (building_compliance['Year Ending'] == max(building_compliance.loc[non_null_es, 'Year Ending']))

                # Grab the most recent Energy Star score and the corresponding year
                data['Energy Star Score'] = building_compliance.loc[non_null_es & recent_non_null, 'ENERGY STAR Score'].item()
                data['ES Score Year Ending'] = building_compliance.loc[non_null_es & recent_non_null, 'Year Ending'].item().strftime('%Y-%m-%d')

            except:
                data['Energy Star Score'] = np.nan
                data['Year Ending'] = np.nan
                
            # Gather the most EBEWE Compliance data for compliance years 2021 and 2022
            if comp_year in [2021, 2022]:            
                
                # Gather Weather Normalized Source EUI Data
                try:
                    # Create a list to hold the percent changes between EUI for first four years vs last year of comparative period
                    eui_percent_changes = []
                    # Create a mask and gather the WN SEUI for the final year in the comparative period
                    ending_cp = (building_compliance['Property Id'] == prop_id) & (building_compliance['Year Ending'] == f'{comp_year - 1}-12-31')
                    end_cp_eui = building_compliance.loc[ending_cp, 'Weather Normalized Source EUI (kBtu/ft²)'].item()
                    # Cycle through the other comparative years and get the percent change between them and the final year
                    for i in range(2, 6):
                        # Create a mask to get the current comp year's WN SEUI
                        mask = (building_compliance['Property Id'] == prop_id) & (building_compliance['Year Ending'] == f'{comp_year - i}-12-31')

                        try:
                            # Calculate and append the percent change between current comparative year and final year in comparative period
                            comp_year_eui = building_compliance.loc[mask, 'Weather Normalized Source EUI (kBtu/ft²)'].item()
                            percent_change = (end_cp_eui - comp_year_eui) / comp_year_eui
                            eui_percent_changes.append((math.trunc((percent_change * 10000))/100, comp_year - i))
                            
                        except:
                            eui_percent_changes.append((np.nan, np.nan))
                            
                    # Add the best EUI Shift to the property's data
                    data['Best EUI Shift %'] = min(eui_percent_changes, key = lambda x: x[0])[0]
                    data['Best EUI Shift Year'] = str(filter_tuple_list(eui_percent_changes, min(eui_percent_changes, key = lambda x: x[0])[0]))
                    
                except: 
                    data['Best EUI Shift %'] = np.nan
                    data['Best EUI Shift Year'] = np.nan
                
                # Gather Water Use Intensity Data
                try:
                    # Create a list to hold the percent changes between Water Use Intensity for first four years vs last year of comparative period
                    wui_percent_changes = []
                    # Create a mask and gather the Water UI for the final year in the comparative period
                    ending_cp = (building_compliance['Property Id'] == prop_id) & (building_compliance['Year Ending'] == f'{comp_year - 1}-12-31')
                    end_cp_wui = building_compliance.loc[ending_cp, 'Water Use Intensity (All Water Sources) (gal/ft²)'].item()
                    # Cycle through the other comparative years and get the percent change between them and the final year
                    for i in range(2, 6):
                        # Create a mask to get the current comp year's WN SEUI
                        mask = (building_compliance['Property Id'] == prop_id) & (building_compliance['Year Ending'] == f'{comp_year - i}-12-31')

                        try:
                            # Calculate and append the percent change between current comparative year and final year in comparative period
                            comp_year_wui = building_compliance.loc[mask, 'Water Use Intensity (All Water Sources) (gal/ft²)'].item()
                            percent_change = (end_cp_wui - comp_year_wui) / comp_year_wui
                            wui_percent_changes.append((math.trunc((percent_change * 10000))/100, comp_year - i))

                        except ValueError:
                            wui_percent_changes.append((np.nan, np.nan))
                            
                    # Add the best Water UI Shift to the property's data
                    data['Best WUI Shift %'] = min(wui_percent_changes, key = lambda x: x[0])[0]
                    data['Best WUI Shift Year'] = str(filter_tuple_list(wui_percent_changes, min(wui_percent_changes, key = lambda x: x[0])[0]))
                    
                except: 
                    data['Best WUI Shift %'] = np.nan
                    data['Best WUI Shift Year'] = np.nan
                                        
                
            data_list.append(data)
            
        except ValueError:
            pass
            
    building_df = pd.DataFrame.from_dict(data_list)
    
    return building_df

