import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time
import csv
import os

chart_data_sets = [
    {'set_number': 1, 'countries': ['Gold', 'Silver', 'Bronze'], 'years': [2000, 2004, 2008, 2012, 2016], 'line_chart_medals': {'Gold': [42, 75, 64, 35, 48], 'Silver': [58, 46, 44, 57, 21], 'Bronze': [69, 68, 65, 59, 43]}, 'area_chart_medals': {'Gold': [74, 54, 27, 64, 46], 'Silver': [69, 50, 65, 49, 44], 'Bronze': [32, 77, 37, 75, 76]},'title': 'Which medal type was won the most in 1984?', 'CorrectLine':[(2000,69)], 'CorrectArea': [(2000,74)]},
    {'set_number': 2, 'countries': ['Gold', 'Silver', 'Bronze'], 'years': [2004, 2008, 2012, 2016, 2020], 'line_chart_medals': {'Gold': [49, 71, 27, 41, 66], 'Silver': [61, 74, 43, 70, 48], 'Bronze': [49, 27, 78, 36, 32]}, 'area_chart_medals': {'Gold': [32, 54, 44, 70, 57], 'Silver': [59, 80, 51, 80, 71], 'Bronze': [75, 60, 36, 26, 71]}, 'title': 'Which medal type was won the least in 2016?','CorrectLine':[(2016,36)], 'CorrectArea': [(2016,176)]},
    {'set_number': 3, 'countries': ['Gold', 'Silver', 'Bronze'], 'years': [2004, 2008, 2012, 2016, 2020], 'line_chart_medals': {'Gold': [72, 42, 73, 67, 77], 'Silver': [46, 49, 53, 45, 58], 'Bronze': [40, 77, 72, 53, 62]}, 'area_chart_medals': {'Gold': [58, 71, 25, 77, 72], 'Silver': [56, 26, 76, 70, 68], 'Bronze': [22, 69, 48, 18, 46]}, 'title': 'In 2016, which medal type had the greatest increase since 2000?','CorrectLine':[(2016,53)], 'CorrectArea': [(2016,147)]},
    {'set_number': 4, 'countries': ['China', 'Brazil', 'Canada', 'Great Britain', 'Australia'], 'years': [1996, 2000, 2004, 2008, 2012], 'line_chart_medals': {'China': [21, 79, 37, 32, 32], 'Brazil': [25, 60, 54, 51, 42], 'Canada': [67, 63, 80, 64, 52], 'Great Britain': [52, 71, 23, 23, 52], 'Australia': [65, 26, 30, 34, 60]}, 'area_chart_medals': {'China': [76, 28, 58, 63, 43], 'Brazil': [64, 29, 72, 53, 65], 'Canada': [59, 69, 23, 75, 69], 'Great Britain': [27, 66, 32, 40, 29], 'Australia': [33, 29, 24, 26, 33]}, 'title': 'Which country won the most medals in 2004?','CorrectLine':[(2004,80)], 'CorrectArea': [(2004,130)]},
    {'set_number': 5, 'countries': ['Germany', 'Italy', 'Brazil', 'USA', 'Japan'], 'years': [2004, 2008, 2012, 2016, 2020], 'line_chart_medals': {'Germany': [35, 71, 60, 55, 31], 'Italy': [24, 64, 61, 37, 65], 'Brazil': [37, 77, 73, 60, 33], 'USA': [64, 55, 78, 69, 61], 'Japan': [46, 20, 69, 21, 78]}, 'area_chart_medals': {'Germany': [46, 55, 49, 26, 72], 'Italy': [61, 23, 57, 66, 58], 'Brazil': [36, 51, 51, 68, 77], 'USA': [21, 56, 49, 49, 26], 'Japan': [71, 77, 63, 78, 56]}, 'title': 'Which country won the most medals overall?','CorrectLine':[(2004,64), (2008,55), (2012,78), (2016,69), (2020,61)], 'CorrectArea': [(2004,235),(2008,262),(2012,269),(2016,287),(2020,289)]},
    {"set_number": 6, "countries": ["Great Britain", "Brazil", "Australia", "Japan", "China"], "years": [1984, 1988, 1992, 1996, 2000], "line_chart_medals": {"Great Britain": [30, 50, 40, 60, 54], "Brazil": [45, 35, 50, 55, 60], "Australia": [40, 45, 55, 50, 35], "Japan": [60, 65, 55, 35, 40], "China": [35, 40, 60, 50, 55]}, "area_chart_medals": {"Great Britain": [57, 54, 69, 52, 53], "Brazil": [73, 77, 57, 33, 22], "Australia": [39, 78, 24, 23, 55], "Japan": [66, 53, 69, 47, 71], "China": [54, 32, 28, 21, 35]}, "title": "Which year has the highest number total of medals between the countries? \n (Select any data point for that year)", "CorrectLine": [(1992, 40), (1992, 50), (1992, 55), (1992, 55), (1992, 60)], "CorrectArea": [(1988, 54), (1988, 131), (1988, 209), (1988, 262), (1988, 294)]},
    {'set_number': 7, 'countries': ['Italy', 'Germany', 'Japan', 'Great Britain', 'USA'], 'years': [1992, 1996, 2000, 2004, 2008], 'line_chart_medals': {'Italy': [71, 51, 55, 59, 52], 'Germany': [27, 58, 58, 32, 48], 'Japan': [51, 70, 28, 40, 70], 'Great Britain': [27, 48, 82, 30, 46], 'USA': [45, 64, 54, 31, 44]}, 'area_chart_medals': {'Italy': [39, 29, 25, 69, 51], 'Germany': [56, 73, 27, 49, 41], 'Japan': [43, 39, 48, 71, 61], 'Great Britain': [51, 68, 27, 68, 41], 'USA': [45, 38, 28, 87, 25]}, 'title': 'Which country won the least medals in 1996?','CorrectLine':[(1996,48)], 'CorrectArea': [(1996,29)]},
    {'set_number': 8, 'countries': ['Germany', 'France', 'Brazil', 'Australia', 'Italy'], 'years': [1996, 2000, 2004, 2008, 2012], 'line_chart_medals': {'Germany': [32, 46, 68, 48, 45], 'France': [64, 52, 43, 65, 66], 'Brazil': [65, 76, 61, 53, 59], 'Australia': [78, 57, 20, 61, 48], 'Italy': [25, 41, 64, 63, 43]}, 'area_chart_medals': {'Germany': [30, 56, 57, 21, 23], 'France': [28, 73, 64, 59, 66], 'Brazil': [67, 47, 27, 29, 23], 'Australia': [29, 28, 31, 78, 50], 'Italy': [26, 26, 42, 57, 57]}, 'title': 'Which country won the second most medals in 2008?','CorrectLine':[(2008,63)], 'CorrectArea': [(2008,80)]},
    {'set_number': 9, 'countries': ['USA', 'Italy', 'Australia', 'Germany', 'France'], 'years': [1984, 1988, 1992, 1996, 2000], 'line_chart_medals': {'USA': [63, 71, 52, 29, 36], 'Italy': [41, 33, 63, 54, 72], 'Australia': [45, 77, 45, 28, 73], 'Germany': [76, 26, 46, 54, 55], 'France': [47, 58, 42, 25, 66]}, 'area_chart_medals': {'USA': [29, 39, 67, 25, 28], 'Italy': [45, 73, 26, 22, 47], 'Australia': [71, 55, 58, 50, 65], 'Germany': [83, 22, 21, 60, 75], 'France': [52, 40, 69, 25, 78]}, 'title': 'What was the highest medal total for a country in a single Olympics?','CorrectLine':[(1988,77)], 'CorrectArea': [(1984,228)]},
    {'set_number': 10, 'countries': ['China', 'USA', 'Japan', 'France', 'Germany'], 'years': [1984, 1988, 1992, 1996, 2000], 'line_chart_medals': {'China': [24, 36, 75, 52, 50], 'USA': [68, 51, 63, 33, 46], 'Japan': [44, 23, 38, 73, 80], 'France': [59, 69, 55, 25, 33], 'Germany': [44, 73, 27, 59, 54]}, 'area_chart_medals': {'China': [77, 69, 49, 72, 54], 'USA': [32, 63, 78, 37, 77], 'Japan': [59, 74, 61, 43, 56], 'France': [26, 38, 42, 43, 66], 'Germany': [38, 29, 40, 22, 44]}, 'title': 'What was the lowest total medal score for a country in a single Olympics?','CorrectLine':[(1988,23)], 'CorrectArea': [(1996,217)]},
]

questions = ['Which medal type was won the most in 2000?','Which medal type was won the least in 2016?', 'Which medal type had the highest increase from 2004-2016 \n (select the corresponding 2016 point)','Which country won the most medals in 2004?','Which country won the most medals overall?', 
             'Which year has the highest number total of medals between the countries? \n (Select any data point for that year)','Which country won the least medals in 1996?','Which country won the second most medals in 2008?','What was the highest medal total for a country in a single Olympics?',
             'What was the lowest total medal score for a country in a single Olympics?']

start_time = 0
click_count = 0
final_answer = ""
trial_data = []
question_number = 0
click_text = None



def display_graph(data_set, chart_type, ax, fig):
    global start_time, click_count, last_clicked_point, final_answer
    start_time = time.time()
    print("time start")
    click_count = 0
    last_clicked_point = None
    final_answer = ""
    ax.clear()

    global click_text
    click_text = ax.text(0.5, 0.75, "", transform=ax.transAxes, ha="center", va="center")

    # Create copies of the callback keys to avoid RuntimeError during iteration
    motion_notify_cids = list(fig.canvas.callbacks.callbacks.get('motion_notify_event', {}).keys())
    pick_event_cids = list(fig.canvas.callbacks.callbacks.get('pick_event', {}).keys())

    # Disconnect any existing event handlers
    for cid in motion_notify_cids:
        fig.canvas.mpl_disconnect(cid)
    for cid in pick_event_cids:
        fig.canvas.mpl_disconnect(cid)

    countries = data_set["countries"]
    years = data_set["years"]
    medals = data_set[f"{chart_type}_chart_medals"]


    lines = []
    scatter_plots = []
    if chart_type == "line":
        # Plotting line charts
        for country in countries:
            line, = ax.plot(years, medals[country], label=country, marker='o', picker=True, pickradius=5)
            lines.append(line)

        def on_hover(event):
            for line in lines:
                if line.contains(event)[0]:
                    line.set_linewidth(4)  # Highlight the line
                else:
                    line.set_linewidth(2)  # Reset the line width
            fig.canvas.draw_idle()

        def on_click(event):
            global click_count, final_answer
            click_count += 1
            print("click")
            if isinstance(event.artist, plt.Line2D):
                line = event.artist
                x, y = line.get_data()
                ind = event.ind
                clicked_point = (x[ind][0], y[ind][0])
                print("Clicked point", clicked_point)
                print("Correct answer: ", data_set["CorrectLine"])
                if clicked_point in data_set["CorrectLine"]:
                    final_answer = "Correct"
                else:
                    final_answer = "Incorrect"
            
            ax.text(0.5, 0.95, "Answer Selected", transform=ax.transAxes, ha="center", fontsize=12, color='blue')
            fig.canvas.draw_idle()
                

        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('pick_event', on_click)

    else:
        # Plotting area charts with scatter points
        prev_values = [0] * len(years)
        for country in countries:
            area = ax.fill_between(years, prev_values, [x + y for x, y in zip(prev_values, medals[country])],
                                   label=country, alpha=0.5)
            scatter = ax.scatter(years, [x + y for x, y in zip(prev_values, medals[country])], s=30, picker=True)
            scatter_plots.append((scatter, area))
            prev_values = [x + y for x, y in zip(prev_values, medals[country])]

        def on_hover(event):
            for scatter, area in scatter_plots:
                if scatter.contains(event)[0]:
                    area.set_alpha(0.7)  # Increase saturation
                else:
                    area.set_alpha(0.5)  # Reset saturation
            fig.canvas.draw_idle()

        def on_click(event):
            global click_count, final_answer
            click_count += 1
            print("click")
            # click_text.set_text("Answer Selected")
            # fig.canvas.draw_idle()
            for scatter, _ in scatter_plots:
                cont, ind = scatter.contains(event.mouseevent)
                if cont:
                    x_clicked, y_clicked = scatter.get_offsets()[ind["ind"][0]]
                    clicked_point = (int(x_clicked), int(y_clicked))
                    print("Clicked point", clicked_point)
                    print("Correct answer: ", data_set["CorrectArea"])
                    if clicked_point in data_set["CorrectArea"]:
                        final_answer = "Correct"
                    else:
                        final_answer = "Incorrect"
            ax.text(0.5, 0.95, "Answer Selected", transform=ax.transAxes, ha="center", fontsize=12, color='blue')
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('pick_event', on_click)

    ax.set_xticks(data_set["years"]) 
    ax.set_xlabel('Olympic Year')
    ax.set_ylabel('Medals')
    ax.set_title(questions[question_number-1])
    ax.legend()



def display_question_page(ax):
    ax.clear()
    ax.text(0.5, 0.5, questions[question_number], fontsize=20, ha='center', va='center')
    ax.axis('off')

def intro_page(ax):
    ax.clear()
    ax.text(0.5, 0.7, "Welcome To Our Chart Survey", fontsize=20, ha='center', va='center')
    ax.text(0.5, 0.4, "For each question answer the question as best as you can, clicking the data point that you think best fits the question.\n You can choose as many times as you like but when you are happy with you answer click 'Next Page'. \n For Questions not asking about a specfic year you may select any data point on the corresponding plot.", fontsize=12, ha='center', va='center')
    ax.axis('off')

def main():
    
    fig = plt.figure(figsize=(13.33, 8))  # Set the size of the window

    ax_chart = fig.add_subplot(111)
    ax_chart_position = ax_chart.get_position()

    ax_chart.set_position([ax_chart_position.x0, ax_chart_position.y0 + 0.1, 
                           ax_chart_position.width, ax_chart_position.height - 0.1])

    ax_button = fig.add_axes([0.81, 0.01, 0.1, 0.075])
    button = Button(ax_button, 'Next Page')

    current_set = 0
    current_chart = "title"

    def save_trial_data_to_file(data):
        file_exists = os.path.isfile('trial_data.csv')
        with open('trial_data1.csv', 'a', newline='') as file:  # 'a' mode for appending data
            fieldnames = ["Question", "Chart", "Final Answer", "Time Taken", "Answer Changed"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # Write headers only if file doesn't exist

            writer.writerows(data)
        
        print("Data appended to trial_data.csv")

    def next_chart(event):
        global question_number
        nonlocal current_set, current_chart
        if (current_chart != "question") and (current_chart != "title"):
            trial_result = {
            "Question" : question_number,
            "Chart" : current_chart,
            "Final Answer": final_answer,
            "Time Taken": time.time() - start_time,
            "Answer Changed": click_count - 1
            }
            print(trial_result)
            trial_data.append(trial_result)
            
        if current_chart == "title":
            current_chart = "question"
            display_question_page(ax_chart)
        elif current_chart == "question":
            question_number += 1
            current_chart = "line"
            display_graph(chart_data_sets[current_set], current_chart, ax_chart, fig)
        elif current_chart == "line":
            current_chart = "area"
            display_graph(chart_data_sets[current_set], current_chart, ax_chart, fig)
        elif current_chart == "area":
            current_set += 1
            current_chart = "question"
            if current_set < len(chart_data_sets):
                display_question_page(ax_chart)
            else:
                plt.close()
            if question_number == 10:
                save_trial_data_to_file(trial_data)
                print("*** Saved Data ***")
        fig.canvas.draw_idle()
        

    button.on_clicked(next_chart)

    intro_page(ax_chart)
    plt.show()
    


# Call main function to start the display
main()
