import matplotlib.pyplot as plt
import time
import tkinter as tk
from matplotlib.widgets import Button
from functools import partial
import numpy as np

current = 'area'

# Function for blackout effect
def blackout_effect(window):
    window.attributes('-fullscreen', True)
    window.configure(bg='black')
    window.update()
    time.sleep(1)
    window.configure(bg='white')
    window.attributes('-fullscreen', False)

# Function for handling button click event
def on_button_clicked(event):
    global start_time, current

    blackout_window = tk.Toplevel(fig.canvas.get_tk_widget().master)
    blackout_window.attributes('-alpha', 1.0)
    blackout_window.attributes('-topmost', True)
    blackout_effect(blackout_window)
    blackout_window.destroy()

    # Clear the current plot
    ax.clear()

    if current == 'line':
        # Generate random data for the stacked area chart
        x = [1, 2, 3, 4, 4.5, 5, 6]
        y1 = [2, 3, 5, 7, 4, 11, 8]
        y2 = [4, 1, 6, 4, 8, 9, 6]
        y3 = [5, 7, 4, 9, 7, 2, 8]

        # Plot the stacked area chart
        ax.stackplot(x, y1, y2, y3, labels=['A', 'B', 'C'])
        ax.legend(loc='upper left')
        ax.set_title('New Points')
        plt.draw()
        current = 'area'

    else:
        x = [1, 2, 3, 4, 4.5, 5, 6]
        y1 = [2, 3, 5, 7, 4, 11, 8]
        y2 = [4, 1, 6, 4, 8, 9, 6]
        y3 = [5, 7, 4, 9, 7, 2, 8]
        ax.plot(x, y1, label='USA')
        ax.plot(x, y2, label='UK')
        ax.plot(x, y3, label='China')
        ax.legend(loc='upper left')
        ax.set_title('Return To Line')
        plt.draw()
        current = 'line'

    start_time = time.time()

# Function for handling mouse click event
def onclick(event, pointX, pointY):
    global clicked, start_time
    if event.inaxes is not None and event.inaxes != button_ax and event.inaxes.figure == fig:
        print(f'Clicked on point ({event.xdata:.2f}, {event.ydata:.2f})')
        clicked = True
        if pointX - 0.08 < event.xdata < pointX + 0.08 and pointY - 0.22 < event.ydata < pointY + 0.27:
            print(f'Response Answer: Correct')
        else:
            print(f'Response Answer: Incorrect')
        response_time = time.time() - start_time
        print(f'Response time: {response_time:.2f} seconds')

# Create a figure and Axes object
fig, ax = plt.subplots()

# Define initial line chart data
x = [1, 2, 3, 4, 5]
y = [3, 3, 3, 3, 3]
line, = ax.plot(x, y, 'o-')

# Set Axes properties
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Set fullscreen and press Next to start')
ax.set_xlim(0, 8)
ax.set_ylim(0, 12)

# Set up event handling
clicked = False
start_time = None
specific_x = 2
specific_y = 3
onclick_specific = partial(onclick, pointX=specific_x, pointY=specific_y)
fig.canvas.mpl_connect('button_press_event', onclick_specific)

# Define the position and size of the button below the x-axis
button_ax = plt.axes([0.8, 0.01, 0.1, 0.05])

# Create the button and specify the label
button = Button(button_ax, 'Next')

# Attach the callback function to the button
button.on_clicked(on_button_clicked)

#fig.canvas.manager.full_screen_toggle()

start_time = time.time()
plt.show()
