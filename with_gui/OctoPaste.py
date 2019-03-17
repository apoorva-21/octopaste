from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode, Listener
import json
import time
import platform
import clipboard
from tkinter import *
from tkinter import font
import os

class OctoPaste:

	def __init__(self):
		# path to the json file storing the clipboard data:
		self.JSON_PATH = './clipboard_data.json'

		#max no of entries at any time in the clipboard(JSON_PATH):
		self.MAX_ENTRIES = 10

		# max no of characters that will appear in a single line of the dropdown menu
		self.MAX_TEXT_LEN = 20

		self.prev_data = ''
		# The key combination to check
		self.PASTE_COMBINATIONS = [
		    {Key.ctrl, Key.alt, KeyCode(char='b')},
		    {Key.ctrl_l, Key.alt_l, KeyCode(char='b')},
		    {Key.ctrl_l, Key.alt_r, KeyCode(char='b')},
		    {Key.ctrl_r, Key.alt_l, KeyCode(char='b')},
		    {Key.ctrl_r, Key.alt_r, KeyCode(char='b')}
		]

		self.COPY_COMBINATIONS = [
			{Key.ctrl, KeyCode(char = 'c')},
			{Key.ctrl_l, KeyCode(char='c')},
		    {Key.ctrl_r, KeyCode(char='c')}
		]

		self.CUT_COMBINATIONS = [
			{Key.ctrl, KeyCode(char = 'x')},
			{Key.ctrl_l, KeyCode(char='x')},
		    {Key.ctrl_r, KeyCode(char='x')}
		]

		self.TERMINAL_PASTE_COMBINATIONS = [
		    {Key.shift, Key.ctrl, Key.alt, KeyCode(char='B')},
		    {Key.shift, Key.ctrl_l, Key.alt_l, KeyCode(char='B')},
		    {Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='B')},
		    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='B')},
		    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='B')}
		]

		self.TERMINAL_COPY_COMBINATIONS = [
			{Key.shift, Key.ctrl, KeyCode(char = 'C')},
			{Key.shift, Key.ctrl_l, Key.alt_r, KeyCode(char='C')},
			{Key.shift, Key.ctrl_l, Key.alt_l, KeyCode(char='C')},
		    {Key.shift, Key.ctrl_r, Key.alt_l, KeyCode(char='C')},
		    {Key.shift, Key.ctrl_r, Key.alt_r, KeyCode(char='C')}
		]

		# The currently active modifiers
		self.current = set()
		self.buffer = None
		self.fileName = 'TestFile.txt'
		self.top = None
		self.Lb1 = None

		#read from json file if it exists::
		if not os.path.exists(self.JSON_PATH):
			with open(self.JSON_PATH, 'w') as f:
				f.write('{"records": []}')

		self.data_json = []
		with open(self.JSON_PATH, 'rb') as f:
			self.data_json = json.load(f)

		self.kb_actor = Controller()

		with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
		    listener.join()




	def handle_focus(self, event):
		if event.widget == self.top:
			self.top.focus_set()
			self.Lb1.focus_set()

	def dropDown(self, is_terminal = False):
		def return_pressed(event):
			to_be_put_in_clipboard = ''
			with open(self.JSON_PATH, 'rb') as f:
				self.data_json = json.load(f)
				for i in self.Lb1.curselection():
					to_be_put_in_clipboard += self.data_json['records'][i]['text']
			clipboard.copy(to_be_put_in_clipboard)

			##print(to_be_put_in_clipboard)

			# # emulate alt+tab
			self.kb_actor.press(Key.alt)
			self.kb_actor.press(Key.tab)
			self.kb_actor.release(Key.alt)
			self.kb_actor.release(Key.tab)
			
			# Lb1.focus_set(takefocus=0)
			self.top.destroy()
			time.sleep(.1)
			#emulate paste event, is_terminal will only decide if shift key is to be emulated::	
			self.kb_actor.press(Key.ctrl)
			if is_terminal:
				self.kb_actor.press(Key.shift)
			self.kb_actor.press('v')
			
			self.current.clear()

			self.kb_actor.release(Key.ctrl)
			if is_terminal:
				self.kb_actor.release(Key.shift)
			self.kb_actor.release('v')

		self.top = Tk()

		OS = platform.system()


		screenWidth = self.top.winfo_screenwidth()
		screenHeight = self.top.winfo_screenheight()
		w = 500
		h = 300

		octo_font = font.Font(size = int(h / 18))
		
		x = screenWidth - (w + 15)
		y = (screenHeight / 2) - (h / 2)
		self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))
		if (OS == 'Windows'):
			self.top.wm_attributes("-alpha", 0.85)
		elif (OS == 'Linux'):
			pass
			#self.top.wait_visibility(self.top)
			#self.top.wm_attributes("-alpha", 0.85)
		elif (OS == 'Darwin'):
			self.top.wait_visibility(self.top)
			self.top.wm_attributes("-alpha", 0.85)
		
		scrollbar = Scrollbar(self.top, orient=VERTICAL)
		if(OS == 'Linux'):
			self.Lb1 = Listbox(self.top, 
								selectmode = EXTENDED,
								width = w - 5,
								height = h,
								relief = SUNKEN,
								bg = 'black',
								fg = 'white',
								selectbackground = '#ffffff',
								yscrollcommand = scrollbar.set,
								font = octo_font)
		else:
			self.Lb1 = Listbox(self.top, 
							selectmode = EXTENDED,
							width = w - 5,
							height = h,
							relief = SUNKEN,
							bg = 'black',
							fg = 'white',
							selectbackground = '#262523',
							yscrollcommand = scrollbar.set,
							font = octo_font)
		

		with open(self.JSON_PATH, 'rb') as f:
			self.data_json = json.load(f)
			for index, element in enumerate(self.data_json['records']):
				if len(element['text']) <= self.MAX_TEXT_LEN:
					self.Lb1.insert(index, str(index + 1) + ') '+ element['text'][:self.MAX_TEXT_LEN])
				else: 
					self.Lb1.insert(index, str(index + 1) + ') '+ element['text'][:int(self.MAX_TEXT_LEN / 2 - 1)] + ' ... ' + element['text'][int(-self.MAX_TEXT_LEN / 2 - 2):])

		self.Lb1.bind("<Return>", return_pressed)
	
		self.Lb1.pack()

		self.top.bind("<FocusIn>", self.handle_focus)
		self.top.mainloop()

	def write_to_json(self, data):
		self.data_json['records'].append({'text' : data})

		#remove entries in FCFS manner::
		if len(self.data_json['records']) > self.MAX_ENTRIES : 
			self.data_json['records'].pop(0)

		with open(self.JSON_PATH, 'w') as f:
			json.dump(self.data_json, f)
		###print('Dumped the new shit!')


	def execute_paste(self, is_terminal = False):
		#empty the current set, since task will be executed now
		self.current.clear()
		
		# open the dropdown menu
		self.dropDown(is_terminal)


	def execute_copy(self):
		copied_data = clipboard.paste()

		if not copied_data == self.prev_data: 
			self.write_to_json(copied_data)
			self.prev_data = copied_data

		# Update dropdown
		# if self.Lb1:
		# 	self.Lb1.Items.Clear()
		# 	with open(JSON_PATH, 'rb') as f:
		# 		data_json = json.load(f)
		# 		for index, element in enumerate(data_json['records']):
		# 			self.Lb1.insert(index, element['text'][:MAX_TEXT_LEN])


	# def execute(self):
	# 	self.current.clear()
	# 	#readFile(fileName)
	# 	self.dropDown()
	# 	####print(buffer['One'])


	# def readFile(self, fileName):
	# 	with open(fileName, 'r') as f:
	# 		self.buffer = json.load(f)


	def on_press(self, key):
		if any([key in COMBO for COMBO in self.TERMINAL_PASTE_COMBINATIONS]):
			self.current.add(key)
			if any(all(k in self.current for k in COMBO) for COMBO in self.TERMINAL_PASTE_COMBINATIONS):
				###print('ctrlShiftV detected!')
				# ###print(current)
				self.execute_paste(is_terminal = True)
				
		if any([key in COMBO for COMBO in self.PASTE_COMBINATIONS]):
			self.current.add(key)
			if any(all(k in self.current for k in COMBO) for COMBO in self.PASTE_COMBINATIONS):
				###print('ctrlV detected!')
				# ##print(current)
				self.execute_paste(is_terminal = False)

		if any([key in COMBO for COMBO in self.COPY_COMBINATIONS]):
			self.current.add(key)
			if any(all(k in self.current for k in COMBO) for COMBO in self.COPY_COMBINATIONS):
				##print('ctrlC detected!')
				self.execute_copy()
				#empty the current set, since task has been executed now
				self.current.clear()


		if any([key in COMBO for COMBO in self.TERMINAL_COPY_COMBINATIONS]):
			self.current.add(key)
			if any(all(k in self.current for k in COMBO) for COMBO in self.TERMINAL_COPY_COMBINATIONS):
				##print('ctrlShiftC detected!')
				self.execute_copy()
				#empty the current set, since task has been executed now
				self.current.clear()

		if any([key in COMBO for COMBO in self.CUT_COMBINATIONS]):
			self.current.add(key)
			if any(all(k in self.current for k in COMBO) for COMBO in self.CUT_COMBINATIONS):
				##print('ctrlX detected!')
				self.execute_copy()
				#empty the current set, since task has been executed now
				self.current.clear()

	def on_release(self, key):
	    self.current.clear()

if __name__ == '__main__':
	op = OctoPaste()
	
	
