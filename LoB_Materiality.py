import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def main():
    st.title("Insurance Lines of Business Heatmap")
    
    st.write("Select the exposure level for each Insurance Line of Business (LoB):")

    # Dropdown for Fire LoB exposure
    st.subheader("Fire LoB")
    fire_exposure = st.selectbox("Exposure Rating:", options=["Low", "Medium", "High", "Not Relevant"], key="fire_exposure")

    # Dropdown for General Liability LoB exposure
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

    # Create the gradient heatmap and overlay dots
    create_gradient_heatmap(fire_physical_rating, fire_transitional_rating, gl_physical_rating, gl_transitional_rating)

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
    physical_factor = 3  # Adjust this based on your requirements
    transitional_factor = 1  # Adjust this based on your requirements

    # Determine which factor to use based on the physical parameter
    if physical:
        rating = (exposure_value + physical_factor) / 2
    else:
        rating = (exposure_value + transitional_factor) / 2

    return rating

def create_gradient_heatmap(fire_physical_rating, fire_transitional_rating, gl_physical_rating, gl_transitional_rating):
    # Define labels and ratings for each Line of Business (LoB)
    lobs = ["Fire", "General Liability"]
    physical_ratings = [fire_physical_rating, gl_physical_rating]
    transitional_ratings = [fire_transitional_rating, gl_transitional_rating]

    # Plotting the gradient heatmap
    fig, ax = plt.subplots()

    # Define a custom gradient colormap
    colors = ['green', 'yellow', 'red']
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    # Create grid for heatmap
    X, Y = np.meshgrid(np.linspace(1, 3, 100), np.linspace(1, 3, 100))
    Z = X + Y  # Combine X and Y to form a grid

    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[1, 3, 1, 3], alpha=0.5)

    # Scatter plot for LoBs with labels
    for i, lob in enumerate(lobs):
        ax.scatter(physical_ratings[i], transitional_ratings[i], color='black', zorder=2)
        ax.text(physical_ratings[i] + 0.05, transitional_ratings[i], lob, color='black', fontsize=12, zorder=3)

    # Set labels and title
    ax.set_xlabel('Physical Risk')
    ax.set_ylabel('Transitional Risk')
    ax.set_title('Insurance Lines of Business Heatmap')

    # Set axis limits
    ax.set_xlim(1, 3)
    ax.set_ylim(1, 3)

    # Show plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()
