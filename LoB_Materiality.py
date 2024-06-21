import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_state(self):
        return self.__dict__

    @staticmethod
    def get(**kwargs):
        if not hasattr(SessionState, "_instance"):
            SessionState._instance = SessionState(**kwargs)
        return SessionState._instance

def main():
    st.set_page_config(page_title="ESG Risk Materiality Assessment Narrative Tool", layout="wide")

    # Initialize session state
    session_state = SessionState.get()

    # Display the introductory text and disclaimer
    display_intro_and_disclaimer()

    # Display ESG Risk Materiality Assessment Narrative Tool
    materiality_assessment(session_state)

def display_intro_and_disclaimer():
    st.title("ESG Risk Materiality Assessment Narrative Tool")
    
    intro_text = """
    This tool, ESG Risk Materiality Assessment Narrative Tool, provides functionality for (re)insurers to perform ESG risk materiality assessments reflecting requirements and guidelines by EIOPA. The tool supports identifying the activities that are related to ESG risk factors with a focus on climate and social aspects. The governance aspect is under development. The aim is to gauge the materiality of activities prone to ESG risks and pick up on the material risks for the quantitative analysis as required by the regulatory basis for the ORSA process. After materiality assessment, the tool suggests performing quantification using scenario narratives based on either NGFS, RCP, or even tailor-made scenarios. This tool helps CROs and risk experts perform bottom-up materiality assessments.
    """
    st.write(intro_text)
    
    disclaimer_text = """
    **Disclaimer:**
    
    The tool does not necessarily reflect the views of regulatory authorities and should not be considered comprehensive regulatory guidance. The information within this tool has been produced by the industry for the industry's use. The recommendations provided are not intended to constitute financial or professional advice and should not be relied upon as such.
    
    For those interested in more detailed information about the NGFS scenarios, please refer to the [NGFS scenario portal](https://www.ngfs.net/ngfs-scenarios-portal/).
    """
    st.write(disclaimer_text)

def materiality_assessment(session_state):
    st.header("Materiality Assessment Questionnaire")

    # Call Section 1 function
    section_1_insurance_activities(session_state)

    # Call Section 2 function
    section_2_exposure_information(session_state)

def section_1_insurance_activities(session_state):
    # Define the CSV data as a multiline string (assuming it's unchanged)
    csv_data = """Lines of Business,Short Name,Transition Risk Factor,Physical Risk Factor,Exposure,Explanation
Medical expenses,ME,1,2,Low,"Transition Risk: Low as medical underwriting is less impacted by climate policies. Physical Risk: Moderate due to increased health claims from heatwaves, diseases, etc. caused by climate change."
Worker compensation,WC,2,2,Medium,"Transition Risk: Moderate due to changes in workplace safety regulations and standards. Physical Risk: Moderate due to increased workplace injuries from extreme weather."
Income protection,IP,1,2,Low,"Transition Risk: Low as employment shifts are less affected by climate policies. Physical Risk: Moderate due to long-term health impacts from climate change affecting work capacity."
Miscellaneous financial loss,MISC,1,1,Low,"Transition Risk: Low since miscellaneous financial loss policies are less affected by climate policies. Physical Risk: Low as financial loss underwriting has limited direct physical impact from climate change."
Motor vehicle insurance,MTPL,2,3,High,"Transition Risk: Moderate due to the transition to electric vehicles and new regulations. Physical Risk: High due to increased claims from weather-related accidents and damages."
Other motor insurance,MOI,2,3,High,"Transition Risk: Similar to motor vehicle insurance with moderate impact. Physical Risk: High due to similar reasons, with higher risk of accidents and damage from extreme weather."
General liability insurance,GTPL,3,2,Medium,"Transition Risk: High as liability for environmental damage and stricter regulations increase. Physical Risk: Moderate as businesses may face claims related to climate impacts."
Assistance,ASS,1,2,Low,"Transition Risk: Low impact on underwriting as service models adapt. Physical Risk: Moderate due to increased demand for assistance during extreme events."
"Marine, aviation and transport insurance",MAT,3,3,High,"Transition Risk: High due to significant regulatory changes in these sectors. Physical Risk: High due to susceptibility to severe weather events and long-term climate impacts on these modes of transport."
Fire and other damage to property insurance,FIRE,3,3,High,"Transition Risk: High as underwriting is impacted by changing building regulations and property values. Physical Risk: High due to increased risk of fires, floods, and other climate-related damages"
"""

    # Read the CSV from the multiline string
    df = pd.read_csv(io.StringIO(csv_data.strip()))

    # Initialize an empty list to store updated materiality values
    exposure_materiality = []

    st.write("### 1. Insurance Activities - Exposure Information")

    # Define the width ratio for the legend and table sections
    legend_width = 0.6  # Width ratio for legend
    table_width = 0.2   # Width ratio for table

    # Create a layout using st.columns to divide the page
    columns = st.columns([legend_width, table_width])

    # Column 1: Table layout for exposures
    with columns[0]:
        # Create a table layout for exposures
        exp_cols = st.columns([0.1, 1, 1])  # Column layout for index, LoB names, and dropdowns
        exp_cols[0].write("**#**")
        exp_cols[1].write("**Line of Business (LoB)**")
        exp_cols[2].write("**LoB Exposure as Share of Total Net Premium**")

        exposure_materiality = []

        for idx, row in df.iterrows():
            exp_cols = st.columns([0.1, 1, 1])
            exp_cols[0].write(f"**{idx+1}**")
            exp_cols[1].write(row['Lines of Business'])
            materiality = exp_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"materiality_{idx}", help=f"Select exposure level for {row['Lines of Business']}", label_visibility="collapsed")
            exposure_materiality.append(materiality)

    # Column 2: Legend for materiality definitions
    with columns[1]:
        with st.container():
            st.markdown("Legend: Exposure Share Definition") 
            st.markdown("- **Low:** Less than 10%")
            st.markdown("- **Medium:** Between 10% and 30%")
            st.markdown("- **High:** More than 30%")
        
    # Update the DataFrame with the selected exposure materiality
    df['Exposure Materiality'] = exposure_materiality

    # Filter out rows where exposure materiality is "Not relevant/No exposure"
    df_filtered = df[df['Exposure Materiality'] != "Not relevant/No exposure"].copy()

    # Calculate average risk factors based on exposure materiality
    df_filtered['Physical Risk Result'] = df_filtered.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + 1 + row['Physical Risk Factor']) / 2, axis=1)
    df_filtered['Transitional Risk Result'] = df_filtered.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + 1 + row['Transition Risk Factor']) / 2, axis=1)

    # Display the heatmap and final table
    st.write("### Heatmap and Results")

    # Create a reactive plot using streamlit's st.pyplot
    create_gradient_heatmap(df_filtered)

    st.header("Risk Factor Table")
    df_display = df_filtered.copy()
    df_display['Explanation'] = df_filtered['Explanation']
    st.write(df_display)

def section_2_exposure_information(session_state):
    # Section 2.1: Asset Allocation
    st.header("2. Insurance Activities - Exposure Information")
    st.subheader("2.1 Asset Allocation")

    # Define the asset allocation data as a list of dictionaries
    asset_data = [
        {"Asset class": "Bonds", "Exposure": ""},
        {"Asset class": "Equity", "Exposure": ""},
        {"Asset class": "Property", "Exposure": ""},
        {"Asset class": "Loans", "Exposure": ""},
        {"Asset class": "Holdings in related undertakings, including participations", "Exposure": ""},
        {"Asset class": "Collective investment taking", "Exposure": ""},
        {"Asset class": "Other assets", "Exposure": ""}
    ]

    # Convert the asset data to a DataFrame
    asset_df = pd.DataFrame(asset_data)

    # Initialize an empty list to store updated asset exposure values
    asset_exposure_values = []

    st.write("### Asset Allocation Exposure Information")

    # Define the width ratio for the legend and table sections
    legend_width = 0.6  # Width ratio for legend
    table_width = 0.2   # Width ratio for table

    # Create a layout using st.columns to divide the page
    columns = st.columns([legend_width, table_width])

    # Column 1: Table layout for exposures
    with columns[0]:
        # Create a table layout for exposures
        exp_cols = st.columns([0.1, 1, 1])  # Column layout for index, asset class, and dropdowns
        exp_cols[0].write("**#**")
        exp_cols[1].write("**Asset Class**")
        exp_cols[2].write("**Asset Exposure as Share of Total Net Assets**")

        for idx, row in asset_df.iterrows():
            exp_cols = st.columns([0.1, 1, 1])
            exp_cols[0].write(f"**{idx+1}**")
            exp_cols[1].write(row['Asset class'])
            exposure = exp_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"asset_exposure_{idx}", help=f"Select exposure level for {row['Asset class']}", label_visibility="collapsed")
            asset_exposure_values.append(exposure)

    # Column 2: Legend for asset exposure definitions
    with columns[1]:
        with st.container():
            st.markdown("Legend: Asset Exposure Share Definition") 
            st.markdown("- **Low:** Less than 10%")
            st.markdown("- **Medium:** Between 10% and 30%")
            st.markdown("- **High:** More than 30%")
        
    # Update the DataFrame with the selected asset exposure values
    asset_df['Exposure'] = asset_exposure_values

    # Filter out rows where exposure is "Not relevant/No exposure"
    asset_df_filtered = asset_df[asset_df['Exposure'] != "Not relevant/No exposure"].copy()

    st.write("### Asset Exposure Results")

    # Display the final asset exposure table
    st.write(asset_df_filtered)

    # Section 2.2: Sectoral and Regional Breakdown
    st.subheader("2.2 Sectoral and Regional Breakdown")
    
    # Define the sectoral and regional breakdown data as a list of dictionaries
    sectoral_data = [
        {"Sector": "Energy", "Regional Exposure": ""},
        {"Sector": "Utilities", "Regional Exposure": ""},
        {"Sector": "Materials", "Regional Exposure": ""},
        {"Sector": "Industrials", "Regional Exposure": ""},
        {"Sector": "Consumer Discretionary", "Regional Exposure": ""},
        {"Sector": "Consumer Staples", "Regional Exposure": ""},
        {"Sector": "Healthcare", "Regional Exposure": ""},
        {"Sector": "Financials", "Regional Exposure": ""},
        {"Sector": "Information Technology", "Regional Exposure": ""},
        {"Sector": "Telecommunication Services", "Regional Exposure": ""},
        {"Sector": "Real Estate", "Regional Exposure": ""}
    ]

    # Convert the sectoral data to a DataFrame
    sectoral_df = pd.DataFrame(sectoral_data)

    # Initialize an empty list to store updated sectoral exposure values
    sectoral_exposure_values = []

    st.write("### Sectoral and Regional Exposure Information")

    # Define the width ratio for the legend and table sections
    legend_width = 0.6  # Width ratio for legend
    table_width = 0.2   # Width ratio for table

    # Create a layout using st.columns to divide the page
    columns = st.columns([legend_width, table_width])

    # Column 1: Table layout for exposures
    with columns[0]:
        # Create a table layout for exposures
        exp_cols = st.columns([0.1, 1, 1])  # Column layout for index, sector, and dropdowns
        exp_cols[0].write("**#**")
        exp_cols[1].write("**Sector**")
        exp_cols[2].write("**Regional Exposure as Share of Total Sectoral Exposure**")

        for idx, row in sectoral_df.iterrows():
            exp_cols = st.columns([0.1, 1, 1])
            exp_cols[0].write(f"**{idx+1}**")
            exp_cols[1].write(row['Sector'])
            exposure = exp_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"sectoral_exposure_{idx}", help=f"Select exposure level for {row['Sector']}", label_visibility="collapsed")
            sectoral_exposure_values.append(exposure)

    # Column 2: Legend for sectoral exposure definitions
    with columns[1]:
        with st.container():
            st.markdown("Legend: Regional Exposure Share Definition") 
            st.markdown("- **Low:** Less than 10%")
            st.markdown("- **Medium:** Between 10% and 30%")
            st.markdown("- **High:** More than 30%")
        
    # Update the DataFrame with the selected sectoral exposure values
    sectoral_df['Regional Exposure'] = sectoral_exposure_values

    # Filter out rows where exposure is "Not relevant/No exposure"
    sectoral_df_filtered = sectoral_df[sectoral_df['Regional Exposure'] != "Not relevant/No exposure"].copy()

    st.write("### Sectoral Exposure Results")

    # Display the final sectoral exposure table
    st.write(sectoral_df_filtered)

def create_gradient_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Define the color gradient
    colors = ["#00FF00", "#FFFF00", "#FF0000"]  # Green, Yellow, Red
    cmap = LinearSegmentedColormap.from_list("green_yellow_red", colors, N=256)

    heatmap_data = df[["Physical Risk Result", "Transitional Risk Result"]].values

    cax = ax.matshow(heatmap_data, cmap=cmap, vmin=1, vmax=3)

    for i in range(len(df)):
        for j in range(2):
            ax.text(x=j, y=i, s=f"{heatmap_data[i, j]:.2f}", va='center', ha='center', color='black')

    plt.xticks(range(2), ["Physical Risk Result", "Transitional Risk Result"], rotation=45)
    plt.yticks(range(len(df)), df['Short Name'])
    plt.colorbar(cax)

    st.pyplot(fig)

if __name__ == "__main__":
    main()
