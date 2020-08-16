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
# 15.08.20 background image to test proportional re-size option
# 15.08.20 button_click function - {} .format for text
# 15.08.20 clickable buttons for all displayed cities in sel_country & win re-sizing
# 15.08.20 __main__ tested (removed); window quit prompt
# 15.08.20 select_country fully functional now


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import json

WINW = 750
WINH = 375
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
			message = 'Weatherman could not find {} in the database.'.format(valid_entry)
			output_text(message)
		else:
			if len(all_ids) > 1:
				# While there are many cities in the world with the same name
				# (25 cities called Springfield in the US alone), there are
				# only ever 3 or fewer countries that share a city by the same
				# name in the vast majority of city names. The absolute longest
				# name found is 'Waterloo', which exists in 6 different countries.
				# We will assume no name is more popular and set the limit at 6.
				# This will ensure formatting and the amount of buttons that are
				# created never go out of range.
				del all_ids[6:]

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
				output_weather(weather_data)

def coordinates(num, entry):
	city_name = " ".join(word.capitalize() for word in entry.split())
	print(num)
	print(entry)



def check_entry(entry):
	valid = False
	if (len(entry) == 0) or (all(char.isspace() for char in entry)):
		print ('Error 1: No input.')
		message = 'Please enter a city.' # Revert to default message.
		output_text(message)
	elif len(entry) > 20:
		print ('Error 2: Too many characters.')
		message = 'Weatherman does not currently support city names' +\
					  '\nwith more than 20 letters.'
		output_text(message)
	elif all(char.isalpha() or char.isspace() for char in entry) != True:
		print ('Error 3: Invalid characters.')
		message = 'Weatherman only understands letters.'
		output_text(message)
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




def change_case(event=None):
    new_text = str.swapcase(lab["text"])
    lab.config(text=new_text)
    country_selected = True

def red_text(event=None):
    lab.config(fg="red")

def black_text(event=None):
    lab.config(fg="black")

def select_country(city_name, ids):
	message = 'Weatherman found {} cities named {}.\nPlease select one:\n\n'.format(
			str(len(ids)),
			str(city_name))
	output_text(message)
	
	# Create a button for every city found under that name, and format all frames'
	# and buttons' relative widths/heights/placements based on the amount of cities.
	choice_frame = tk.Frame(app, bg=BLUE, bd=3)
	choice_frame.place(relx=0.5,
					   rely=0.35,
					   relwidth=0.5,
					   relheight=0.05 + 0.08*len(ids),
					   anchor='n')
	for i in range(len(ids)):
		button = tk.Button(choice_frame, text= (str(city_name) + ", " + ids[i][1]),
					command=lambda i=i: button_click(entry_box.get(), i))
		button.config(font=F_BUTTON, padx=10, pady=10)
		button.place(relx=0.01,
					 rely=i/len(ids) + 0.01,
					 relwidth=0.98,
					 relheight=1/len(ids) - 0.02)

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
		message = 'The weather in {}, {} is {}.'.format(str(city),\
													    str(country),\
													    str(desc))
	except:
		print ('Error 4: Problem retrieving data from Open Weather Map.')
		message = 'Weatherman could not retrieve data and doesn\'t know why.'
	output_text(message)
	
	
	

def enter_key(event):
	button_click(entry_box.get())
	
def output_text(message, *args, **kwargs):
	output_box = tk.Frame(app, bg=BLACK, bd=3)
	output_box.place(relx=0.5, rely=0.22, relwidth=0.75, relheight=0.7, anchor='n')
	
	output = tk.Label(output_box, anchor='nw', justify='left', bd=4)
	output.config(font=F_TEXT)
	output.place(relwidth=1, relheight=1)
	output['text'] = message

def terminate():
    if messagebox.askokcancel(
    		"Quit", "Are you sure you wish to quit on Weatherman?"):
        app.destroy()




# -------- MAIN --------


# --- Window & Background
refresh = True
app = tk.Tk()
app.title('Weatherman v1.0')
app.minsize(700,350)
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
entry_box.place(relwidth=0.69, relheight=1)
output_text('Please enter a city.') # Default message

# --- Button ---
button = tk.Button(top_frame, text="Let's Go!",
		 	command=lambda: button_click(entry_box.get()))
button.config(font=F_BUTTON, padx=20, pady=20)
button.place(relx=0.7, relwidth=0.3, relheight=1)
app.bind('<Return>', enter_key)



# --- Weather Icon ---
#weather_icon = tk.Canvas(app, bd=0, highlightthickness=0)
#weather_icon.delete("all")
#img = ImageTk.PhotoImage(Image.open('./icons/' +\
		#icon_name + '.png').resize((size,size)))
#weather_icon.create_image(0, 0, anchor='nw', image=img)
#weather_icon.image = img
#weather_icon.place(relx=0.75, rely=0, relwidth=1, relheight=0.5)

app.protocol("WM_DELETE_WINDOW", terminate)


# --- Main Loop ---
app.mainloop()

