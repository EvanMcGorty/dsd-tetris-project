from tkinter import Tk, Canvas, Frame, LEFT, font

from logic import*



class PytrisWidget(Frame,Logic):

	def __init__(self, master=None):
		Frame.__init__(self,master)
		Logic.__init__(self)
		self.master = master
		self.pack()
		master.minsize(BOARD_WIDTH*PIECE_SIZE,BOARD_HEIGHT*PIECE_SIZE)
		self.board_canvas = Canvas(self,width=BOARD_WIDTH*PIECE_SIZE,height=BOARD_HEIGHT*PIECE_SIZE)
		self.board_canvas.pack()
		self.focus_set()		
		self.bind('<Key>',self.turn_key_on)
		self.bind('<KeyRelease>',self.turn_key_off)
		self.run_frame()

	def turn_key_on(self,keyname):
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				self.buttons[i] = True
		
	def turn_key_off(self,keyname):
		for i in range(0,len(KEYS)):
			if keyname.keysym == KEYS[i]:
				self.buttons[i] = False
				self.buttons_release_wait[i] = True

	def paint_board(self):
		for y in range(0,len(self.paint_update_board)):
			for x in range(0,len(self.paint_update_board[0])):
				cur = self.paint_update_board[len(self.paint_update_board)-1-y][x]
				if cur != PAINT_NOTHING:
					tag = str(x)+' '+str(y)
					oldelem = self.board_canvas.find_withtag(tag)
					if len(oldelem)!=0:
						self.board_canvas.delete(oldelem)
					self.board_canvas.create_rectangle(
						x*PIECE_SIZE,y*PIECE_SIZE,(x+1)*PIECE_SIZE,(y+1)*PIECE_SIZE,
						outline=COLOR_SCHEME[-1], width=0.5*int(not COLORBLIND_MODE)+2*int(COLORBLIND_MODE and cur==BACKGROUND_TILE),
						fill=COLOR_SCHEME[cur],
						tags = (0,tag))
					self.paint_update_board[len(self.paint_update_board)-1-y][x] = PAINT_NOTHING
	
	def paint_messages(self):
		tag = "messagetext"
		oldtext = self.board_canvas.find_withtag(tag)
		if len(oldtext)!=0:
			self.board_canvas.delete(oldtext)
		if self.get_text_display_time()+TEXT_DISPLAY_DURATION>self.get_curframe():
			self.board_canvas.create_text(BOARD_WIDTH/2*PIECE_SIZE,BOARD_HEIGHT/2*PIECE_SIZE,text=self.get_text_display_string().upper(),
			font = font.Font(family="bahnschrift",size=int(PIECE_SIZE*BOARD_WIDTH/10),weight="bold"),fill="#78d",tag=tag)

	def run_frame(self):
		if self.framecount%3 == 0:
			self.after(16,self.run_frame)
		else:
			self.after(17,self.run_frame)
		self.perform_frame_logic()
		self.paint_board()
		self.paint_messages()

