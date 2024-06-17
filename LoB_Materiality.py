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
    st.set_page_config(page_title="Insurance Materiality Assessment", layout="wide")

    # Initialize session state
    session_state = SessionState.get()

    # Display Materiality Assessment
    materiality_assessment(session_state)

def materiality_assessment(session_state):
    st.header("Materiality Assessment")

    # Define the CSV data as a multiline string
    csv_data = """Lines of Business,Transition Risk Factor,Physical Risk Factor,Explanation
ME,1,2,"Transition Risk: Low as medical underwriting is less impacted by climate policies. Physical Risk: Moderate due to increased health claims from heatwaves, diseases, etc. caused by climate change."
WC,2,2,"Transition Risk: Moderate due to changes in workplace safety regulations and standards. Physical Risk: Moderate due to increased workplace injuries from extreme weather."
IP,1,2,"Transition Risk: Low as employment shifts are less affected by climate policies. Physical Risk: Moderate due to long-term health impacts from climate change affecting work capacity."
MISC,1,1,"Transition Risk: Low since miscellaneous financial loss policies are less affected by climate policies. Physical Risk: Low as financial loss underwriting has limited direct physical impact from climate change."
MTPL,2,3,"Transition Risk: Moderate due to the transition to electric vehicles and new regulations. Physical Risk: High due to increased claims from weather-related accidents and damages."
MOI,2,3,"Transition Risk: Similar to motor vehicle insurance with moderate impact. Physical Risk: High due to similar reasons, with higher risk of accidents and damage from extreme weather."
GTPL,3,2,"Transition Risk: High as liability for environmental damage and stricter regulations increase. Physical Risk: Moderate as businesses may face claims related to climate impacts."
ASS,1,2,"Transition Risk: Low impact on underwriting as service models adapt. Physical Risk: Moderate due to increased demand for assistance during extreme events."
MAT,3,3,"Transition Risk: High due to significant regulatory changes in these sectors. Physical Risk: High due to susceptibility to severe weather events and long-term climate impacts on these modes of transport."
FIRE,3,3,"Transition Risk: High as underwriting is impacted by changing building regulations and property values. Physical Risk: High due to increased risk of fires, floods, and other climate-related damages"
"""

    # Read the CSV from the multiline string
    df = pd.read_csv(io.StringIO(csv_data.strip()))

    # Initialize an empty list to store updated materiality values
    exposure_materiality = []

    st.write("### Exposure Assessment")

    # Create a table layout for exposures
    st.write("### Exposure Assessment")

    exp_cols = st.columns([0.1, 1, 1])  # Column layout for index, LoB names, and dropdowns
    exp_cols[0].write("**#**")
    exp_cols[1].write("**Line of Business**")
    exp_cols[2].write("**Exposure**")

    for idx, row in df.iterrows():
        exp_cols = st.columns([0.1, 1, 1])
        exp_cols[0].write(f"**{idx+1}**")
        exp_cols[1].write(row['Lines of Business'])
        materiality = exp_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"materiality_{idx}", help=f"Select exposure level for {row['Lines of Business']}", label_visibility="collapsed")
        exposure_materiality.append(materiality)

    # Update the DataFrame with the selected exposure materiality
    df['Exposure Materiality'] = exposure_materiality

    # Filter out rows where exposure materiality is "Not relevant/No exposure"
    df_filtered = df[df['Exposure Materiality'] != "Not relevant/No exposure"].copy()

    # Calculate average risk factors based on exposure materiality
    df_filtered['Physical Risk Result'] = df_filtered.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + 1 + row['Physical Risk Factor']) / 2, axis=1)
    df_filtered['Transitional Risk Result'] = df_filtered.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + 1 + row['Transition Risk Factor']) / 2, axis=1)

    # Display the heatmap and final table
    st.write("### Heatmap and Results")

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

    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[0.5, 3.5, 0.5, 3.5], alpha=0.5)

    # Scatter plot for LoBs with labels
    for _, row in df.iterrows():
        if not np.isnan(row['Physical Risk Result']) and not np.isnan(row['Transitional Risk Result']):
            ax.scatter(row['Physical Risk Result'], row['Transitional Risk Result'], color='black', zorder=2)
            # Shorten name if longer than 15 characters
            short_name = row['Lines of Business'] if len(row['Lines of Business']) <= 15 else row['Lines of Business'][:15] + "..."
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

    # Show plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()
