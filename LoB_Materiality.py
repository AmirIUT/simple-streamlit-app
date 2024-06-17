import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io

def main():
    st.title("Insurance Lines of Business Heatmap")

    # Define the CSV data as a multiline string
    csv_data = """
    Lines of Business,Transitional Risk Factor,Physical Risk Factor,Explanation
    Medical expenses,1,2,Transition Risk: Low as medical underwriting is less impacted by climate policies 
    """


    # Read the CSV from the multiline string
    df = pd.read_csv(io.StringIO(csv_data))

    # Display the table
    st.write("Default table:")
    st.write(df)

    # Add inputs to overwrite risk factors
    for index, row in df.iterrows():
        df.at[index, 'Transitional Risk Factor'] = st.number_input(f"Transitional Risk Factor for {row['Lines of Business']}", value=row['Transitional Risk Factor'])
        df.at[index, 'Physical Risk Factor'] = st.number_input(f"Physical Risk Factor for {row['Lines of Business']}", value=row['Physical Risk Factor'])
        df.at[index, 'Explanation'] = st.text_input(f"Explanation for {row['Lines of Business']}", value=row['Explanation'])

    # Create a dropdown for each LoB to select exposure level
    exposure_levels = ["Low", "Medium", "High", "Not Relevant"]
    df['Exposure'] = df['Lines of Business'].apply(lambda x: st.selectbox(f"Select exposure for {x}:", options=exposure_levels))

    # Convert exposure levels to numerical values
    df['Exposure Value'] = df['Exposure'].apply(map_exposure_to_value)

    # Calculate ratings
    df['Physical Rating'] = df.apply(lambda row: calculate_rating(row['Exposure Value'], row['Physical Risk Factor']), axis=1)
    df['Transitional Rating'] = df.apply(lambda row: calculate_rating(row['Exposure Value'], row['Transitional Risk Factor']), axis=1)

    # Create the gradient heatmap and overlay dots
    create_gradient_heatmap(df)

def map_exposure_to_value(exposure_level):
    if exposure_level == "Low":
        return 1
    elif exposure_level == "Medium":
        return 2
    elif exposure_level == "High":
        return 3
    else:
        return 0  # Not Relevant

def calculate_rating(exposure_value, risk_factor):
    # Calculate average rating based on exposure value and risk factor
    if exposure_value == 0:  # Not Relevant
        return np.nan  # Return NaN for not relevant to avoid plotting
    else:
        return (exposure_value + risk_factor) / 2

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
        if not np.isnan(row['Physical Rating']) and not np.isnan(row['Transitional Rating']):
            ax.scatter(row['Physical Rating'], row['Transitional Rating'], color='black', zorder=2)
            ax.text(row['Physical Rating'] + 0.05, row['Transitional Rating'], row['Lines of Business'], color='black', fontsize=12, zorder=3)

    # Set labels and title
    ax.set_xlabel('Physical Risk')
    ax.set_ylabel('Transitional Risk')
    ax.set_title('Insurance Lines of Business Heatmap')

    # Set axis limits
    ax.set_xlim(1, 3.5)
    ax.set_ylim(1, 3.5)

    # Show plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()
