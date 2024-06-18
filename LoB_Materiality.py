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
    st.title("ESG Risk Materiality Assessment Narrative Tool ")
    
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
    st.header("Materliaty Assessment Questionnaire")

    # Insurance Sector 
    Sector = st.selectbox("Field of (re)insurance operation", ["Life/Health", "NonLife", "Pension", "Composite"])

    # Define the CSV data as a multiline string
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

    st.write("### Insurance Activities - Exposure Information")

    # Define the width ratio for the legend and table sections
    legend_width = 0.6  # Width ratio for legend
    table_width = 0.2   # Width ratio for table

    # Create a layout using st.columns to divide the page
    columns = st.columns([legend_width, table_width])

   

    # Column 1: Table layout for exposures
    with columns[0]:
        st.write("### Exposure Assessment")

        # Create a table layout for exposures
        exp_cols = st.columns([0.1, 1, 1])  # Column layout for index, LoB names, and dropdowns
        exp_cols[0].write("**#**")
        exp_cols[1].write("**Line of Business (LoB)**")
        exp_cols[2].write("**LoB Share in Total Net Premium**")

        exposure_materiality = []

        for idx, row in df.iterrows():
            exp_cols = st.columns([0.1, 1, 1])
            exp_cols[0].write(f"**{idx+1}**")
            exp_cols[1].write(row['Lines of Business'])
            materiality = exp_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"materiality_{idx}", help=f"Select exposure level for {row['Lines of Business']}", label_visibility="collapsed")
            exposure_materiality.append(materiality)
    # Column 2: Legend for materiality definitions
    with columns[1]:
        """



        """
        st.markdown("Legend: Exposure Share Definition") 
        """



        """
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

    # Scatter plot for LoBs with labels and varying circle sizes based on exposure
    for _, row in df.iterrows():
        if not np.isnan(row['Physical Risk Result']) and not np.isnan(row['Transitional Risk Result']):
            circle_size = size_map[row['Exposure Materiality']]  # Dynamic circle size based on exposure materiality
            ax.scatter(row['Physical Risk Result'], row['Transitional Risk Result'], color='black', zorder=2, s=circle_size)
            # Shorten name if longer than 15 characters for heatmap only
            short_name = row['Short Name'] if len(row['Lines of Business']) > 15 else row['Lines of Business']
            ax.text(row['Physical Risk Result'] + 0.1, row['Transitional Risk Result'], short_name, color='black', fontsize=8, zorder=3, ha='left', va='center')

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

if __name__ == "__main__":
    main()
