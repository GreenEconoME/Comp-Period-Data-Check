# Import dependencies
import streamlit as st
import pandas as pd
from Utilities.clean_data import clean_data
from Utilities.process_part_elec import process_part_elec
from Utilities.create_workbook import create_workbook
from Utilities.plot_kbtu_data import plot_kbtu_data

# Set config to have a wide layout
st.set_page_config(layout = 'wide')

# Add title and instructions
st.title('EBEWE Data Check')
st.sidebar.markdown('''
    <h1>Notes:</h1>
    Use the following instructions to gather the data in ESPM and Zoho to upload.

    - Creating the ESPM report:
        - Template used previously titled EBEWE Data Check
        - Select Timeframe:
            - Yearly: From Dec 31, 2015 to May 31, 2022
        - Select Properties:
            - Select all properties
        - Select Information and Metrics
            - Los Angeles Building ID
            - Electricity Use (Grid) - Monthly (kBtu)
            - Natural Gas Use - Monthly (kBtu)
            - Percent Electricity
    - Creating the Zoho report:
        - Run and export report titled Buildings Currently Benchmarking for EBEWE
    - About:
        - Building is considered to have full data if it has gas entries for all months of the comparative period, or all months of comparative period to present.
        - Buildings contained in the generated datasets are buildings that we are currently benchmarking for EBEWE.
''', unsafe_allow_html = True)

espm_report = st.file_uploader('Upload EBEWE Data Check ESPM Report')
zoho_report = st.file_uploader('Upload Current EBEWE Opp Zoho Report')

@st.experimental_memo()
def run_etl():
    if espm_report and zoho_report is not None:
        building_metrics = pd.read_excel(espm_report, 
                                        sheet_name = 'Information and Metrics',
                                        skiprows = 5)
        
        building_usage = pd.read_excel(espm_report,
                                        sheet_name = 'Monthly Usage',
                                        skiprows = 4)

        current_ebewe = pd.read_excel(zoho_report, 
                                        skiprows = 1)

        # Clean the loaded reports
        building_metrics, building_usage = clean_data(building_metrics, building_usage, current_ebewe)
        
        # Create the processed partially electric dataframes
        all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df = process_part_elec(building_metrics, building_usage)

        # Create a workbook to download for the partially electric buildings
        workbook = create_workbook(process_part_elec(building_metrics, building_usage))

        return workbook, building_usage, all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df

# Run the etl funciton and return the dataframes that will be used to graph usage
# Set a boolean to prevent undefined errors prior to running the etl
etl_has_ran = False
if espm_report and zoho_report is not None:
    workbook, building_usage, all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df = run_etl()
    etl_has_ran = True

# Once the etl has ran, display a download button and display data
if etl_has_ran:
    # Display a download for the created workbook
    st.download_button(label = 'Click to Download the Partially Electric Buildings by CY', 
                                data = workbook,
                                file_name = 'Partial Electric Building Energy Data by CY.xlsx')

    partial_dfs = {'All Partial Electric Buildings' : all_partials_data, 
                    'Compliance Year 2021 Full Data' : ind_part_21_full_df, 
                    'Compliance Year 2021 Missing Data' : ind_part_21_miss_df,
                    'Compliance Year 2022 Full Data' : ind_part_22_full_df, 
                    'Compliance Year 2022 Missing Data' : ind_part_22_miss_df,
                    'Compliance Year 2023 Full Data' : ind_part_23_full_df, 
                    'Compliance Year 2023 Missing Data' : ind_part_23_miss_df,
                    'Compliance Year 2024 Full Data' : ind_part_24_full_df, 
                    'Compliance Year 2024 Missing Data' : ind_part_24_miss_df,
                    'Compliance Year 2025 Full Data' : ind_part_25_full_df, 
                    'Compliance Year 2025 Missing Data' : ind_part_25_miss_df}

    try:
        # Using the selectbox dropdowns, get the dataframe and building to plot
        dataset_choice = st.selectbox('Choose a Dataset', 
                                        options = [x for x in partial_dfs.keys()], 
                                        key = 'dataset')

        building_choice = st.selectbox('Choose a building', 
                                        options = partial_dfs[dataset_choice]['Property Name'], 
                                        key = 'building')
        # Plot the chosen building
        st.plotly_chart(plot_kbtu_data(building_usage, building_choice), use_container_width = True)

        # Display information on the selected building
        col1, col2 = st.columns(2)
        col1.metric('Earliest Gas', partial_dfs[dataset_choice].loc[partial_dfs[dataset_choice]['Property Name'] == building_choice, 'Earliest Gas Data'].item())
        col2.metric('Latest Gas', partial_dfs[dataset_choice].loc[partial_dfs[dataset_choice]['Property Name'] == building_choice, 'Latest Gas Data'].item())

        # Display the selected dataframe
        st.markdown(f'<h3>{dataset_choice}:<h3>', 
                    unsafe_allow_html = True)
        st.dataframe(partial_dfs[dataset_choice])

    # If there are no buildings within the selected dataframe, return an explanation
    except KeyError:
        st.write('There are no properties in this dataset')

