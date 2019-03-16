from pynput.keyboard import Controller, Key
import clipboard

kb_actor = Controller()
# clipboard.copy('fts')
kb_actor.press(Key.ctrl)
kb_actor.press(Key.shift)
kb_actor.press('v')

kb_actor.release(Key.ctrl)
kb_actor.release(Key.shift)
kb_actor.release('v')
