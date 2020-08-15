# WEATHERMAN
# by Michal Wiraszka

# Written fully in Python, making heavy use of its Tkinter module.
# 'Weatherman' requests information from Open Weather Map's API, and displays
# the city's current weather information using Python's Tkinter GUI.
# Based on a tutorial by Keith Galli. 

# --- Versions ---

# Current v1.0 - MVP
# 02.08.20 project resumed since last session; window formatting
# 02.08.20 identify countries of same-name cities if more than one exists
# 03.08.20 simplifying code in a few places with {} string output notation
# 15.08.20 background image to test re-size options


import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import json

WINW = 800
WINH = 400
WHITE = '#FFFFFF'
BLACK = '#000000'
BLUE = '#80C1FF'
RED = '#DDAAAA'
F_TEXT = ('Helvetica', 16)
F_BUTTON = ('Helvetica', 20, "bold")


def button_click(entry):
	valid = check_entry(entry)
	single_city_found = False
	if valid:
		valid_entry = " ".join(word.capitalize() for word in entry.split())
		all_ids = get_ids(valid_entry)
		if len(all_ids) == 0:
			output_text['text'] = 'Weatherman could not find ' +\
				valid_entry + ' in the database.'
		else:
			if len(all_ids) > 1:
				final_id = choose_country(valid_entry, all_ids)
			else:
				final_id = all_ids[0][0]
				single_city_found = True
			if single_city_found:
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

def choose_country(city_name, ids):
	txt1 = 'Weatherman found {} cities named {}.\nPlease select one:\n\n'.format(
			str(len(ids)),
			str(city_name))
	txt2 = ''
	for i in range(len(ids)):
		txt2 = txt2 + (ids[i][1] + '\n')
	output_text['text'] = txt1 + txt2
	

def get_icon(icon_name):
	# Icon sized proportionally to window dimensions
	size = int(output_box.winfo_height() * 0.25)
	img = ImageTk.PhotoImage(Image.open('./icons/' +\
		icon_name + '.png').resize((size,size)))
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
		get_icon(icon_name)
		txt = 'The weather in {}, {} is {}.'.format(str(city),
													str(country),
													str(desc))
		output_text['text'] = txt
	except:
		print ('Error 4: Problem retrieving data from Open Weather Map.')
	

def enter_key(event):
	button_click(entry_box.get())


app = tk.Tk()
app.title('Weatherman v1.0')
app.minsize(600,300)
app.maxsize(800,400)

win = tk.Canvas(app, width=WINW, height=WINH)
bg_img= tk.PhotoImage(file='bg.png')
bg_label = tk.Label(app, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
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