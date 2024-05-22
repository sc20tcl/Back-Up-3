import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

plt.rcParams.update({'font.size': 11})

# Prepare your data
categories = ['2011', '2012']
sub_categories = ['% men', '% women']
values = [[15.1, 28.3], [25.2, 30.0]]  # values for each sub-category in each category

# Convert categories to numeric value for plotting
categories_numeric = [int(category) for category in categories]

# Create a new figure and axes with a size of 4x6 inches
fig, ax = plt.subplots(figsize=(6, 4))

# Plotting the data
for i in range(len(categories_numeric)):
    ax.scatter(categories_numeric[i], values[i][0], c='black', marker='o', label=sub_categories[0] if i == 0 else "")
    ax.scatter(categories_numeric[i], values[i][1], c='black', marker='x', label=sub_categories[1] if i == 0 else "")

# Customize the plot
ax.set_xlabel('Year')
ax.set_ylabel('Percentage')
ax.set_xticks(categories_numeric)  # Set x-ticks to be the years
ax.set_xticklabels(categories)  # Set x-tick labels to represent the years
ax.legend()  # Show legend

# Ensure y-axis reaches 40
ax.set_ylim([0, 40])

# Save plot
plt.savefig('scatter_plot.png', dpi=300)

# Show the plot
plt.show()