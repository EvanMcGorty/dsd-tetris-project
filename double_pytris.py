from widget import*

f = tk.Tk()
left = PytrisWidget(master=f)
left.pack(side = tk.LEFT)
right = PytrisWidget(master=f)
right.pack(side = tk.RIGHT)
f.focus_set()

def off(keyname):
	global left
	global right
	left.turn_key_off(keyname)
	right.turn_key_off(keyname)
	print(keyname)

	
def on(keyname):
	global left
	global right
	left.turn_key_on(keyname)
	right.turn_key_on(keyname)
	print(keyname)

f.bind('<Key>',on)
f.bind('<KeyRelease>',off)
f.mainloop()