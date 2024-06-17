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
    size_map = {'Low': 50, 'Medium': 100, 'High': 150}

    # Plot the gradient heatmap
    im = ax.imshow(Z, cmap=cmap, origin='lower', extent=[0.5, 3.5, 0.5, 3.5], alpha=0.5)

    # Scatter plot for LoBs with labels and varying circle sizes based on exposure
    for idx, row in df.iterrows():
        # Ensure columns are correctly accessed based on their new names
        physical_risk = row['User Defined Physical Risk'] if np.isnan(row['Risk Result (Physical)']) else row['Risk Result (Physical)']
        transitional_risk = row['User Defined Transition Risk'] if np.isnan(row['Risk Result (Transitional)']) else row['Risk Result (Transitional)']

        # Convert risk levels to heatmap coordinates
        physical_risk_coord = (physical_risk - 1) / 2 + 0.5
        transitional_risk_coord = (transitional_risk - 1) / 2 + 0.5

        # Get size of circle based on exposure level
        size = size_map.get(row['Exposure'], 50)

        ax.scatter(physical_risk_coord, transitional_risk_coord, color='black', zorder=2, s=size)
        
        # Shorten name if longer than 15 characters for heatmap only
        short_name = row['Short Name'] if len(row['Lines of Business']) > 15 else row['Lines of Business']
        ax.text(physical_risk_coord + 0.1, transitional_risk_coord, short_name, color='black', fontsize=8, zorder=3, ha='left', va='center')

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
