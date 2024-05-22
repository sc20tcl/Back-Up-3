
data_set  =  {'set_number': 5, 'countries': ['Germany', 'Italy', 'Brazil', 'USA', 'Japan'], 'years': [2004, 2008, 2012, 2016, 2020], 'line_chart_medals': {'Germany': [35, 71, 60, 55, 31], 'Italy': [24, 64, 61, 37, 65], 'Brazil': [37, 77, 73, 60, 33], 'USA': [64, 55, 78, 69, 61], 'Japan': [46, 20, 69, 21, 78]}, 'area_chart_medals': {'Germany': [46, 55, 49, 26, 72], 'Italy': [61, 23, 57, 66, 58], 'Brazil': [36, 51, 51, 68, 77], 'USA': [21, 56, 49, 49, 26], 'Japan': [71, 77, 63, 78, 56]}, 'title': 'Which country won the most medals overall?','CorrectLine':[(2004,64), (2008,55), (2012,78), (2016,69), (2020,61)], 'CorrectArea': [(2004,71),(2008,77),(2012,63),(2016,78),(2020,56)]}

clicked_point = (2012, 78)
print(data_set["CorrectLine"])

if clicked_point in data_set["CorrectLine"]:
    final_answer = "Correct"
else:
    final_answer = "InCorrect"

print(final_answer)