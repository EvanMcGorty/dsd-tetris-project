from tkinter import Tk, Canvas, Frame, BOTH

from logic import*


PIECE_SIZE = 40

COLOR_DICT = {0:"#000",1:"#e21",2:"#04c",3:"#1ec",4:"#8e7",5:"#fc0",6:"#fe2",7:"#b2d"}



class PytrisWidget(Frame):

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		master.minsize(10*PIECE_SIZE,20*PIECE_SIZE)
		self.canvas = Canvas(self,width=10*PIECE_SIZE,height=20*PIECE_SIZE)
		self.canvas.pack()
		self.canvas.focus_set()
		self.canvas.bind('<Key>',self.turn_key_on)
		self.canvas.bind('<KeyRelease>',self.turn_key_off)
		self.run_frame()

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
		
	def paintboard(self):
		for y in range(0,len(paint_update_board)):
			for x in range(0,len(paint_update_board[0])):
				if paint_update_board[len(paint_update_board)-1-y][x] != PAINT_NOTHING:
					self.canvas.create_rectangle(
						x*PIECE_SIZE,y*PIECE_SIZE,(x+1)*PIECE_SIZE,(y+1)*PIECE_SIZE,
						outline="#fff", fill=COLOR_DICT[paint_update_board[len(paint_update_board)-1-y][x]])
					paint_update_board[len(paint_update_board)-1-y][x] = PAINT_NOTHING


	def run_frame(self):
		self.after(17,self.run_frame)
		global framecount
		paint_update_board[framecount%19][framecount%10] = framecount%8
		self.paintboard()
		framecount+=1

