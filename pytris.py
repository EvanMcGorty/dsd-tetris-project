from widget import*
import sys
import editable_keybinds_settings_p2 as p2controls

class Pytris(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		self.m = master

	def run(self,args):
		self.rngseed = random.randint(0,int(2**64-1))
		if RNG_SEED!=None:
			self.rngseed = RNG_SEED
		self.linegoal = None
		self.timegoal = None
		if "sprint" in args:
			self.linegoal = SPRINT_LINE_COUNT

		if "blitz" in args:
			self.timegoal = BLITZ_TIME_AMOUNT


		if "2p" in args:
			self.run_2player()
		elif "playback" in args:
			self.play_replay()
		elif "record" in args:
			self.record_replay()
		else:
			self.run_basic()

	def run_basic(self):
		rng = random.Random()
		rng.seed(self.rngseed)
		self.game = GameWidget(master=self.m,rng=rng,linegoal=self.linegoal,timegoal=self.timegoal)
		self.game.run_frame()
		self.game.pack()
		self.game.focus_set()
		self.game.mainloop()

	def off(self,keyname):
		self.left.turn_key_off(keyname)
		self.right.turn_key_off(keyname)
	def on(self,keyname):
		self.left.turn_key_on(keyname)
		self.right.turn_key_on(keyname)
	def run_2player(self):
		rng1 = random.Random()
		rng1.seed(self.rngseed)
		rng2 = random.Random()
		rng2.seed(self.rngseed)
		self.left = GameWidget(master=self.m,rng=rng1,linegoal=self.linegoal,timegoal=self.timegoal)
		self.left.run_frame()
		self.left.pack(side = tk.LEFT)
		self.right = GameWidget(master=self.m,rng=rng2,keybinds=p2controls.keybinds,linegoal=self.linegoal,timegoal=self.timegoal)
		self.right.run_frame()
		self.right.pack(side = tk.RIGHT)
		self.m.focus_set()
		self.m.bind('<Key>',self.on)
		self.m.bind('<KeyRelease>',self.off)
		self.m.mainloop()


	def writecurinput(self):
		buttonval = 0
		for i in range(len(self.game.buttons)):
			if self.game.buttons[i]:
				buttonval+=int(2**i)
		releaseval = 0
		for i in range(len(self.game.buttons_release_wait)):
			if self.game.buttons_release_wait[i]:
				releaseval+=int(2**i)
		self.replay_data.append(buttonval)
		self.replay_data.append(releaseval)
	def record_replay(self):
		self.replay_data = bytearray()
		rng = random.Random()
		rng.seed(self.rngseed)
		self.game = GameWidget(master=self.m,rng=rng,linegoal=self.linegoal,timegoal=self.timegoal,every_frame_call=self.writecurinput)
		self.game.run_frame()
		self.game.pack()
		self.game.focus_set()
		self.game.mainloop()
		file = open("replay",'wb')
		file.write(self.replay_data)
		file.close()

	def readnextinput(self):
		if self.replay_index<len(self.replay_data):
			self.game.buttons=[bool(self.replay_data[self.replay_index] & (1<<n)) for n in range(8)]
			self.game.buttons_release_wait=[bool(self.replay_data[self.replay_index+1] & (1<<n)) for n in range(8)]
			self.replay_index+=2
			if self.replay_index>=len(self.replay_data):
				self.game.focus_set()
	def play_replay(self):
		file = open("replay",'rb')
		self.replay_data = file.read()
		self.replay_index = 0
		file.close()
		rng = random.Random()
		rng.seed(self.rngseed)
		self.game = GameWidget(master=self.m,rng=rng,linegoal=self.linegoal,timegoal=self.timegoal,every_frame_call=self.readnextinput)
		self.game.run_frame()
		self.game.pack()
		self.m.focus_set()
		self.game.mainloop()

pytris = Pytris(master=tk.Tk())
pytris.pack()
pytris.run(set(sys.argv))