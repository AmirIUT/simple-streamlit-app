import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Insurance Lines of Business Heatmap")
    
    st.write("Select the exposure level for each Insurance Line of Business (LoB):")

    # Dropdowns for Fire LoB
    st.subheader("Fire LoB")
    fire_exposure = st.selectbox("Exposure Rating:", options=["Low", "Medium", "High", "Not Relevant"], key="fire_exposure")

    # Dropdowns for General Liability LoB
    st.subheader("General Liability LoB")
    gl_exposure = st.selectbox("Exposure Rating:", options=["Low", "Medium", "High", "Not Relevant"], key="gl_exposure")

    # Convert exposure levels to numerical values
    fire_exposure_value = map_exposure_to_value(fire_exposure)
    gl_exposure_value = map_exposure_to_value(gl_exposure)

    # Calculate ratings for heatmap
    fire_physical_rating = calculate_rating(fire_exposure_value, physical=True)
    fire_transitional_rating = calculate_rating(fire_exposure_value, physical=False)
    gl_physical_rating = calculate_rating(gl_exposure_value, physical=True)
    gl_transitional_rating = calculate_rating(gl_exposure_value, physical=False)

    # Create the heatmap
    create_heatmap(fire_physical_rating, fire_transitional_rating, gl_physical_rating, gl_transitional_rating)

def map_exposure_to_value(exposure_level):
    if exposure_level == "Low":
        return 1
    elif exposure_level == "Medium":
        return 2
    elif exposure_level == "High":
        return 3
    else:
        return 0  # Not Relevant

def calculate_rating(exposure_value, physical=True):
    # Factors defined for physical and transitional ratings
    if physical:
        physical_factor = 3  # Adjust this based on your requirements
    else:
        transitional_factor = 1  # Adjust this based on your requirements

    # Calculate average rating
    return (exposure_value + physical_factor) / 2

def create_heatmap(fire_physical_rating, fire_transitional_rating, gl_physical_rating, gl_transitional_rating):
    # Define labels and values
    lob_labels = ["Fire", "General Liability"]
    risk_labels = ["Physical Risk", "Transitional Risk"]

    # Create data for heatmap
    data = np.array([[fire_physical_rating, fire_transitional_rating],
                     [gl_physical_rating, gl_transitional_rating]])

    # Plot the heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap="YlOrRd")

    # Set ticks and labels
    ax.set_xticks(np.arange(len(risk_labels)))
    ax.set_yticks(np.arange(len(lob_labels)))
    ax.set_xticklabels(risk_labels)
    ax.set_yticklabels(lob_labels)

    # Rotate the tick labels and set alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations
    for i in range(len(lob_labels)):
        for j in range(len(risk_labels)):
            text = ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")

    ax.set_title("Insurance Lines of Business Heatmap")
    ax.set_xlabel("Risk Dimension")
    ax.set_ylabel("Insurance Lines of Business")

    # Show heatmap
    st.pyplot(fig)

if __name__ == "__main__":
    main()
