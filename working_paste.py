import clipboard
from pynput.keyboard import Controller, Key, KeyCode, Listener
import json

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

# The currently active modifiers
current = set()
kb_actor = Controller()

#read from json file::
data_json = []
with open('./clipboard_data/sample.json', 'rb') as f:
	data_json = json.load(f)['records']

def execute_paste():

	#empty the current set, since task will be executed now
	current.clear()
	print(current)

	#clipboard mei copy::
	clipboard.copy(data_json[0]['text'])
	print('lol before gen event')

	#emulate paste event::
	kb_actor.press(Key.ctrl)
	kb_actor.press(Key.shift)
	kb_actor.press('v')
	
	#empty the set of the keys added above:
	current.clear()

	kb_actor.release(Key.ctrl)
	kb_actor.release(Key.shift)
	kb_actor.release('v')

	print('lol after gen event')


def execute_copy():
	copied_data = clipboard.paste()


def on_press(key):
    if any([key in COMBO for COMBO in PASTE_COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in PASTE_COMBINATIONS):
        	print('ctrlV detected!')
        	print(current)
        	execute_paste()


    if any([key in COMBO for COMBO in COPY_COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COPY_COMBINATIONS):
        	print('ctrlC detected!')
        	execute_copy()
        	#empty the current set, since task has been executed now
        	current.clear()

def on_release(key):
	current.clear()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()