import subprocess
import time

def get_window_data():
	''' Gets the position and size of a window '''
	window_list = []
	# Empty list to store all of our windows' data
	
	result = subprocess.run(['wmctrl', '-lG'], stdout=subprocess.PIPE)
	# Gets information about the current "open" windows
	windows = result.stdout.decode('utf-8')
	# Decodes the windows so we can properly read them
	
	for line in windows.splitlines():
		# All of the windows are grouped together in lines, so go through each line to extract the data
		
		parts = line.split()
		# We need to split each line by the spaces containing the data
		
		window_data = {
			'id' : parts[0],
			'desktop' : parts[1],
			'x' : int(parts[2]),
			'y' : int(parts[3]),
			'width' : int(parts[4]),
			'height' : int(parts[5]),
			'title' : ' '.join(parts[7:])
		}
		# Gets all the relevant data parts
		
		window_list.append(window_data)
		# Add the window data to the list
		
	return window_list

def change_window(window_id, x, y, width, height, modify):
	''' Changes the properties of a window (height, width, position) '''
	
	if modify:
		subprocess.run(['xdotool', 'windowunmap', window_id])
		subprocess.run(['xdotool', 'windowmap', window_id])
		# Makes the windows minimized
		# Be careful with this: you can end up minimizing the task bar and desktop!
	
	subprocess.run(['wmctrl', '-i', '-r', window_id, '-e', f'10,{x},{y},{width},{height}'])
	# Move the appropriate window to where we want it to go, and set its height/width to what we want
	# If we want to not change any of the values, use -1
	

def return_window_id(name, windows, restrictions=None):
	''' Search through window names and get the corresponding id back '''
	for win in windows:
		# Go through the windows list
		if restrictions:
			if name in win['title'] and restrictions not in win['title']:
				return win['id']
		else:		
			if name in win['title']:
				# If we find a match to the name, return its ID
				return win['id']
			
	# If we find nothing, return None
	return None

def OpenPDF(ID):
	''' Opens a specified poster by using its ID '''
	path = "/home/iau/Desktop/Posters/PDFs/"
	poster_id = f"submission_{ID}.pdf"
	
	command = f'chromium-browser --new-window {path + poster_id}'
	
	subprocess.Popen(command, shell=True)
7
### INPUT CODE ###
if __name__ == "__main__":
	max_width = 1920
	max_height = 1080

	pdf = input("Please enter a poster ID:\n")
	OpenPDF(pdf)
	
	time.sleep(1)
	windows = get_window_data()
	for win in windows:
		print(win)

	poster_window = return_window_id("Chromium", windows, "Zoom" )
    
	meeting_window = return_window_id("Zoom", windows)
    # This needs to be changed, since it likely won't be that

	change_window(poster_window, int(0.25 * max_width), 60, int(0.8 * max_width), max_height, False)
	change_window(meeting_window, 0, 60, int(0.2 * max_width), max_height, False)
