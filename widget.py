import tkinter as tk
import tkinter.font

from logic import*


def paint_canvas(canvas,board,piecegridwidth,gridwidth):
	for y in range(0,len(board)):
		for x in range(0,len(board[y])):
			cur = board[len(board)-1-y][x]
			if cur != PAINT_NOTHING:
				tag = str(x)+' '+str(y)
				oldelem = canvas.find_withtag(tag)
				if len(oldelem)!=0:
					canvas.delete(oldelem)
				canvas.create_rectangle(
					x*PIECE_SIZE,y*PIECE_SIZE,(x+1)*PIECE_SIZE,(y+1)*PIECE_SIZE,
					outline=COLOR_SCHEME[-1],
					width=piecegridwidth*int(cur!=BACKGROUND_TILE)+gridwidth*int(cur==BACKGROUND_TILE),
					fill=COLOR_SCHEME[cur],
					tags = (0,tag))
				board[len(board)-1-y][x] = PAINT_NOTHING

class PytrisWidget(tk.Frame,Logic):

	def __init__(self, master=None):
		tk.Frame.__init__(self,master)
		Logic.__init__(self)
		self.master = master
		self.pack()
		master.minsize(BOARD_WIDTH*PIECE_SIZE,BOARD_HEIGHT*PIECE_SIZE)
		self.left_panel = tk.Frame(self,width=HOLD_DISPLAY_WIDTH*PIECE_SIZE,height=BOARD_HEIGHT*PIECE_SIZE)
		self.left_panel.pack(side = tk.LEFT)
		self.hold_canvas = tk.Canvas(self.left_panel,width=HOLD_DISPLAY_WIDTH*PIECE_SIZE,height=HOLD_DISPLAY_HEIGHT*PIECE_SIZE)
		self.hold_canvas.pack(side = tk.TOP)
		self.info_canvas = tk.Canvas(self.left_panel,width=HOLD_DISPLAY_WIDTH*PIECE_SIZE,height=BOARD_HEIGHT*PIECE_SIZE-HOLD_DISPLAY_HEIGHT*PIECE_SIZE)
		self.info_canvas.pack(side = tk.BOTTOM)
		self.board_canvas = tk.Canvas(self,width=BOARD_WIDTH*PIECE_SIZE,height=BOARD_HEIGHT*PIECE_SIZE)
		self.board_canvas.pack(side = tk.RIGHT)
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


	def paint_hold(self):
		paint_canvas(self.hold_canvas,self.hold_display_paint_update,int(not COLORBLIND_MODE)*0.5,0)

	def paint_board(self):
		paint_canvas(self.board_canvas,self.paint_update_board,int(not COLORBLIND_MODE)*0.5,0.5+int(COLORBLIND_MODE)*2)
	
	def paint_messages(self):
		tag = "messagetext"
		oldtext = self.board_canvas.find_withtag(tag)
		if len(oldtext)!=0:
			self.board_canvas.delete(oldtext)
		if self.get_text_display_time()+TEXT_DISPLAY_DURATION>self.get_curframe():
			self.board_canvas.create_text(BOARD_WIDTH/2*PIECE_SIZE,BOARD_HEIGHT/2*PIECE_SIZE,text=self.get_text_display_string().upper(),
			font = tk.font.Font(family="bahnschrift",size=int(PIECE_SIZE*BOARD_WIDTH/10),weight="bold"),fill="#78d",tag=tag)

	def run_frame(self):
		if self.framecount%3 == 0:
			self.after(16,self.run_frame)
		else:
			self.after(17,self.run_frame)
		self.perform_frame_logic()
		self.paint_hold()
		self.paint_board()
		self.paint_messages()

