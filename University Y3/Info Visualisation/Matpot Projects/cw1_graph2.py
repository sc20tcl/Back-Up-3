import matplotlib.pyplot as plt
import matplotlib as mpl

# Set the global font size to 11pt
mpl.rcParams.update({'font.size': 11})

# Data for the top 5 highest and lowest application/displaced ratios
countries = ['Cote d\'Ivoire', 'Viet Nam', 'Afghanistan', 'Tanzania ', 'Bangladesh', 
             'Madagascar', 'Suriname', 'Haiti', 'Iceland', 'Slovenia']
ratios = [-0.000169, -0.000164, -0.000064,  -0.000034,  -0.000004, 
           0.718, 0.830, 1.000, 1.131, 3.671]  # Negative values for the lowest ratios

# Create the figure and primary axis
fig, ax1 = plt.subplots(figsize=(12, 8))  # Increased figure height

# Bar plot for the highest ratios
bars_high = ax1.bar(countries[5:], ratios[5:], color='blue')

# Set primary y-axis for the highest ratios (0 to 5)
ax1.set_ylim(0, 5)
ax1.set_ylabel('Ratio of current displaced indivuals : applicants')  # Label for primary y-axis

# Create a secondary axis for the lowest ratios
ax2 = ax1.twinx()

# Invert secondary y-axis for the lowest ratios
ax2.invert_yaxis()

# Bar plot for the lowest ratios on secondary axis
bars_low = ax2.bar(countries[:5], [-r for r in ratios[:5]], color='orange')

# Set secondary y-axis for the inverted lowest ratios
ax2.set_ylim(0, 0.0002)
ax2.set_ylabel('Ratio of current displaced indivuals : applicants')  # Label for secondary y-axis

# Adding a legend
ax1.legend((bars_high[0], bars_low[0]), ('Top 5 Highest Ratios', 'Top 5 Lowest Ratios'), loc='upper right')

# Adding labels and title
ax1.set_xlabel('Countries')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

# Adding the caption below the chart with increased padding
caption = "Illustrated here are the countries with the five highest and five lowest ratios of asylum applications compared to the displaced individuals already present."
plt.figtext(0.53, 0.1, caption, ha='center', wrap=True)

# Adjust the layout to accommodate the caption
plt.subplots_adjust(bottom=0.25)

# Show the plot with adjusted layout
plt.savefig("AppRatio.png", bbox_inches='tight', dpi=300)
plt.show()
