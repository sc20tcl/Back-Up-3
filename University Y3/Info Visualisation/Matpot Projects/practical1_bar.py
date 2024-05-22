import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

categories = ['2011', '2012']
sub_categories = ['% men', '% women']
values = [[15.1, 28.3], [25.2, 30.0]]  # values for each sub-category in each category

# Step 3: Calculate bar width and positions
num_categories = len(categories)
num_sub_categories = len(sub_categories)
total_width = 0.8
ind = np.arange(num_categories)
width = 0.4

# Step 4: Plot the bars
fig, ax = plt.subplots(figsize=(6, 4))

for i in range(num_sub_categories):
    bar_positions = ind + i * width
    ax.bar(bar_positions, [val[i] for val in values], width, label=sub_categories[i])


# Step 5: Customize the plot
plt.rcParams.update({'font.size': 11})

ax.set_xlabel('Year')
ax.set_ylabel('Percentage')
ax.set_xticks(ind + total_width / num_sub_categories / 2)
ax.set_xticklabels(categories)
ax.legend()

ax.set_ylim([None, 40])

plt.savefig('bar_chart.png', dpi=300)

# Step 6: Show the plot
plt.show()
