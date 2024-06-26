import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # Initialize Methodology_Text attribute
        self.Methodology_Text = False  # Set to False initially
    
    def get_state(self):
        return self.__dict__

    @staticmethod
    def get(**kwargs):
        if not hasattr(SessionState, "_instance"):
            SessionState._instance = SessionState(**kwargs)
        return SessionState._instance

def main():

    
    st.set_page_config(page_title="ESG Risk Materiality Assessment Narrative Tool", layout="wide")
    session_state = SessionState.get()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Insurance Activities", "Investment Activities", "Methodology"])

    if page == "Introduction":
        display_intro_and_disclaimer()
    elif page == "Insurance Activities":
        section_1_insurance_activities(session_state)
    elif page == "Investment Activities":
        section_2_investment_activities(session_state)
    elif page == "Methodology":
        Methodology_Text()



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
    
def section_1_insurance_activities(session_state):
    st.header("Materiality Assessment Questionnaire")

    # Insurance Sector 
    Sector = st.selectbox("Field of (re)insurance operation", ["Please Select", "Life/Health", "NonLife", "Pension", "Composite"])

    # Define the CSV data as a multiline string (assuming it's unchanged)
    csv_data = """Lines of Business,Short Name,Transition Risk Factor,Physical Risk Factor,Exposure,Explanation
Medical expenses,MED,1,2,Low,"Transition Risk: Low as medical underwriting is less impacted by climate policies. Physical Risk: Moderate due to increased health claims from heatwaves, diseases, etc. caused by climate change."
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

    st.write("### 1. Insurance Activities")

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

def create_gradient_heatmap(df):
    # Plotting the gradient heatmap
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define a custom gradient colormap
    colors = ['green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    # Create grid for heatmap
    X, Y = np.meshgrid(np.linspace(0.5, 3.5, 100), np.linspace(0.5, 3.5, 100))
    Z = X + Y  # Combine X and Y to form a grid

    # Map exposure levels to circle sizes
    size_map = {'Low': 50, 'Medium': 150, 'High': 450}

    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[0.5, 3.5, 0.5, 3.5], alpha=0.5)
    
    # To avoid overlapping text, we will keep track of positions
    text_positions = {}
   
    # Scatter plot for LoBs with labels and varying circle sizes based on exposure
    for _, row in df.iterrows():
        if not np.isnan(row['Physical Risk Result']) and not np.isnan(row['Transitional Risk Result']):
            circle_size = size_map[row['Exposure Materiality']]  # Dynamic circle size based on exposure materiality
            ax.scatter(row['Physical Risk Result'], row['Transitional Risk Result'], color='black', zorder=2, s=circle_size)
            # Shorten name if longer than 15 characters for heatmap only
            # short_name = row['Short Name'] if len(row['Lines of Business']) > 15 else row['Lines of Business']
            # ax.text(row['Physical Risk Result'] + 0.1, row['Transitional Risk Result'], short_name, color='black', fontsize=8, zorder=3, ha='left', va='center')
            
            # Adjust position to avoid overlap
            pos = (row['Physical Risk Result'], row['Transitional Risk Result'])
            if pos in text_positions:
                text_positions[pos] += 0.1  # Increment y position slightly to avoid overlap
            else:
                text_positions[pos] = 0  # Initialize position

             # Use short name and add a comma if there's an overlap
            short_name = row['Short Name'] if text_positions[pos] == 0 else row['Short Name'] + ','
            ax.text(row['Physical Risk Result'] + 0.1, row['Transitional Risk Result'] + text_positions[pos], short_name, color='black', fontsize=8, zorder=3, ha='left', va='center')

            
    # Set labels and title
    ax.set_xlabel('Physical Risk')
    ax.set_ylabel('Transitional Risk')
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Low', 'Medium', 'High'])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Low', 'Medium', 'High'])
    ax.set_title('Insurance Lines of Business Heatmap')

    # Set axis limits
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)

    # Automatically adjust layout
    fig.tight_layout()

    # Show plot using st.pyplot to ensure it updates reactively
    st.pyplot(fig)


def section_2_investment_activities(session_state):
    # New section: Investment Activities - Exposure Information
    st.header("2. Investment Activities")

    # Section 2.1: Asset Allocation
    st.subheader("2.1 Asset Allocation")

    # Define the asset allocation data as a multiline string
    asset_csv_data = """Asset Class,Short Name Asset,Transition Risk Factor,Physical Risk Factor,Explanation
    Corporate Bonds,C-BOND,2,2,"Transition Risk: Corporate bonds can be exposed to industries that may face regulatory changes and shifts towards sustainability. Physical Risk: Companies may also be affected by physical risks, but it varies by industry."
    Government Bonds,G-BOND,1,1,"Transition Risk: Governments are generally more stable and can adapt policies over time. Physical Risk: The impact on government bonds is relatively low as governments can spread risk across many sectors."
    Equity,EQUTY,3,3,"Transition Risk: Equities are highly exposed to market sentiment and regulatory changes. Physical Risk: Physical risks can directly impact company operations and revenues."
    Property,PROP,3,3,"Transition Risk: Property investments are directly impacted by regulatory changes related to sustainability. Physical Risk: Properties are highly susceptible to physical risks like extreme weather events."
    Loans,LOAN,2,2,"Transition Risk: The risk depends on the sectors to which loans are extended. Physical Risk: Physical risks can impact the ability of borrowers to repay loans, particularly in vulnerable sectors."
    Holdings in related undertakings including participations,PART,2,2,"Transition Risk: Holdings in related companies can face transition risks if those companies are in vulnerable sectors. Physical Risk: Physical risks depend on the geographic and sectoral exposure of the undertakings."
    Collective investment taking,CIU,3,3,"Transition Risk: Public funds, especially equity, are sensitive to market changes and regulatory shifts. Physical Risk: Funds are exposed to diverse industries and geographies, increasing their vulnerability to physical risks."
    Other assets,OTHER,2,2,"Transition Risk: This category includes a variety of assets, generally leading to mid-level transition risk. Physical Risk: The physical risk is also mid-level due to the mixed nature of these assets."
    """

    # Read the CSV from the multiline string
    asset_df = pd.read_csv(io.StringIO(asset_csv_data.strip()))

    # Display the raw data to debug
    # st.write("### Debug: Raw Asset Data")
    # st.write(asset_df)

    # Initialize an empty list to store updated asset exposure values
    asset_exposure = []

    # Create a layout using st.columns to divide the page
    columns = st.columns([0.1, 1, 1])  # Column layout for index, asset classes, and dropdowns
    columns[0].write("**#**")
    columns[1].write("**Asset Class**")
    columns[2].write("**Asset Class Exposure as Share of Total Asset**")

    # List to store relevant asset classes based on criteria
    relevant_asset_classes = []

    # Display asset allocation table and selectboxes
    for idx, row in asset_df.iterrows():
        col = st.columns([0.1, 1, 1])
        col[0].write(f"**{idx + 1}**")
        col[1].write(row['Asset Class'])
        exposure = col[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No Exposure"], index=1,
                                    key=f"asset_exposure_{idx}",
                                    help=f"Select exposure level for {row['Asset Class']}",
                                    label_visibility="collapsed")
        asset_exposure.append(exposure)

        # Check if exposure level is Low or Not relevant/No Exposure
        if exposure not in ["Low", "Not relevant/No Exposure"]:
            relevant_asset_classes.append(row['Asset Class'])

    # Update the DataFrame with the selected asset exposure
    asset_df['Exposure'] = asset_exposure

    # Filter out rows where exposure is "Not relevant/No Exposure"
    relevant_asset_df = asset_df[asset_df['Exposure'] != "Not relevant/No Exposure"].copy()

    # Display the relevant asset allocation table
    st.write("### Relevant Asset Allocation")
    st.write(relevant_asset_df)

    # Assume df is some DataFrame that needs to be updated with exposure materiality
    df = pd.DataFrame({
        'Asset Class': asset_df['Asset Class'],
        'Short Name Asset': asset_df['Short Name Asset'],
        'Transition Risk Factor': asset_df['Transition Risk Factor'],
        'Physical Risk Factor': asset_df['Physical Risk Factor'],
        'Exposure Materiality Asset': asset_exposure
    })

    # Handle "Not relevant/No Exposure" in risk calculation
    df.loc[df['Exposure Materiality Asset'] == "Not relevant/No Exposure", 'Physical Risk Result'] = np.nan
    df.loc[df['Exposure Materiality Asset'] == "Not relevant/No Exposure", 'Transitional Risk Result'] = np.nan


    # Calculate average exposure level for each risk factor
    df.loc[df['Exposure Materiality Asset'] != "Not relevant/No Exposure", 'Physical Risk Result'] = \
        df[df['Exposure Materiality Asset'] != "Not relevant/No Exposure"].apply(lambda row: \
            (["Low", "Medium", "High"].index(row['Exposure Materiality Asset']) + 1 + row['Physical Risk Factor']) / 2, axis=1)

    df.loc[df['Exposure Materiality Asset'] != "Not relevant/No Exposure", 'Transitional Risk Result'] = \
        df[df['Exposure Materiality Asset'] != "Not relevant/No Exposure"].apply(lambda row: \
            (["Low", "Medium", "High"].index(row['Exposure Materiality Asset']) + 1 + row['Transition Risk Factor']) / 2, axis=1)


    # Create a DataFrame for the heatmap
    heatmap_df = pd.DataFrame({
        'Short Name Asset': df['Short Name Asset'],
        'Physical Risk Result': df['Physical Risk Result'],
        'Transitional Risk Result': df['Transitional Risk Result'],
        'asset_exposure': df['Exposure Materiality Asset']
    })

    # Display the heatmap and results
    st.write("### Heatmap and Results")

    # Create a reactive plot using streamlit's st.pyplot
    create_gradient_heatmap_assets(heatmap_df)
    
    # New question before section 2.2
    st.write("### Are the sectoral and country breakdown of the investment activities available?")
    breakdown_available = st.radio("Choose option:", ("Yes", "No"))

    if breakdown_available == "No":
        st.write("Sectoral and regional breakdown of investment activities are not available.")
    else:
        st.header("2.2 Sectoral and Regional Breakdown of Investment Activities")
        st.write("Here we collect materiality levels for different asset classes across Climate Policy Relevant Sectors (CPRS) for those asset classes with a minimum medium materiality.")

        # Define CPRS categories
        cprs_categories = ["Fossil Fuel", "Utility/Electricity", "Energy Intensive", "Buildings", "Transportation", "Agriculture"]

        # Dummy relevant asset classes for demonstration
        relevant_asset_classes = ["Equity", "Corporate Bonds"]

        # Iterate over each relevant asset class
        for asset_class in relevant_asset_classes:
            if asset_class in ["Equity", "Corporate Bonds"]:  # Only include Equity and Corporate Bonds for this section
                st.markdown(f"#### {asset_class} - Sectoral breakdown")
        
                # Create a table layout for sectoral breakdown for current asset class
                sectoral_cols = st.columns([0.1] + [1] * len(cprs_categories))  # Column layout for index and CPRS categories
        
                # Header row for CPRS categories
                sectoral_cols[0].write("")  # Empty cell for the first column (no numbering)
                for col_idx, category in enumerate(cprs_categories):
                    sectoral_cols[col_idx + 1].write(f"**{category}**")
        
                # Ask materiality questions for each CPRS category and calculate averages
                materiality_values = []
                for idx in range(len(cprs_categories)):
                    materiality = sectoral_cols[idx + 1].selectbox("", options=["Low", "Medium", "High", "Not relevant/No Exposure"], index=1, key=f"{asset_class}_{idx}", help=f"Select materiality for {asset_class} in {cprs_categories[idx]}", label_visibility="collapsed")
        
                    # Assign numeric values based on selection
                    if materiality == "Low":
                        materiality_value = 1
                    elif materiality == "Medium":
                        materiality_value = 2
                    elif materiality == "High":
                        materiality_value = 3
                    else:
                        materiality_value = -10  # Assign a default value for "Not relevant/No Exposure"
        
                    materiality_values.append(materiality_value)
        
                # Calculate CPRS factor (maximum of materiality values for different asset classes)
                cprs_factor = max(materiality_values)
        
                # Retrieve the exposure for the current asset class from section 2.1
                exposure_values = df[df['Asset Class'] == asset_class]['Exposure Materiality Asset'].values
                if len(exposure_values) > 0:
                    exposure = exposure_values[0]
                else:
                    exposure = "Not relevant/No Exposure"
        
                # Assign numeric values based on exposure level
                if exposure == "Low":
                    exposure_level = 1
                elif exposure == "Medium":
                    exposure_level = 2
                elif exposure == "High":
                    exposure_level = 3
                else:
                    exposure_level = 0  # Assign a default value for "Not relevant/No Exposure"
        
                # Calculate average and print recommendation message
                if exposure_level > 0 and cprs_factor > 0:
                    average = (exposure_level + cprs_factor) / 2
                    if average >= 2:
                        st.write(f"Sectoral benchmarking is highly recommended for {asset_class}.")

        # Add the "Government Bond" section
        st.markdown("#### Government Bonds - Country breakdown")
        
        # List of countries for the dropdown
        countries = ["Please select", "USA", "UK", "Germany", "France", "Japan", "China", "Canada", "Australia", "India", "Brazil"]
        
        # Header row
        st.write("Here we collect top five countries for government bonds")
        
        # Rows for the top 5 countries
        for i in range(5):
            gb_row = st.columns([1, 1])  # Create a single row with 2 columns
        
            # Second column: Country selectbox for government bond
            country_gb = gb_row[0].selectbox("", options=countries, key=f"country_gb_{i}")
        
            # Third column: Exposure selectbox for government bond
            exposure_gb = gb_row[1].selectbox("", options=["Low", "Medium", "High", "Not relevant/No Exposure"], key=f"exposure_gb_{i}", help=f"Select the exposure level for government bond portfolio")
        
        # Second loop for property
        st.markdown("#### Property - Country breakdown")
        st.write("Here we collect top five countries for property portfolio")
        
        for i in range(5):
            property_row = st.columns([1, 1])  # Create a single row with 2 columns
        
            # Second column: Country selectbox for property
            country_property = property_row[0].selectbox("", options=countries, key=f"country_property_{i}")
        
            # Third column: Exposure selectbox for property
            exposure_property = property_row[1].selectbox("", options=["Low", "Medium", "High", "Not relevant/No Exposure"], key=f"exposure_property_{i}", help=f"Select the exposure level for property portfolio")


def create_gradient_heatmap_assets(df):
    # Plotting the gradient heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define a custom gradient colormap
    colors = ['green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    X, Y = np.meshgrid(np.linspace(0.5, 3.5, 100), np.linspace(0.5, 3.5, 100))
    Z = (X + Y) / 2  # Combine x and y coordinates to create gradient effect

    # Map exposure levels to circle sizes
    size_map = {'Low': 50, 'Medium': 150, 'High': 450}
    
    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[0.5, 3.5, 0.5, 3.5], alpha=0.5)

    # To avoid overlapping text, we will keep track of positions
    text_positions = {}

    # Scatter plot for assets with labels and varying circle sizes based on exposure
    for _, row in df.iterrows():
        if not np.isnan(row['Physical Risk Result']) and not np.isnan(row['Transitional Risk Result']):
            circle_size = size_map[row['asset_exposure']]  # Dynamic circle size based on exposure materiality
            ax.scatter(row['Physical Risk Result'], row['Transitional Risk Result'], color='black', zorder=2, s=circle_size)
            
            # Adjust position to avoid overlap
            pos = (row['Physical Risk Result'], row['Transitional Risk Result'])
            if pos in text_positions:
                text_positions[pos] += 0.1  # Increment y position slightly to avoid overlap
            else:
                text_positions[pos] = 0  # Initialize position

             # Use short name and add a comma if there's an overlap
            short_name = row['Short Name Asset'] if text_positions[pos] == 0 else row['Short Name Asset'] + ','
            ax.text(row['Physical Risk Result'] + 0.1, row['Transitional Risk Result'] + text_positions[pos], short_name, color='black', fontsize=8, zorder=3, ha='left', va='center')

    # Set labels and title
    ax.set_xlabel('Physical Risk')
    ax.set_ylabel('Transitional Risk')
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Low', 'Medium', 'High'])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Low', 'Medium', 'High'])
    ax.set_title('Investment Classes Heatmap')

    # Set axis limits
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0.5, 3.5)

    # Automatically adjust layout
    fig.tight_layout()

    # Show plot using st.pyplot to ensure it updates reactively
    st.pyplot(fig)


# ----------------------------------------------------------------------------------------
        
def Methodology_Text():
    st.header("Methodology")
    st.write("This is the detailed methodology page where you can explain your methodology in depth.")
    # Add more content as needed.

    # st.title("Methodology")
    
    # Add your Methology Content here
    
    #Methodology_text = """
    #**Environmental Risk Factors - Investments:** 
    
    #This section provides an overview of the how the investments risk factors for the environmental risks are selected. 
    
    #"""
    #st.write(Methodology_text)
    

if __name__ == "__main__":
    main()
