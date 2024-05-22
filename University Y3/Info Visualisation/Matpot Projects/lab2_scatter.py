import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

categories = ['2006', '2007', '2008', '2009', '2010']
sub_categories = ['Headingley Ward', 'Horsforth Ward', 'Hyde Park and Woodhouse Ward']
values = [ [100, 92, 79, None, 83], [180, 190, 225, None, 225], [720, 731, 721, None, 766]]  # values for each sub-category in each category

# Step 3: Calculate bar width and positions
num_categories = len(categories)
num_sub_categories = len(sub_categories)
total_width = 0.8
ind = np.arange(num_categories)
width = 0.4

# Step 4: Plot the bars
fig, ax = plt.subplots(figsize=(6, 4))

ax.scatter(categories, values[0], c='black', marker='o', label=sub_categories[0])
ax.scatter(categories, values[1], c='black', marker='x', label=sub_categories[1])
ax.scatter(categories, values[2], c='black', marker='^', label=sub_categories[2])

# Step 5: Customize the plot
plt.rcParams.update({'font.size': 11})

ax.set_xlabel('Year')
ax.set_ylabel('Number of In-Poverty Children')
ax.legend()

plt.savefig('lab2_scatter.png', dpi=300)

# Step 6: Show the plot
plt.show()