#queueing functions for the copied text to be stored
#store in json/ append to dict each text copied
#ctrl c to copy to the normal os clipboard
#access the clipboard internally and fetch the copied text
#store the copied text locally to the db
#ctrlv for normal paste, since the os clipboard will still have the data buffered
#ctrl alt v for the tkinter ui to popup

#for files, access the filepath from the internal buffer*

import clipboard
import pyautogui
import time
# with open('./lol.txt', 'rb') as f:

clipboard.copy('hello bhs')

# pyautogui.hotkey('altleft','shiftleft' 'tab')
# time.sleep(10)
pyautogui.hotkey('ctrl', 'shift','v')


