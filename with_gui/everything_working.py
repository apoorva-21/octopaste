import clipboard
from pynput.keyboard import Controller, Key, KeyCode, Listener
import json
from tkinter import *
import time

#path to the json file storing the clipboard data:
JSON_PATH = './sample.json'

#max no of entries at any time in the clipboard(JSON_PATH):
MAX_ENTRIES = 10

# max no of characters that will appear in a single line of the dropdown menu
MAX_TEXT_LEN = 20

# The key combination to check::
PASTE_COMBINATIONS = [
    {Key.ctrl, Key.alt, KeyCode(char='v')},
    {Key.ctrl_l, Key.alt_l, KeyCode(char='v')},
    {Key.ctrl_l, Key.alt_r, KeyCode(char='v')},
    {Key.ctrl_r, Key.alt_l, KeyCode(char='v')},
    {Key.ctrl_r, Key.alt_r, KeyCode(char='v')}
]

COPY_COMBINATIONS = [
	{Key.ctrl, KeyCode(char = 'c')},
	{Key.ctrl_l, Key.alt_l, KeyCode(char='c')},
	{Key.ctrl_l, Key.alt_r, KeyCode(char='c')},
    {Key.ctrl_r, Key.alt_l, KeyCode(char='c')},
    {Key.ctrl_r, Key.alt_r, KeyCode(char='c')}
]

CUT_COMBINATIONS = [
	{Key.ctrl, KeyCode(char = 'x')},
	{Key.ctrl_l, Key.alt_l, KeyCode(char='x')},
	{Key.ctrl_l, Key.alt_r, KeyCode(char='x')},
    {Key.ctrl_r, Key.alt_l, KeyCode(char='x')},
    {Key.ctrl_r, Key.alt_r, KeyCode(char='x')}
]

TERMINAL_PASTE_COMBINATIONS = [
    {Key.shift, Key.ctrl, Key.alt, KeyCode(char='V')},
    {Key.shift, Key.ctrl_l, Key.alt_l, KeyCode(char='V')},
    {Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='V')},
    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='V')},
    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='V')}
]

TERMINAL_COPY_COMBINATIONS = [
	{Key.shift, Key.ctrl, KeyCode(char = 'C')},
	{Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='C')},
	{Key.shift, Key.ctrl_l, Key.alt_l, KeyCode(char='C')},
    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='C')},
    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='C')}
]

# The currently active modifiers
current = set()
kb_actor = Controller()
listener = None

#to store the previous copied data, to prevent redundant entries:
prev_data = ''

#read from json file::
data_json = []
with open(JSON_PATH, 'rb') as f:
	data_json = json.load(f)

def write_to_json(data):
	data_json['records'].append({'text' : data})

	#remove entries in FCFS manner::
	if len(data_json['records']) > MAX_ENTRIES : 
		data_json['records'].pop(0)
	
	with open(JSON_PATH, 'w') as f:
		json.dump(data_json, f)
	print('Dumped the new shit!')

def execute_paste(is_terminal = False):
	#empty the current set, since task will be executed now
	current.clear()
	
	# open the dropdown menu
	dropDown(is_terminal)

	# #clipboard mei copy::
	# clipboard.copy(data_json['records'][0]['text'])
	# print('lol before gen event')
	
	# print('lol after gen event')


def execute_copy():
	global prev_data
	copied_data = clipboard.paste()
	
	if not copied_data == prev_data: 
		write_to_json(copied_data)
		prev_data = copied_data

	# Update dropdown
	# with open(JSON_PATH, 'rb') as f:
	# 	data_json = json.load(f)
	# 	for index, element in enumerate(data_json['records']):
	# 		Lb1.insert(index, element['text'][:MAX_TEXT_LEN])


def dropDown(is_terminal = False):    
	def handle_focus(event):
		if event.widget == top:
			top.focus_set()
			Lb1.focus_set()

	def return_pressed(event):
		to_be_put_in_clipboard = ''
		with open(JSON_PATH, 'rb') as f:
			data_json = json.load(f)
			for i in Lb1.curselection():
				to_be_put_in_clipboard += data_json['records'][i]['text']
		clipboard.copy(to_be_put_in_clipboard)

		print(to_be_put_in_clipboard)

		# # emulate alt+tab
		kb_actor.press(Key.alt)
		kb_actor.press(Key.tab)
		kb_actor.release(Key.alt)
		kb_actor.release(Key.tab)
		
		# Lb1.focus_set(takefocus=0)
		top.destroy()
		time.sleep(.1)
		#emulate paste event, is_terminal will only decide if shift key is to be emulated::	
		kb_actor.press(Key.ctrl)
		if is_terminal:
			kb_actor.press(Key.shift)
		kb_actor.press('v')
		
		current.clear()

		kb_actor.release(Key.ctrl)
		if is_terminal:
			kb_actor.release(Key.shift)
		kb_actor.release('v')

	top = Tk()
	Lb1 = Listbox(top, selectmode = EXTENDED)
	
	with open(JSON_PATH, 'rb') as f:
		data_json = json.load(f)
		for index, element in enumerate(data_json['records']):
			Lb1.insert(index, element['text'][:MAX_TEXT_LEN])

	Lb1.bind("<Return>", return_pressed)
	Lb1.pack()

	top.bind("<FocusIn>", handle_focus)
	top.mainloop()

def on_press(key):
	if any([key in COMBO for COMBO in PASTE_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in PASTE_COMBINATIONS):
			print('ctrlV detected!')
			# print(current)
			execute_paste(is_terminal = False)

	if any([key in COMBO for COMBO in TERMINAL_PASTE_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in TERMINAL_PASTE_COMBINATIONS):
			print('ctrlShiftV detected!')
			# print(current)
			execute_paste(is_terminal = True)

	if any([key in COMBO for COMBO in COPY_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in COPY_COMBINATIONS):
			print('ctrlC detected!')
			execute_copy()
			#empty the current set, since task has been executed now
			current.clear()


	if any([key in COMBO for COMBO in TERMINAL_COPY_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in TERMINAL_COPY_COMBINATIONS):
			print('ctrlShiftC detected!')
			execute_copy()
			#empty the current set, since task has been executed now
			current.clear()

	if any([key in COMBO for COMBO in CUT_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in CUT_COMBINATIONS):
			print('ctrlX detected!')
			execute_copy()
			#empty the current set, since task has been executed now
			current.clear()

	# print(current)


def on_release(key):
	current.clear()

with Listener(on_press=on_press, on_release=on_release) as listener:
	listener.join()


'''
    ed the new shit!
^CTraceback (most recent call last):
  File "keyboard_clip_p1.py", line 129, in <module>
    listener.join()
  File "/usr/local/lib/python3.6/site-va89-HP ~/Desktop/MUM_HACK/Octopaste $ python3 keyboard_clip_p1.py 
  File "keyboard_clip_p1.py", line 111
    if any([key in COMBO for COMBO in TERMINAL_PASTE_COMBINATIONS]):
                        '''