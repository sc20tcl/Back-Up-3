import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

def read_data(file_path):
    """
    Reads the CSV file and returns a DataFrame.
    """
    return pd.read_csv(file_path)

def process_data(df, country, flow_type='inflow'):
    """
    Filters and aggregates the data for a specific country to calculate total inflow or outflow.
    """
    if flow_type == 'inflow':
        df_filtered = df[df['Country of asylum (ISO)'] == country]
        aggregated = df_filtered.groupby('Country of origin (ISO)')[['Refugees under UNHCR\'s mandate', 'Asylum-seekers']].sum().sum(axis=1)
    else:
        df_filtered = df[df['Country of origin (ISO)'] == country]
        aggregated = df_filtered.groupby('Country of asylum (ISO)')[['Refugees under UNHCR\'s mandate', 'Asylum-seekers']].sum().sum(axis=1)

    return pd.DataFrame(aggregated, columns=[flow_type])

def visualize_data(df, country, flow_type='inflow'):
    """
    Visualizes the data on a world map with an extremely light blue color scale,
    making non-data countries white, and includes a custom legend and a color bar with a label.
    """
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Exclude Antarctica
    world = world[world['name'] != 'Antarctica']

    # Merging world data with the processed data
    merged = world.set_index('iso_a3').join(df, how='left')

    plt.rcParams.update({'font.size': 11})  # Set global font size to 11pt

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    # Define boundaries and colormap
    boundaries = [0, 4, 25, 162, 1032, 6554, 15000, 30000, 41618, 260000]
    norm = mcolors.BoundaryNorm(boundaries, ncolors=256)
    cmap = mcolors.ListedColormap(plt.cm.Blues(np.linspace(0.005, 1, 256)))

    # Plotting the world and the data
    world.plot(ax=ax, color='white', edgecolor='black', linewidth=0.5)
    merged.dropna().plot(column=flow_type, ax=ax, cmap=cmap, edgecolor='black', linewidth=0.5, legend=False, norm=norm)
    merged[merged.index == country].plot(ax=ax, color='orange', edgecolor='black', linewidth=0.5)

    # Create a patch for the legend and add legend to the figure
    somalia_patch = mpatches.Patch(color='orange', label='Somalia')
    fig.legend(handles=[somalia_patch], loc='center left', bbox_to_anchor=(0.1, 0.5, 0.5, 0.5), fontsize=11)

    # Add caption
    caption = "This Thematic map visualizes the extent of Somali refugee outflows in 2019, with varying shades of blue indicating the volume of refugees in each destination country."
    plt.figtext(0.5, 0.2, caption, wrap=True, horizontalalignment='center', fontsize=11)

    # Customize the color bar and add label
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = plt.colorbar(mappable=plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
    cbar.set_label('Number of Asylum Seekers', fontsize=11)
    cbar.set_ticks(boundaries)
    cbar.set_ticklabels([f'{boundary}' for boundary in boundaries])
    cbar.ax.tick_params(labelsize=11)

    ax.set_axis_off()
    plt.savefig(f"{country}_{flow_type}FINAL.png", bbox_inches='tight', dpi=300)
    plt.show()

def main():
    # Hardcoded file path, country, and flow type
    file_path = "population.csv"  # Replace with your file name
    country = "SOM"  # Replace with your chosen country ISO code
    flow_type = "outflow"  # Choose 'inflow' or 'outflow'

    df = read_data(file_path)
    processed_df = process_data(df, country, flow_type)
    visualize_data(processed_df, country, flow_type)

if __name__ == "__main__":
    main()