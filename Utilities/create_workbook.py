import pandas as pd
from io import BytesIO
import streamlit as st

def create_workbook(complete_and_missing_dfs_by_CY):
    (ind_part_21_full_df, 
    ind_part_21_miss_df, 
    ind_part_22_full_df, 
    ind_part_22_miss_df, 
    ind_part_23_full_df, 
    ind_part_23_miss_df, 
    ind_part_24_full_df, 
    ind_part_24_miss_df, 
    ind_part_25_full_df, 
    ind_part_25_miss_df) = complete_and_missing_dfs_by_CY

    data = BytesIO()
    with pd.ExcelWriter(data) as writer:
        ind_part_21_full_df.to_excel(writer, sheet_name = 'CY 21 Full Data', index = False)
        ind_part_21_miss_df.to_excel(writer, sheet_name = 'CY 21 Missing Data', index = False)
        ind_part_22_full_df.to_excel(writer, sheet_name = 'CY 22 Full Data', index = False)
        ind_part_22_miss_df.to_excel(writer, sheet_name = 'CY 22 Missing Data', index = False)
        ind_part_23_full_df.to_excel(writer, sheet_name = 'CY 23 Full Data', index = False)
        ind_part_23_miss_df.to_excel(writer, sheet_name = 'CY 23 Missing Data', index = False)
        ind_part_24_full_df.to_excel(writer, sheet_name = 'CY 24 Full Data', index = False)
        ind_part_24_miss_df.to_excel(writer, sheet_name = 'CY 24 Missing Data', index = False)
        ind_part_25_full_df.to_excel(writer, sheet_name = 'CY 25 Full Data', index = False)
        ind_part_25_miss_df.to_excel(writer, sheet_name = 'CY 25 Missing Data', index = False)

    workbook = data.getvalue()
    return workbook