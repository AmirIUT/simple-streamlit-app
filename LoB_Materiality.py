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

    # 2.1. Asset Allocation
    st.subheader("2.1. Asset Allocation")
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
    asset_exposure = []

    # Create a table layout for asset allocation
    asset_cols = st.columns([0.1, 1, 1])  # Column layout for index, asset classes, and dropdowns
    asset_cols[0].write("**#**")
    asset_cols[1].write("**Asset Class**")
    asset_cols[2].write("**Asset Class Exposure as Share of Total Asset**")

    for idx, row in asset_df.iterrows():
        asset_cols = st.columns([0.1, 1, 1])
        asset_cols[0].write(f"**{idx+1}**")
        asset_cols[1].write(row['Asset class'])
        exposure = asset_cols[2].selectbox("", options=["Low", "Medium", "High", "Not relevant/No exposure"], index=1, key=f"asset_exposure_{idx}", help=f"Select exposure level for {row['Asset class']}", label_visibility="collapsed")
        asset_exposure.append(exposure)

    # Update the DataFrame with the selected asset exposure
    asset_df['Exposure'] = asset_exposure

    # 2.2 Placeholder for Next Sub-section (conditionally displayed)
    display_section_2_2()

def display_section_2_2():
    st.subheader("2.2 Placeholder for Next Sub-section")

    # New question: Are the sectoral and regional breakdown of the investment activities available?
    breakdown_available = st.radio("Are the sectoral and regional breakdown of the investment activities available?", ("Yes", "No"))

    if breakdown_available == "Yes":
        st.write("More information will be added here based on sectoral and regional breakdown.")
    else:
        st.warning("Sectoral and regional breakdown information is not available.")

if __name__ == "__main__":
    main()
