from widget import*
import sys
import editable_keybinds_settings_p2 as p2controls

class Pytris(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		self.m = master

	def run(self,args):
		self.rngseed = random.randint(0,int(2**64-1))
		self.linegoal = None
		self.timegoal = None
		if "sprint" in args:
			self.linegoal = SPRINT_LINE_COUNT

		if "blitz" in args:
			self.timegoal = BLITZ_TIME_AMOUNT

		if "2p" in args:
			self.run_2player()
		else:
			self.run_basic()

	def run_basic(self):
		self.game = GameWidget(master=self.m,linegoal=self.linegoal,timegoal=self.timegoal)
		self.game.pack()
		self.game.focus_set()
		self.game.mainloop()

	def run_2player(self):
		rng1 = random.Random()
		rng1.seed(self.rngseed)
		rng2 = random.Random()
		rng2.seed(self.rngseed)
		self.left = GameWidget(master=self.m,rng=rng1,linegoal=self.linegoal,timegoal=self.timegoal)
		self.left.pack(side = tk.LEFT)
		self.right = GameWidget(master=self.m,rng=rng2,keybinds=p2controls.keybinds,linegoal=self.linegoal,timegoal=self.timegoal)
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
pytris.run(set(sys.argv))