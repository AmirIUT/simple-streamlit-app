import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io

def main():
    st.set_page_config(page_title="Insurance Materiality Assessment", layout="wide")

    # Initialize session state
    session_state = SessionState.get(page="Application ReadMe")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Application ReadMe"):
        session_state.page = "Application ReadMe"
    if st.sidebar.button("Materiality Assessment"):
        session_state.page = "Materiality assessment"

    # Render the current page based on session state
    if session_state.page == "Application ReadMe":
        display_readme()
    elif session_state.page == "Materiality assessment":
        materiality_assessment()

def display_readme():
    st.title("Application ReadMe")
    st.write("Placeholder for your ReadMe text goes here.")
    st.write("### Go to Materiality Assessment")
    st.write("Click the link below to navigate to the Materiality Assessment page.")
    if st.button("Go to Materiality Assessment"):
        SessionState.get().page = "Materiality assessment"

def materiality_assessment():
    st.title("Materiality Assessment")

    # Define the CSV data as a multiline string
    csv_data = """Lines of Business,Transition Risk Factor,Physical Risk Factor,Explanation
Medical expenses,1,2,"Transition Risk: Low as medical underwriting is less impacted by climate policies. Physical Risk: Moderate due to increased health claims from heatwaves, diseases, etc. caused by climate change."
Worker compensation,2,2,"Transition Risk: Moderate due to changes in workplace safety regulations and standards. Physical Risk: Moderate due to increased workplace injuries from extreme weather."
Income protection,1,2,"Transition Risk: Low as employment shifts are less affected by climate policies. Physical Risk: Moderate due to long-term health impacts from climate change affecting work capacity."
Miscellaneous financial loss,1,1,"Transition Risk: Low since miscellaneous financial loss policies are less affected by climate policies. Physical Risk: Low as financial loss underwriting has limited direct physical impact from climate change."
Motor vehicle insurance,2,3,"Transition Risk: Moderate due to the transition to electric vehicles and new regulations. Physical Risk: High due to increased claims from weather-related accidents and damages."
Other motor insurance,2,3,"Transition Risk: Similar to motor vehicle insurance with moderate impact. Physical Risk: High due to similar reasons, with higher risk of accidents and damage from extreme weather."
General liability insurance,3,2,"Transition Risk: High as liability for environmental damage and stricter regulations increase. Physical Risk: Moderate as businesses may face claims related to climate impacts."
Assistance,1,2,"Transition Risk: Low impact on underwriting as service models adapt. Physical Risk: Moderate due to increased demand for assistance during extreme events."
\"Marine, aviation and transport insurance\",3,3,"Transition Risk: High due to significant regulatory changes in these sectors. Physical Risk: High due to susceptibility to severe weather events and long-term climate impacts on these modes of transport."
Fire and other damage to property insurance,3,3,"Transition Risk: High as underwriting is impacted by changing building regulations and property values. Physical Risk: High due to increased risk of fires, floods, and other climate-related damages"
"""

    # Read the CSV from the multiline string
    df = pd.read_csv(io.StringIO(csv_data.strip()))

    # Ask for materiality of exposure (Low, Medium, High) for each LoB
    st.header("Exposure Adjustment")
    exposure_levels = ["Low", "Medium", "High"]
    
    # Loop through each line of business
    for idx, row in df.iterrows():
        # Display the dropdown and update exposure materiality
        materiality = st.selectbox(f"Materiality of Exposure for {row['Lines of Business']}:", options=exposure_levels, index=exposure_levels.index(row['Exposure Materiality']))
        if materiality != row['Exposure Materiality']:
            df.at[idx, 'Exposure Materiality'] = materiality

    # Calculate average risk factors based on exposure materiality
    df['Physical Risk Result'] = df.apply(lambda row: calculate_average_factor(row['Exposure Materiality'], row['Physical Risk Factor']), axis=1)
    df['Transitional Risk Result'] = df.apply(lambda row: calculate_average_factor(row['Exposure Materiality'], row['Transition Risk Factor']), axis=1)

    # Create the gradient heatmap and overlay dots
    create_gradient_heatmap(df)

    # Display the CSV table (without editable Explanation column)
    st.header("Insurance Lines of Business Table")
    df_display = df.drop(columns=['Explanation'])  # Drop Explanation column for display
    st.write(df_display)

    # Allow possibility to overwrite risk factors after displaying the heatmap
    st.header("Overwrite Risk Factors")
    for index, row in df.iterrows():
        df.at[index, 'Transition Risk Factor'] = st.number_input(f"Transition Risk Factor for {row['Lines of Business']}", value=row['Transition Risk Factor'])
        df.at[index, 'Physical Risk Factor'] = st.number_input(f"Physical Risk Factor for {row['Lines of Business']}", value=row['Physical Risk Factor'])

def calculate_average_factor(materiality, risk_factor):
    # Calculate average factor based on materiality of exposure
    if materiality == "Low":
        exposure_factor = 1
    elif materiality == "Medium":
        exposure_factor = 2
    elif materiality == "High":
        exposure_factor = 3
    
    return (exposure_factor + risk_factor) / 2

def create_gradient_heatmap(df):
    # Plotting the gradient heatmap
    fig, ax = plt.subplots()

    # Define a custom gradient colormap
    colors = ['green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    # Create grid for heatmap
    X, Y = np.meshgrid(np.linspace(1, 3.5, 100), np.linspace(1, 3.5, 100))
    Z = X + Y  # Combine X and Y to form a grid

    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[1, 3.5, 1, 3.5], alpha=0.5)

    # Scatter plot for LoBs with labels
    for _, row in df.iterrows():
        if not np.isnan(row['Physical Risk Result']) and not np.isnan(row['Transitional Risk Result']):
            ax.scatter(row['Physical Risk Result'], row['Transitional Risk Result'], color='black', zorder=2)
            ax.text(row['Physical Risk Result'] + 0.05, row['Transitional Risk Result'], row['Lines of Business'], color='black', fontsize=12, zorder=3)

    # Set labels and title
    ax.set_xlabel('Physical Risk Result')
    ax.set_ylabel('Transition Risk Result')
    ax.set_title('Insurance Lines of Business Heatmap')

    # Set axis limits
    ax.set_xlim(1, 3.5)
    ax.set_ylim(1, 3.5)

    # Show plot
    st.pyplot(fig)

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

if __name__ == "__main__":
    main()
