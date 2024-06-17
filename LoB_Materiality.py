import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io

def main():
    st.set_page_config(page_title="Insurance Materiality Assessment", layout="wide")

    # Load data
    df = load_data()

    # Display materiality assessment
    materiality_assessment(df)

def load_data():
    # Sample data
    csv_data = """Lines of Business,Short Name,Transition Risk Factor,Physical Risk Factor,Exposure,Explanation
Medical expenses,ME,1,2,Low,"Transition Risk: Low as medical underwriting is less impacted by climate policies. Physical Risk: Moderate due to increased health claims from heatwaves, diseases, etc. caused by climate change."
Worker compensation,WC,2,2,Medium,"Transition Risk: Moderate due to changes in workplace safety regulations and standards. Physical Risk: Moderate due to increased workplace injuries from extreme weather."
Income protection,IP,1,2,Low,"Transition Risk: Low as employment shifts are less affected by climate policies. Physical Risk: Moderate due to long-term health impacts from climate change affecting work capacity."
Miscellaneous financial loss,MISC,1,1,Low,"Transition Risk: Low since miscellaneous financial loss policies are less affected by climate policies. Physical Risk: Low as financial loss underwriting has limited direct physical impact from climate change."
Motor vehicle insurance,MTPL,2,3,High,"Transition Risk: Moderate due to the transition to electric vehicles and new regulations. Physical Risk: High due to increased claims from weather-related accidents and damages."
Other motor insurance,MOI,2,3,High,"Transition Risk: Similar to motor vehicle insurance with moderate impact. Physical Risk: High due to similar reasons, with higher risk of accidents and damage from extreme weather."
General liability insurance,GTPL,3,2,Medium,"Transition Risk: High as liability for environmental damage and stricter regulations increase. Physical Risk: Moderate as businesses may face claims related to climate impacts."
Assistance,ASS,1,2,Low,"Transition Risk: Low impact on underwriting as service models adapt. Physical Risk: Moderate due to increased demand for assistance during extreme events."
\"Marine, aviation and transport insurance\",MAT,3,3,High,"Transition Risk: High due to significant regulatory changes in these sectors. Physical Risk: High due to susceptibility to severe weather events and long-term climate impacts on these modes of transport."
Fire and other damage to property insurance,FIRE,3,3,High,"Transition Risk: High as underwriting is impacted by changing building regulations and property values. Physical Risk: High due to increased risk of fires, floods, and other climate-related damages"
"""
    # Read CSV data into DataFrame
    df = pd.read_csv(io.StringIO(csv_data.strip()))
    return df

def materiality_assessment(df):
    st.header("Materiality Assessment")

    # Display exposure assessment
    st.subheader("Exposure Assessment")
    df['Exposure Level'] = df.apply(lambda row: st.selectbox(f"{row['Lines of Business']} - Exposure Level",
                                                             options=["Low", "Medium", "High"],
                                                             index=0),
                                    axis=1)

    # Filter out rows with 'Not relevant/No exposure'
    df_filtered = df[df['Exposure Level'] != 'Not relevant/No exposure'].copy()

    # Calculate average risk factors
    df_filtered['Average Risk Factor'] = (df_filtered['Transition Risk Factor'] + df_filtered['Physical Risk Factor']) / 2

    # Display heatmap and summary
    st.subheader("Heatmap and Summary")

    create_heatmap(df_filtered)

    st.subheader("Summary - Environmental Materiality Analysis")
    for idx, row in df_filtered.iterrows():
        if row['Average Risk Factor'] >= 2:
            st.markdown(f"**{row['Lines of Business']}** - {row['Explanation']}")
            st.markdown(f"Since the average risk factor is >= 2, a further deep dive and quantification is suggested for two climate scenarios: one below 2 degrees Celsius and one above 2 degrees Celsius of global warming.")
        else:
            st.markdown(f"**{row['Lines of Business']}** - {row['Explanation']}")
            st.markdown("The risk is not material enough to warrant quantification at this stage.")

def create_heatmap(df):
    # Define colormap
    colors = ['green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot heatmap
    sc = ax.scatter(df['Transition Risk Factor'], df['Physical Risk Factor'], c=df['Average Risk Factor'], cmap=cmap, edgecolors='k', s=200)
    fig.colorbar(sc, ax=ax, label='Average Risk Factor')

    # Set labels and title
    ax.set_xlabel('Transition Risk Factor')
    ax.set_ylabel('Physical Risk Factor')
    ax.set_title('Insurance Materiality Assessment')
    ax.grid(True)

    # Show plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()
