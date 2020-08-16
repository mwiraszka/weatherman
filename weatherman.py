# WEATHERMAN
# by Michal Wiraszka

# Written fully in Python, making heavy use of its Tkinter module.
# 'Weatherman' requests information from Open Weather Map's API, and displays
# the city's current weather information using Python's Tkinter GUI.
# Based on a tutorial by Keith Galli. 

# --- Versions ---

# Current v1.0 - MVP only
# 02.08.20 project resumed since last session; window formatting
# 02.08.20 identify countries of same-name cities if more than one exists
# 03.08.20 simplifying code in a few places with {} string output notation
# 15.08.20 background image to test proportional re-size option
# 15.08.20 button_click function - {} .format for text
# 15.08.20 clickable buttons for all displayed cities in sel_country & win re-sizing
# 15.08.20 __main__ tested (removed); window quit prompt
# 15.08.20 select_country fully functional now
# 15.08.20 display more weather information; import datetime and math for time calculations
# 16.08.20 display img icons, country codes conversion & final touches!

import datetime
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import json

WINW = 700
WINH = 365
WHITE = '#FFFFFF'
BLACK = '#000000'
BLUE = '#80C1FF'
RED = '#DDAAAA'
F_TEXT = ('Helvetica', 16)
F_BUTTON = ('Helvetica', 20, "bold")


def button_click(entry, country_selection=None):
	valid = check_entry(entry)
	single_city_found = False
	if valid:
		valid_entry = " ".join(word.capitalize() for word in entry.split())
		all_ids = get_ids(valid_entry)
		if len(all_ids) == 0:
			output_text(f'Weatherman could not find {valid_entry} in the database.')
		else:
			if len(all_ids) > 1:
				if country_selection != None:
					final_id = all_ids[country_selection][0]
					single_city_found = True
				else:
					select_country(valid_entry, all_ids)
			else:
				final_id = all_ids[0][0]
				single_city_found = True
			if single_city_found:
				weather_data = get_weather(final_id)
				icon_name = output_weather(weather_data)


def check_entry(entry):
	valid = False
	if (len(entry) == 0) or (all(char.isspace() for char in entry)):
		print ('Error 1: No input.')
		output_text('Please enter a city.')  # Revert to default message.
	elif len(entry) > 20:
		print ('Error 2: Too many characters.')
		output_text('Weatherman does not support city names with more than 20 letters.')
	elif all(char.isalpha() or char.isspace() for char in entry) != True:
		print ('Error 3: Invalid characters.')
		output_text('Weatherman only understands letters.')
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


def select_country(city_name, ids):
	output_text(f'Weatherman found {len(ids)} cities named {city_name}.\nSelect one:\n\n')
	
	with open('country_codes.json') as f:
 		codes = json.load(f)
	
	# Create a button for every city found under that name, and format all frames'
	# and buttons' relative widths/heights/placements based on the amount of cities.
	choice_frame = tk.Frame(app, bg=BLUE, bd=3)
	choice_frame.place(relx=0.5,
					   rely=0.35,
					   relwidth=0.5,
					   relheight=0.08*len(ids)+0.05,
					   anchor='n')
	for i in range(len(ids)):
		ctry_name = str(ids[i][1])
		for j in range(len(codes)):
			# Replace two-letter country codes where possible
			if str(ids[i][1]) == codes[j]['Code']:
				ctry_name = codes[j]['Name']
				
		button = tk.Button(choice_frame, text= (str(city_name) + ", " + ctry_name),
					command=lambda i=i: button_click(entry_box.get(), i))
		button.config(font=F_BUTTON, padx=10, pady=10)
		button.place(relx=0.01,
					 rely=i/len(ids)+0.01,
					 relwidth=0.98,
					 relheight=1/len(ids)-0.02)


def get_weather(city_id):
	url = 'https://api.openweathermap.org/data/2.5/weather'
	api_key = '2afa8f07bddea63ef2efbe6bf12fe17d'
	
	params = {'id': city_id, 'appid': api_key, 'units': 'metric'}
	response = requests.get(url, params=params)
	return response.json()


def output_weather(weather_data):
	try:
		# Retrieve all data from weather_data nested dictionaries
		city = weather_data['name']
		ctry = weather_data['sys']['country']
		desc = weather_data['weather'][0]['description']
		temp = weather_data['main']['temp']
		feels_like = weather_data['main']['feels_like']
		low_temp = weather_data['main']['temp_min']
		high_temp = weather_data['main']['temp_max']
		humidity = weather_data['main']['humidity']
		pressure = weather_data['main']['pressure']
		icon_name = weather_data['weather'][0]['icon']
		dt_calc = datetime.datetime.fromtimestamp(weather_data['dt'])
		dt_sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
		dt_sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
		dt_diff = math.ceil(((datetime.datetime.now() - dt_calc).seconds) / 60)
		deg = u'\N{DEGREE SIGN}'
		bul = u'\u2022'
		
		# Alter first line based on how many minutes have passed (dt_diff)
		if dt_diff > 1 and dt_diff < 60:
			l1 = f' As of {dt_calc.date()} at {dt_calc.hour:02}:{dt_calc.minute:02}' +\
			     f' ({dt_diff} minutes ago)...'
		elif dt_diff == 1:
			l1 = f' As of {dt_calc.date()} at {dt_calc.hour:02}:{dt_calc.minute:02}' +\
			     f' (< {dt_diff} minute ago)...'
		else:
			l1 = f' As of {dt_calc.date()} at {dt_calc.hour:02}:{dt_calc.minute:02}...'
		
		# Amalgamate remainder of lines into a single message
		l2 = f' The weather in {city}, {ctry} is {temp:.1f}{deg}C and {desc}.'
		l3 = ' Additional info:'
		l4 = f' {bul} Feels like: {feels_like:.1f}{deg}C'
		l5 = f' {bul} Today\'s low: {high_temp:.1f}{deg}C'
		l6 = f' {bul} Today\'s high: {low_temp:.1f}{deg}C'
		l7 = f' {bul} Humidity: {humidity}%'
		l8 = f' {bul} Pressure: {(pressure/10)}kPa'
		l9 = f' {bul} Sunrise at: {dt_sunrise.hour:02}:{dt_sunrise.minute:02}'
		l10 = f' {bul} Sunset at: {dt_sunset.hour:02}:{dt_sunset.minute:02}'
		message = l1+'\n\n'+l2+'\n\n'+l3+'\n\n'+\
				  l4+'\n'+l5+'\n'+l6+'\n'+l7+'\n'+l8+'\n'+l9+'\n'+l10
	except:
		print ('Error 4: Problem retrieving data from Open Weather Map.')
		message = 'Weatherman could not retrieve data and doesn\'t know why.'
	output_text(message, icon_name)
	
	
	
def enter_key(event):
	# Pressing the Enter key is equivalent to clicking the button.
	button_click(entry_box.get())


def output_text(message, img=None):
	output_box = tk.Frame(app, bg=BLACK, bd=3)
	output_box.place(relx=0.5, rely=0.22, relwidth=0.75, relheight=0.7, anchor='n')
	
	output = tk.Label(output_box, anchor='nw', justify='left', bd=4)
	output.config(font=F_TEXT)
	output.place(relwidth=1, relheight=1)
	output['text'] = message

	if img != None:
		icon_url = './icons/' + img + '.png'
		temp = Image.open(icon_url)
		icon_img = ImageTk.PhotoImage(temp)
		icon_box = tk.Frame(app, bg=BLACK, bd=3)
		icon_box.place(relx=0.86, rely=0.24, width=80, height=80, anchor='ne')

		weather_icon = tk.Canvas(icon_box, bd=0, highlightthickness=0)
		weather_icon.create_image(10, 10, anchor='nw', image=icon_img)
		weather_icon.image = icon_img
		weather_icon.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)


def terminate():
    if messagebox.askokcancel(
    		"Quit", "Are you sure you want to abandon Weatherman?"):
        app.destroy()



# -------- MAIN ----------------
# --- Window & Background ---
refresh = True
app = tk.Tk()
app.title('Weatherman v1.0')
app.minsize(700,365)
app.maxsize(800,400)
win = tk.Canvas(app, width=WINW, height=WINH)
bg_img = tk.PhotoImage(file='bg.png')
bg_label = tk.Label(app, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
win.pack()

# --- Top Frame ---
top_frame = tk.Frame(app, bg=BLACK, bd=3)
top_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# --- Entry Box & Output Box ---
entry_box = tk.Entry(top_frame)
entry_box.config(font=F_TEXT)
entry_box.place(relwidth=0.49, relheight=1)
output_text('Please enter a city.') # Default message

# --- Button ---
button = tk.Button(top_frame, text="Go Go Weatherman!",
		 	command=lambda: button_click(entry_box.get()))
button.config(font=F_BUTTON)
button.place(relx=0.5, relwidth=0.5, relheight=1)
app.bind('<Return>', enter_key)

# --- Red circle in corner of window is clicked
app.protocol("WM_DELETE_WINDOW", terminate)

# --- Main Loop ---
app.mainloop()

