import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Insurance Lines of Business Heatmap")
    
    st.write("Select the exposure levels for each Insurance Line of Business (LoB):")

    # Dropdowns for Fire LoB
    st.subheader("Fire LoB")
    fire_physical_risk = st.selectbox("Physical Risk:", options=["Low", "Medium", "High", "Not Relevant"], key="fire_physical")
    fire_transitional_risk = st.selectbox("Transitional Risk:", options=["Low", "Medium", "High", "Not Relevant"], key="fire_transitional")

    # Dropdowns for General Liability LoB
    st.subheader("General Liability LoB")
    gl_physical_risk = st.selectbox("Physical Risk:", options=["Low", "Medium", "High", "Not Relevant"], key="liab_physical")
    gl_transitional_risk = st.selectbox("Transitional Risk:", options=["Low", "Medium", "High", "Not Relevant"], key="liab_transitional")

    # Convert exposure levels to numerical values
    fire_physical_value = map_exposure_to_value(fire_physical_risk)
    fire_transitional_value = map_exposure_to_value(fire_transitional_risk)
    gl_physical_value = map_exposure_to_value(gl_physical_risk)
    gl_transitional_value = map_exposure_to_value(gl_transitional_risk)

    # Calculate averages for positioning in heatmap
    fire_avg = np.mean([fire_physical_value, fire_transitional_value])
    gl_avg = np.mean([gl_physical_value, gl_transitional_value])

    # Create the heatmap
    create_heatmap(fire_avg, gl_avg)

def map_exposure_to_value(exposure_level):
    if exposure_level == "Low":
        return 1
    elif exposure_level == "Medium":
        return 2
    elif exposure_level == "High":
        return 3
    else:
        return 0  # Not Relevant

def create_heatmap(fire_avg, gl_avg):
    # Define labels and values
    lob_labels = ["Fire", "General Liability"]
    physical_risk_labels = ["Low", "Medium", "High"]
    transitional_risk_labels = ["Low", "Medium", "High"]

    # Create data for heatmap
    data = np.array([[fire_avg, fire_avg, fire_avg],
                     [gl_avg, gl_avg, gl_avg]])

    # Plot the heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap="YlOrRd")

    # Set ticks and labels
    ax.set_xticks(np.arange(len(physical_risk_labels)))
    ax.set_yticks(np.arange(len(lob_labels)))
    ax.set_xticklabels(physical_risk_labels)
    ax.set_yticklabels(lob_labels)

    # Rotate the tick labels and set alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations
    for i in range(len(lob_labels)):
        for j in range(len(physical_risk_labels)):
            text = ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center", color="black")

    ax.set_title("Insurance Lines of Business Heatmap")
    ax.set_xlabel("Physical Risk")
    ax.set_ylabel("Insurance Lines of Business")

    # Show heatmap
    st.pyplot(fig)

if __name__ == "__main__":
    main()
