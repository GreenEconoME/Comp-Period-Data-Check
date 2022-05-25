import pandas as pd
from io import BytesIO
import streamlit as st

def create_workbook(complete_and_missing_dfs_by_CY):
    (all_partials_data, 
    ind_part_21_full_df, 
    ind_part_21_miss_df, 
    ind_part_22_full_df, 
    ind_part_22_miss_df, 
    ind_part_23_full_df, 
    ind_part_23_miss_df, 
    ind_part_24_full_df, 
    ind_part_24_miss_df, 
    ind_part_25_full_df, 
    ind_part_25_miss_df, 
    all_electric_data, 
    ind_elec_21_full_df, 
    ind_elec_21_miss_df, 
    ind_elec_22_full_df, 
    ind_elec_22_miss_df, 
    ind_elec_23_full_df, 
    ind_elec_23_miss_df, 
    ind_elec_24_full_df, 
    ind_elec_24_miss_df, 
    ind_elec_25_full_df, 
    ind_elec_25_miss_df) = complete_and_missing_dfs_by_CY

    data = BytesIO()
    with pd.ExcelWriter(data) as writer:
        # Adding the partially electric buildings
        all_partials_data.to_excel(writer, sheet_name = 'All Partial Electric Data', index = False)
        ind_part_21_full_df.to_excel(writer, sheet_name = 'Part E CY 21 Full Data', index = False)
        ind_part_21_miss_df.to_excel(writer, sheet_name = 'Part E CY 21 Missing Data', index = False)
        ind_part_22_full_df.to_excel(writer, sheet_name = 'Part E CY 22 Full Data', index = False)
        ind_part_22_miss_df.to_excel(writer, sheet_name = 'Part E CY 22 Missing Data', index = False)
        ind_part_23_full_df.to_excel(writer, sheet_name = 'Part E CY 23 Full Data', index = False)
        ind_part_23_miss_df.to_excel(writer, sheet_name = 'Part E CY 23 Missing Data', index = False)
        ind_part_24_full_df.to_excel(writer, sheet_name = 'Part E CY 24 Full Data', index = False)
        ind_part_24_miss_df.to_excel(writer, sheet_name = 'Part E CY 24 Missing Data', index = False)
        ind_part_25_full_df.to_excel(writer, sheet_name = 'Part E CY 25 Full Data', index = False)
        ind_part_25_miss_df.to_excel(writer, sheet_name = 'Part E CY 25 Missing Data', index = False)
        
        # Adding the fully electric buildings
        all_electric_data.to_excel(writer, sheet_name = 'All Fully Electric Data', index = False)
        ind_elec_21_full_df.to_excel(writer, sheet_name = 'Fully E CY 21 Full Data', index = False)
        ind_elec_21_miss_df.to_excel(writer, sheet_name = 'Fully E CY 21 Missing Data', index = False)
        ind_elec_22_full_df.to_excel(writer, sheet_name = 'Fully E CY 22 Full Data', index = False)
        ind_elec_22_miss_df.to_excel(writer, sheet_name = 'Fully E CY 22 Missing Data', index = False)
        ind_elec_23_full_df.to_excel(writer, sheet_name = 'Fully E CY 23 Full Data', index = False)
        ind_elec_23_miss_df.to_excel(writer, sheet_name = 'Fully E CY 23 Missing Data', index = False)
        ind_elec_24_full_df.to_excel(writer, sheet_name = 'Fully E CY 24 Full Data', index = False)
        ind_elec_24_miss_df.to_excel(writer, sheet_name = 'Fully E CY 24 Missing Data', index = False)
        ind_elec_25_full_df.to_excel(writer, sheet_name = 'Fully E CY 25 Full Data', index = False)
        ind_elec_25_miss_df.to_excel(writer, sheet_name = 'Fully E CY 25 Missing Data', index = False)

    workbook = data.getvalue()
    return workbook