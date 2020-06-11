from widget import*
import sys
import editable_keybinds_settings_p2 as p2controls

class Pytris(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		self.m = master

	def run(self,args):
		self.rngseed = random.randint(0,int(2**64-1))
		if len(args)>1 and args[1]=="2p":
			self.run_2player()
		else:
			self.run_basic()

	def run_basic(self):
		self.game = GameWidget(master=self.m)
		self.game.pack()
		self.game.focus_set()
		self.game.mainloop()

	def run_2player(self):
		rng1 = random.Random()
		rng1.seed(self.rngseed)
		rng2 = random.Random()
		rng2.seed(self.rngseed)
		self.left = GameWidget(master=self.m,rng=rng1)
		self.left.pack(side = tk.LEFT)
		self.right = GameWidget(master=self.m,rng=rng2,keybinds=p2controls.keybinds)
		self.right.pack(side = tk.RIGHT)
		self.m.focus_set()
		self.m.bind('<Key>',self.on)
		self.m.bind('<KeyRelease>',self.off)
		self.m.mainloop()


	
	

	def off(self,keyname):
		self.left.turn_key_off(keyname)
		self.right.turn_key_off(keyname)
		
	def on(self,keyname):
		self.left.turn_key_on(keyname)
		self.right.turn_key_on(keyname)


pytris = Pytris(master=tk.Tk())
pytris.pack()
pytris.run(sys.argv)