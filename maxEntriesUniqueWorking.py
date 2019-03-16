import clipboard
from pynput.keyboard import Controller, Key, KeyCode, Listener
# import pyautogui
import json

#path to the json file storing the clipboard data:
JSON_PATH = './clipboard_data/sample.json'

#max no of entries at any time in the clipboard(JSON_PATH):
MAX_ENTRIES = 10

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
	{Key.ctrl_l, Key.alt_r, KeyCode(char='c')},
    {Key.ctrl_r, Key.alt_l, KeyCode(char='c')},
    {Key.ctrl_r, Key.alt_r, KeyCode(char='c')}
]

TERMINAL_PASTE_COMBINATIONS = [
    {Key.shift, Key.ctrl, Key.alt, KeyCode(char='v')},
    {Key.shift, Key.ctrl_l, Key.alt_l, KeyCode(char='v')},
    {Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='v')},
    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='v')},
    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='v')}
]

TERMINAL_COPY_COMBINATIONS = [
	{Key.shift, Key.ctrl, KeyCode(char = 'p')},
	{Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='c')},
    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='c')},
    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='c')}
]

# The currently active modifiers
current = set()
kb_actor = Controller()


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
	print(current)
	
	#clipboard mei copy::
	clipboard.copy(data_json['records'][0]['text'])
	print('lol before gen event')
	
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

	print('lol after gen event')


def execute_copy():
	global prev_data
	copied_data = clipboard.paste()
	
	if not copied_data == prev_data: 
		write_to_json(copied_data)
		prev_data = copied_data


def on_press(key):
	if any([key in COMBO for COMBO in PASTE_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in PASTE_COMBINATIONS):
			print('ctrlV detected!')
			print(current)
			execute_paste(is_terminal = False)

	if any([key in COMBO for COMBO in TERMINAL_PASTE_COMBINATIONS]):
		current.add(key)
		if any(all(k in current for k in COMBO) for COMBO in TERMINAL_PASTE_COMBINATIONS):
			print('ctrlShiftV detected!')
			print(current)
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

	print(current)


def on_release(key):
	current.clear()

with Listener(on_press=on_press, on_release=on_release) as listener:
	listener.join()


'''
    ed the new shit!
^CTraceback (most recent call last):
  File "keyboard_clip_p1.py", line 129, in <module>
    listener.join()
  File "/usr/local/lib/python3.6/site-packages/pynput/_util/__init__.py", line 192, in join
    super(AbstractListener, self).join(*args)
  File "/usr/local


    '''