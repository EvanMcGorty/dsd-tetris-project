from tkinter import Tk, Canvas, Frame, BOTH

framecount = 0


PIECE_SIZE = 30

PAINT_NOTHING = 0

def make_board_matrix(initval):
	board = []
	for y in range(0,20):
		nextrow = []
		for x in range(0,10):
			nextrow.append(initval)
		board.append(nextrow)
	return board

paint_update_board = make_board_matrix(PAINT_NOTHING)

buttons = []
for i in range(0,8):
	buttons.append(False)

(ROT90,ROT270,ROT180,RIGHT,LEFT,SOFT,HARD,HOLD) = [0,1,2,3,4,5,6,7]

KEYS = ['Up','z','a','Right','Left','Down','space','c']

class Application(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		master.minsize(10*PIECE_SIZE,20*PIECE_SIZE)
		self.canvas = Canvas(self,width=10*PIECE_SIZE,height=20*PIECE_SIZE)
		self.canvas.pack()
		self.setup()
		self.prepare_next_frame()

	def turn_key_on(self,keyname):
		global KEYS
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				buttons[i] = True
		
	def turn_key_off(self,keyname):
		global KEYS
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				buttons[i] = False
		
		

	def setup(self):
		self.canvas.focus_set()
		self.canvas.bind('<Key>',self.turn_key_on)
		self.canvas.bind('<KeyRelease>',self.turn_key_off)


	def prepare_next_frame(self):
		self.after(17,self.run_frame)
		
	def paintboard(self):
		paint_update_board[framecount%19][framecount%9] = 1
		canvas = self.canvas
		for y in range(0,len(paint_update_board)):
			for x in range(0,len(paint_update_board[0])):
				if paint_update_board[len(paint_update_board)-1-y][x] != PAINT_NOTHING:
					canvas.create_rectangle(
						x*PIECE_SIZE,y*PIECE_SIZE,(x+1)*PIECE_SIZE,(y+1)*PIECE_SIZE,
						outline="#fb0", fill="#fb0")
					paint_update_board[len(paint_update_board)-1-y][x] = PAINT_NOTHING


	def run_frame(self):
		global framecount
		framecount+=1
		self.prepare_next_frame()
		self.paintboard()

		'''
		canvas = Canvas(self)
		canvas.create_rectangle(0, 0, 10*framecount, 10,
			outline="#fb0", fill="#fb0")
		canvas.grid(row = 0, column = 0)
		'''


root = Tk()
app = Application(master=root)
app.mainloop()