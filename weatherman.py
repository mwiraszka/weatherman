# WEATHERMAN
# by Michal Wiraszka

# Written fully in Python, making heavy use of its Tkinter module.
# 'Weatherman' requests information from Open Weather Map's API, and displays
# the city's current weather information using Python's Tkinter GUI.
# Based on a tutorial by Keith Galli. 

# --- Versions ---

# Current v1.0 has very limited functionality.
# 02.08.20 project resumed since last session; window formatting


import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import json

WINW = 500
WINH = 400
WHITE = '#FFFFFF'
BLACK = '#000000'
BLUE = '#80C1FF'
RED = '#DDAAAA'
F_TEXT = ('Helvetica', 16)
F_BUTTON = ('Helvetica', 20, "bold")


def button_click(entry):
	valid = check_entry(entry)
	if valid:
		valid_entry = " ".join(word.capitalize() for word in entry.split())
		all_ids = get_ids(valid_entry)
		if len(all_ids) == 0:
			output_text['text'] = 'Weatherman could not find ' +\
				valid_entry + ' in the database.'
		else:
			if len(all_ids) > 1:
				final_id = choose_country(valid_entry, str(len(all_ids)))
			else:
				final_id = all_ids[0][0]
			weather_data = get_weather(final_id)
			output_weather(weather_data)

def check_entry(entry):
	valid = False
	if (len(entry) == 0) or (all(char.isspace() for char in entry)):
		print ('Error 1: No input.')
		# Return to default message in the output box
		output_text['text'] = 'Please enter a city above.'
	elif len(entry) > 20:
		print ('Error 2: Too many characters.')
		output_text['text'] = 'Weatherman does not currently support city' +\
			' names\nwith more than 20 letters.'
	elif all(char.isalpha() or char.isspace() for char in entry) != True:
		print ('Error 3: Invalid characters.')
		output_text['text'] = 'Weatherman only understands letters.'
	else:
		valid = True
	return valid
		
def get_ids(valid_entry):
	with open('cities.json') as f:
 		cities = json.load(f)
	# A 2D-list [ID, country] to store all IDs for given city name
	all_ids = []
	for city in cities:
		if city['name'] == valid_entry:
			if len(all_ids) == 0:
				all_ids.append([city['id'], city['country']])
			# Check for country duplicates. Assuming all same city names within
			# a country refer to the same general location, skip those IDs.
			else:
				for item in range(len(all_ids)):
					# Country name already exists in list. Skip this ID.
					if city['country'] == all_ids[item][1]:
						break
					# End of loop and no duplicate found. Add this ID.
					elif item == (len(all_ids) - 1):	
						all_ids.append([city['id'], city['country']])
	return all_ids

def choose_country(city_name, num):
	output_text['text'] = 'Weatherman found ' + str(num) +\
		' cities called ' + str(city_name) + '.\n\nUnfortunately the' +\
		' functionality of choosing\na city from a list is not built in yet.'

def get_icon(icon_name):
	# Icon sized proportionally to window dimensions
	size = int(output_box.winfo_height() * 0.25)
	img = ImageTk.PhotoImage(Image.open('./icons/' +\
		icon_name + '.png').resize((size, size)))
	weather_icon.delete("all")
	weather_icon.create_image(0, 0, anchor='nw', image=img)
	weather_icon.image = img

def get_weather(city_id):
	url = 'https://api.openweathermap.org/data/2.5/weather'
	api_key = '2afa8f07bddea63ef2efbe6bf12fe17d'
	
	params = {'id': city_id, 'appid': api_key, 'units': 'metric'}
	response = requests.get(url, params=params)
	return response.json()

def output_weather(weather_data):
	try:
		city = weather_data['name']
		country = weather_data['sys']['country']
		desc = weather_data['weather'][0]['description']
		icon_name = weather_data['weather'][0]['icon']
	except:
		print ('Error 4: Problem retrieving data from Open Weather Map.')
	get_icon(icon_name)
	output_text['text'] = 'The weather in ' + str(city) + ', ' +\
		str(country) + ' is ' + str(desc) + '.'

def enter_key(event):
	button_click(entry_box.get())


app = tk.Tk()
app.title('Weatherman v1.0')
app.minsize(450, 360)
app.maxsize(600, 480)

win = tk.Canvas(app, width=WINW, height=WINH)
win.pack()

top_frame = tk.Frame(app, bg=BLACK, bd=3)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry_box = tk.Entry(top_frame)
entry_box.config(font=F_TEXT)
entry_box.place(relwidth=0.65, relheight=1)

button = tk.Button(top_frame, text="Let's Go!",
	command=lambda: button_click(entry_box.get()))
button.config(font=F_BUTTON, padx=20, pady=20)
button.place(relx=0.7, relwidth=0.3, relheight=1)
app.bind('<Return>', enter_key)

output_box = tk.Frame(app, bg=BLACK, bd=3)
output_box.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

output_text = tk.Label(output_box, anchor='nw', justify='left', bd=4)
output_text.config(font=F_TEXT)
output_text.place(relwidth=1, relheight=1)
output_text['text'] = 'Please enter a city above.'

weather_icon = tk.Canvas(output_text, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)


app.mainloop()