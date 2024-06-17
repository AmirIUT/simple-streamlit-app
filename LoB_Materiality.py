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
        materiality_assessment(session_state)

def display_readme():
    st.title("Application ReadMe")
    st.write("Placeholder for your ReadMe text goes here.")
    st.write("### Go to Materiality Assessment")
    st.write("Click the link below to navigate to the Materiality Assessment page.")
    if st.button("Go to Materiality Assessment"):
        SessionState.get().page = "Materiality assessment"

def materiality_assessment(session_state):
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

    # Initialize an empty list to store updated materiality values
    exposure_materiality = []

    # Loop through each line of business
    for idx, row in df.iterrows():
        # Display the dropdown and update exposure materiality
        materiality = st.selectbox(f"Materiality of Exposure for {row['Lines of Business']}:", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index("Medium"))
        exposure_materiality.append(materiality)

    # Update the DataFrame with the selected exposure materiality
    df['Exposure Materiality'] = exposure_materiality

    # Calculate average risk factors based on exposure materiality
    df['Physical Risk Result'] = df.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + row['Physical Risk Factor']) / 2, axis=1)
    df['Transitional Risk Result'] = df.apply(lambda row: (["Low", "Medium", "High"].index(row['Exposure Materiality']) + row['Transition Risk Factor']) / 2, axis=1)

    # Create the gradient heatmap and overlay dots
    create_gradient_heatmap(df)

    # Display the CSV table (without editable Explanation column)
    st.header("Insurance Lines of Business Table")
    df_display = df.drop(columns=['Explanation'])  include possible
