from tkinter import Tk, Canvas, Frame, BOTH, ALL, font

from logic import*


PIECE_SIZE = 40

COLOR_DICT = {-1*int(COLORBLIND_MODE): "#feb", -1*int(not COLORBLIND_MODE):"#000",1:"#e21",2:"#04c",3:"#1ec",4:"#0b3",5:"#f60",6:"#fc0",7:"#b2d"}

class PytrisWidget(Frame):

	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		master.minsize(10*PIECE_SIZE,20*PIECE_SIZE)
		self.board_canvas = Canvas(self,width=10*PIECE_SIZE,height=20*PIECE_SIZE)
		self.board_canvas.pack()
		self.board_canvas.focus_set()		
		self.board_canvas.bind('<Key>',self.turn_key_on)
		self.board_canvas.bind('<KeyRelease>',self.turn_key_off)
		self.run_frame()

	def turn_key_on(self,keyname):
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				buttons[i] = True
		
	def turn_key_off(self,keyname):
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				buttons[i] = False
				buttons_release_wait[i] = True


	def run_frame(self):
		global framecount
		if framecount%3 == 0:
			self.after(16,self.run_frame)
		else:
			self.after(17,self.run_frame)
		perform_frame_logic()
		for y in range(0,len(paint_update_board)):
			for x in range(0,len(paint_update_board[0])):
				cur = paint_update_board[len(paint_update_board)-1-y][x]
				if cur != PAINT_NOTHING:
					tag = str(x)+' '+str(y)
					oldelem = self.board_canvas.find_withtag(tag)
					if len(oldelem)!=0:
						self.board_canvas.delete(oldelem)
					self.board_canvas.create_rectangle(
						x*PIECE_SIZE,y*PIECE_SIZE,(x+1)*PIECE_SIZE,(y+1)*PIECE_SIZE,
						outline=COLOR_DICT[-1], width=0.5*int(not COLORBLIND_MODE)+2*int(COLORBLIND_MODE and cur==BACKGROUND_TILE),
						fill=COLOR_DICT[cur],
						tags = (0,tag))
					paint_update_board[len(paint_update_board)-1-y][x] = PAINT_NOTHING
		tag = "messagetext"
		oldtext = self.board_canvas.find_withtag(tag)
		if len(oldtext)!=0:
			self.board_canvas.delete(oldtext)
		if get_text_display_time()+TEXT_DISPLAY_DURATION>get_curframe():
			self.board_canvas.create_text(5*PIECE_SIZE,10*PIECE_SIZE,text=get_text_display_string().upper(),font = font.Font(family="bahnschrift",size=PIECE_SIZE,weight="bold"),tag=tag)

