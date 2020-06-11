from widget import*

f = tk.Tk()
left = PytrisWidget(master=f)
left.pack(side = tk.LEFT)
right = PytrisWidget(master=f)
right.keybinds = ['u','i','o','p','7','8','9','0'] #use joytokey to have 2 people playing on the same computer
right.pack(side = tk.RIGHT)
f.focus_set()

def off(keyname):
	global left
	global right
	left.turn_key_off(keyname)
	right.turn_key_off(keyname)
	
def on(keyname):
	global left
	global right
	left.turn_key_on(keyname)
	right.turn_key_on(keyname)

f.bind('<Key>',on)
f.bind('<KeyRelease>',off)
f.mainloop()