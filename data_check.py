# Import dependencies
import streamlit as st
import pandas as pd
from Utilities.clean_data import clean_data
from Utilities.process_part_full_elec import process_part_full_elec
from Utilities.create_workbook import create_workbook
from Utilities.plot_kbtu_data import plot_kbtu_data

# Set config to have a wide layout
st.set_page_config(layout = 'wide')

# Add title and instructions
st.title('EBEWE Data Check')
st.sidebar.markdown('''
    <h1>Notes:</h1>
    Use the following instructions to gather the data in ESPM and Zoho to upload.

    - The app takes three datasets which can be found in the ESPM Reports and Zoho Reports titled: 
        - EBEWE Data Check W Compliance Metrics
        - EBEWE Data Check W Energy
        - Buildings Currently Benchmarking for EBEWE
    - Creating the ESPM reports:
        - EBEWE Data Check W Compliance Metrics
            - Select Timeframe:
                - Date Range - Yearly: From Dec 31, 2016 to May 31, 2021
            - Select Properties:
                - Select all properties
            - Select Information and Metrics
                - Los Angeles Building ID
                - ENERGY STAR Score
                - Weather Normalized Source EUI (kBtu/ft²)
                - Water Use Intensity (All Water Sources) (gal/ft²)
        - EBEWE Data Check W Energy
            - Select Timeframe:
                - Date Range - Yearly: From Dec 31, 2015 to May 31, 2022 (or current month)
            - Select Properties:
                - Select all properties
            - Select Information and Metrics
                - Los Angeles Building ID
                - Electricity Use (Grid) - Monthly (kBtu)
                - Natural Gas Use - Monthly (kBtu)
                - Percent Electricity
                - Primary Property Type - Self Selected
    - Creating the Zoho report:
        - Run and export report titled Buildings Currently Benchmarking for EBEWE
    - About:
        - Building is considered to have full data if it has energy data entries for all months of the comparative period if comparative period is completed, or all months of comparative period to present otherwise.
        - Buildings contained in the generated datasets are buildings that we are currently contracted for EBEWE related opportunities. 
        - Partially electric buildings have both electric and gas.
        - Fully electric buildings have only electric.
        - Buildings without any energy data are not included.
''', unsafe_allow_html = True)

espm_compliance = st.file_uploader('Upload EBEWE Data Check With Compliance Metrics ESPM Report')
espm_energy = st.file_uploader('Upload EBEWE Data Check With Energy ESPM Report')
zoho_report = st.file_uploader('Upload Current EBEWE Opp Zoho Report')

@st.cache
def run_etl():
    if espm_compliance and espm_energy and zoho_report is not None:
        building_metrics = pd.read_excel(espm_energy, 
                                        sheet_name = 'Information and Metrics',
                                        skiprows = 5)
        
        building_usage = pd.read_excel(espm_energy,
                                        sheet_name = 'Monthly Usage',
                                        skiprows = 4)

        building_compliance = pd.read_excel(espm_compliance, 
                                            sheet_name = 'Information and Metrics',
                                            skiprows = 5)

        current_ebewe = pd.read_excel(zoho_report, 
                                        skiprows = 1)

        # Clean the loaded reports
        building_metrics, building_usage, building_compliance = clean_data(building_metrics, 
                                                                            building_usage,
                                                                            building_compliance, 
                                                                            current_ebewe)
        
        # Create the processed partially electric dataframes
        (all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, 
        ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, 
        ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, 
        ind_part_25_full_df, ind_part_25_miss_df, all_electric_data, 
        ind_elec_21_full_df, ind_elec_21_miss_df, ind_elec_22_full_df, 
        ind_elec_22_miss_df, ind_elec_23_full_df, ind_elec_23_miss_df, 
        ind_elec_24_full_df, ind_elec_24_miss_df, ind_elec_25_full_df, 
        ind_elec_25_miss_df) = process_part_full_elec(building_metrics, building_usage, building_compliance)

        # Create a workbook to download for the partially electric buildings
        workbook = create_workbook(all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, 
                                    ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, 
                                    ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, 
                                    ind_part_25_full_df, ind_part_25_miss_df, all_electric_data, 
                                    ind_elec_21_full_df, ind_elec_21_miss_df, ind_elec_22_full_df, 
                                    ind_elec_22_miss_df, ind_elec_23_full_df, ind_elec_23_miss_df, 
                                    ind_elec_24_full_df, ind_elec_24_miss_df, ind_elec_25_full_df, 
                                    ind_elec_25_miss_df)

        return (workbook, building_usage, all_partials_data, 
                ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, 
                ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, 
                ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, 
                ind_part_25_miss_df, all_electric_data, ind_elec_21_full_df, 
                ind_elec_21_miss_df, ind_elec_22_full_df, ind_elec_22_miss_df, 
                ind_elec_23_full_df, ind_elec_23_miss_df, ind_elec_24_full_df, 
                ind_elec_24_miss_df, ind_elec_25_full_df, ind_elec_25_miss_df)

# Run the etl funciton and return the dataframes that will be used to graph usage
# Set a boolean to prevent undefined errors prior to running the etl
etl_has_ran = False
if espm_compliance and espm_energy and zoho_report is not None:
    (workbook, building_usage, all_partials_data, 
    ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, 
    ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, 
    ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, 
    ind_part_25_miss_df, all_electric_data, ind_elec_21_full_df, 
    ind_elec_21_miss_df, ind_elec_22_full_df, ind_elec_22_miss_df, 
    ind_elec_23_full_df, ind_elec_23_miss_df, ind_elec_24_full_df, 
    ind_elec_24_miss_df, ind_elec_25_full_df, ind_elec_25_miss_df) = run_etl()
    etl_has_ran = True

# Once the etl has ran, display a download button and display data
if etl_has_ran:

    st.markdown('<h3>Download the processed workbook here:<h3>', unsafe_allow_html = True)
    # Display a download for the created workbook
    st.download_button(label = 'Click to Download the Partially and Fully Electric Buildings by CY', 
                                data = workbook,
                                file_name = 'Building Energy Data by CY.xlsx')

    all_datasets = {'Partially Electric Buildings' : {'All Partial Electric Buildings' : all_partials_data, 
                                                        'Compliance Year 2021 Full Data' : ind_part_21_full_df, 
                                                        'Compliance Year 2021 Missing Data' : ind_part_21_miss_df,
                                                        'Compliance Year 2022 Full Data' : ind_part_22_full_df, 
                                                        'Compliance Year 2022 Missing Data' : ind_part_22_miss_df,
                                                        'Compliance Year 2023 Full Data' : ind_part_23_full_df, 
                                                        'Compliance Year 2023 Missing Data' : ind_part_23_miss_df,
                                                        'Compliance Year 2024 Full Data' : ind_part_24_full_df, 
                                                        'Compliance Year 2024 Missing Data' : ind_part_24_miss_df,
                                                        'Compliance Year 2025 Full Data' : ind_part_25_full_df, 
                                                        'Compliance Year 2025 Missing Data' : ind_part_25_miss_df}, 
                    'Fully Electric Buildings' : {'All Fully Electric Buildings' : all_electric_data, 
                                                        'Compliance Year 2021 Full Data' : ind_elec_21_full_df, 
                                                        'Compliance Year 2021 Missing Data' : ind_elec_21_miss_df,
                                                        'Compliance Year 2022 Full Data' : ind_elec_22_full_df, 
                                                        'Compliance Year 2022 Missing Data' : ind_elec_22_miss_df,
                                                        'Compliance Year 2023 Full Data' : ind_elec_23_full_df, 
                                                        'Compliance Year 2023 Missing Data' : ind_elec_23_miss_df,
                                                        'Compliance Year 2024 Full Data' : ind_elec_24_full_df, 
                                                        'Compliance Year 2024 Missing Data' : ind_elec_24_miss_df,
                                                        'Compliance Year 2025 Full Data' : ind_elec_25_full_df, 
                                                        'Compliance Year 2025 Missing Data' : ind_elec_25_miss_df}
                    }

    try:
        # Using a selectbox, determine to view partially or fully electric buildings
        part_or_full = st.selectbox('Choose to view partially electric, or fully electric buildings', 
                                        options = [x for x in all_datasets.keys()])

        # Using the selectbox dropdowns, get the dataframe and building to plot
        dataset_choice = st.selectbox('Choose a Dataset', 
                                        options = [x for x in all_datasets[part_or_full].keys()], 
                                        key = 'dataset')

        # Define a variable to hold the selected data
        selected_data = all_datasets[part_or_full][dataset_choice]

        # Using a selectbox, get the building choice
        building_choice = st.selectbox('Choose a building', 
                                        options = selected_data['Property Name'], 
                                        key = 'building')
        
        # Plot the chosen building
        st.plotly_chart(plot_kbtu_data(building_usage, building_choice, part_or_full), use_container_width = True)

        # Define used metrics
        earliest_gas = selected_data.loc[selected_data['Property Name'] == building_choice, 'Earliest Gas Data'].item()
        latest_gas = selected_data.loc[selected_data['Property Name'] == building_choice, 'Latest Gas Data'].item()
        earliest_electric = selected_data.loc[selected_data['Property Name'] == building_choice, 'Earliest Electric Data'].item()
        latest_electric = selected_data.loc[selected_data['Property Name'] == building_choice, 'Latest Electric Data'].item()
        es_score_metric = f"{selected_data.loc[selected_data['Property Name'] == building_choice, 'Energy Star Score'].item():.0f}"
        es_score_year_metric = selected_data.loc[selected_data['Property Name'] == building_choice, 'ES Score Year Ending'].item()
        primary_use_type = selected_data.loc[selected_data['Property Name'] == building_choice, 'Primary Property Type'].item()
        best_eui_shift = f"{selected_data.loc[selected_data['Property Name'] == building_choice, 'Best EUI Shift %'].item()}%"
        best_eui_shift_year = f"{selected_data.loc[selected_data['Property Name'] == building_choice, 'Best EUI Shift Year'].item()}"
        best_wui_shift = f"{selected_data.loc[selected_data['Property Name'] == building_choice, 'Best WUI Shift %'].item()}%"
        best_wui_shift_year = f"{selected_data.loc[selected_data['Property Name'] == building_choice, 'Best WUI Shift Year'].item()}"


        # Display the earliest and latest data for the selected building
        # If viewing partially electric buildings, display earliest/latest gas/electric dates
        if part_or_full == 'Partially Electric Buildings':
            col1, col2, col3, col4 = st.columns(4)
            col1.metric('Earliest Gas', earliest_gas)
            col2.metric('Latest Gas', latest_gas)
            col3.metric('Earliest Electric', earliest_electric)
            col4.metric('Latest Electric', latest_electric)
        
        # If viewing fully electric buildings, display earliest/latest electric dates
        else:
            col1, col2 = st.columns(2)
            col1.metric('Earliest Electric', earliest_electric)
            col2.metric('Latest Electric', latest_electric)

        # If viewing a completed compliance period, display the EBEWE Exemption metrics
        if dataset_choice in (['Compliance Year 2021 Full Data', 'Compliance Year 2021 Missing Data',
                                'Compliance Year 2022 Full Data', 'Compliance Year 2022 Missing Data']):
            es1, es2, es3 = st.columns(3)
            es1.metric('Recent ES Score', es_score_metric)
            es2.metric('Recent ES Score Year Ending', es_score_year_metric)
            es3.metric('Primary Use Type', primary_use_type)
            exem1, exem2, exem3, exem4 = st.columns(4)
            exem1.metric('Best EUI Shift', best_eui_shift)
            exem2.metric('Best EUI Shift Year', best_eui_shift_year)
            exem3.metric('Best WUI Shift', best_wui_shift)
            exem4.metric('Best WUI Shift Year', best_wui_shift_year)
            
        else:
            es1, es2, es3 = st.columns(3)
            es1.metric('Recent ES Score', es_score_metric)
            es2.metric('Recent ES Score Year Ending', es_score_year_metric)
            es3.metric('Primary Use Type', selected_data.loc[selected_data['Property Name'] == building_choice, 'Primary Property Type'].item())
        
        # Display the selected dataframe
        st.markdown(f'<h3>{dataset_choice}:<h3>', 
                    unsafe_allow_html = True)

        # Define dataframe styling functions
        # Define styler to color cells that have >=75 Energy Star
        def es_coder(cell_value):
            color = ''
            if cell_value >= 75:
                color = 'green'
            return f'color: {color}'
        # Define styler to color cells with at least a 15% reduction in Weather Normalized Source EUI
        def eui_coder(cell_value):
            color = ''
            if cell_value <= -15:
                color = 'green'
            return f'color: {color}'
        # Define a styler to color cells with at least a 20% reduction in Water Use Intensity
        def wui_coder(cell_value):
            color = ''
            if cell_value <= -20:
                color = 'green'
            return f'color: {color}'
        
        # Display the formatted selected dataframe
        st.dataframe(selected_data.reset_index(drop = True)
                                    .style
                                    .applymap(es_coder, subset = ['Energy Star Score'])
                                    .applymap(eui_coder, subset = ['Best EUI Shift %'])
                                    .applymap(wui_coder, subset = ['Best WUI Shift %'])
                                    .format(formatter = {'Energy Star Score' : '{:.0f}', 
                                                        'Best EUI Shift %' : '{:.2f}', 
                                                        'Best WUI Shift %' : '{:.2f}'}))

    # If there are no buildings within the selected dataframe, return an explanation
    except Exception as e:
        st.write(e)
        st.write('There are no properties in this dataset')

