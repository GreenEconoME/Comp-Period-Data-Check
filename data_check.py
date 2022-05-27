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
            - Primary Property Type - Self Selected
    - Creating the Zoho report:
        - Run and export report titled Buildings Currently Benchmarking for EBEWE
    - About:
        - Building is considered to have full data if it has energy data entries for all months of the comparative period, or all months of comparative period to present.
        - Buildings contained in the generated datasets are buildings that we are currently benchmarking for EBEWE. 
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
    workbook, building_usage, all_partials_data, ind_part_21_full_df, ind_part_21_miss_df, ind_part_22_full_df, ind_part_22_miss_df, ind_part_23_full_df, ind_part_23_miss_df, ind_part_24_full_df, ind_part_24_miss_df, ind_part_25_full_df, ind_part_25_miss_df, all_electric_data, ind_elec_21_full_df, ind_elec_21_miss_df, ind_elec_22_full_df, ind_elec_22_miss_df, ind_elec_23_full_df, ind_elec_23_miss_df, ind_elec_24_full_df, ind_elec_24_miss_df, ind_elec_25_full_df, ind_elec_25_miss_df = run_etl()
    etl_has_ran = True

# Once the etl has ran, display a download button and display data
if etl_has_ran:
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
        # Useing a selectbox, determine to view partially or fully electric buildings
        part_or_full = st.selectbox('Choose to view partially electric, or fully electric buildings', 
                                        options = [x for x in all_datasets.keys()])
        # Using the selectbox dropdowns, get the dataframe and building to plot
        dataset_choice = st.selectbox('Choose a Dataset', 
                                        options = [x for x in all_datasets[part_or_full].keys()], 
                                        key = 'dataset')

        building_choice = st.selectbox('Choose a building', 
                                        options = all_datasets[part_or_full][dataset_choice]['Property Name'], 
                                        key = 'building')
        
        # Plot the chosen building
        st.plotly_chart(plot_kbtu_data(building_usage, building_choice, part_or_full), use_container_width = True)

        # Display the earliest and latest data for the selected building
        # If viewing partially electric buildings, display earliest/latest gas/electric dates
        if part_or_full == 'Partially Electric Buildings':
            col1, col2, col3, col4 = st.columns(4)
            col1.metric('Earliest Gas', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Earliest Gas Data'].item())
            col2.metric('Latest Gas', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Latest Gas Data'].item())
            col3.metric('Earliest Electric', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Earliest Electric Data'].item())
            col4.metric('Latest Electric', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Latest Electric Data'].item())
        
        # If viewing fully electric buildings, display earliest/latest electric dates
        else:
            col1, col2 = st.columns(2)
            col1.metric('Earliest Electric', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Earliest Electric Data'].item())
            col2.metric('Latest Electric', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Latest Electric Data'].item())

        # If viewing a completed compliance period, display the EBEWE Exemption metrics
        if dataset_choice in (['Compliance Year 2021 Full Data', 'Compliance Year 2021 Missing Data',
                                'Compliance Year 2022 Full Data', 'Compliance Year 2022 Missing Data']):
            es1, es2, es3 = st.columns(3)
            es1.metric('Recent ES Score', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Energy Star Score'].item())
            es2.metric('Recent ES Score Year Ending', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'ES Score Year Ending'].item())
            es3.metric('Primary Use Type', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Primary Property Type'].item())
            exem1, exem2, exem3, exem4 = st.columns(4)
            exem1.metric('Best EUI Shift', f"{all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Best EUI Shift %'].item()}%")
            exem2.metric('Best EUI Shift Year', f"{all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Best EUI Shift Year'].item()}")
            exem3.metric('Best WUI Shift', f"{all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Best WUI Shift %'].item()}%")
            exem4.metric('Best WUI Shift Year', f"{all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Best WUI Shift Year'].item()}")
            
        else:
            es1, es2, es3 = st.columns(3)
            es1.metric('Recent ES Score', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Energy Star Score'].item())
            es2.metric('Recent ES Score Year Ending', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'ES Score Year Ending'].item())
            es3.metric('Primary Use Type', all_datasets[part_or_full][dataset_choice].loc[all_datasets[part_or_full][dataset_choice]['Property Name'] == building_choice, 'Primary Property Type'].item())
        # Display the selected dataframe
        st.markdown(f'<h3>{dataset_choice}:<h3>', 
                    unsafe_allow_html = True)
        st.dataframe(all_datasets[part_or_full][dataset_choice])
    # If there are no buildings within the selected dataframe, return an explanation
    except Exception as e:
        st.write(e)
        st.write('There are no properties in this dataset')

