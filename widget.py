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

		piece_display_height = PIECE_DISPLAY_HEIGHT*PIECE_SIZE
		piece_display_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		left_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		right_width = piece_display_width
		middle_width = BOARD_WIDTH*PIECE_SIZE
		middle_height = BOARD_HEIGHT*PIECE_SIZE
		next_pieces_height = PIECE_DISPLAY_HEIGHT*PIECE_SIZE*NEXT_PIECES
		next_pieces_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		largest_height = max(middle_height,piece_display_height,next_pieces_height)
		right_info_height = largest_height-next_pieces_height
		left_info_height = largest_height-piece_display_height

		self.configure(width = left_width+middle_width+right_width,height=largest_height)

		self.left_panel = tk.Frame(self,width=left_width,height=largest_height)
		self.left_panel.grid(row=0,column=0,sticky=tk.N)
		self.hold_canvas = tk.Canvas(self.left_panel,width=piece_display_width,height=piece_display_height)
		self.hold_canvas.grid(row=0,column=0)
		self.left_info_canvas = tk.Canvas(self.left_panel,width=left_width,height=left_info_height)
		self.left_info_canvas.grid(row=1,column=0)

		self.board_canvas = tk.Canvas(self,width=middle_width,height=largest_height)
		self.board_canvas.grid(row=0,column=1,sticky=tk.N)

		self.right_panel = tk.Frame(self,width=right_width,height=largest_height)
		self.right_panel.grid(row=0,column=2,sticky=tk.N)
		self.next_pieces_frame = tk.Frame(self.right_panel,width=next_pieces_width,height=next_pieces_height)
		self.next_pieces_frame.grid(row=0,column=0)
		self.right_info_canvas = tk.Canvas(self.right_panel,width=right_width,height=right_info_height)
		self.right_info_canvas.grid(row=1,column=0)
		self.next_piece_canvases = []
		for i in range(NEXT_PIECES):
			cur = tk.Canvas(self.next_pieces_frame,width=piece_display_width,height=piece_display_height)
			cur.grid(row=NEXT_PIECES-1-i,column=0)
			self.next_piece_canvases.append(cur)

		self.bind('<Key>',self.turn_key_on)
		self.bind('<KeyRelease>',self.turn_key_off)
		self.run_frame()

	def turn_key_on(self,keyname):
		for i in range(0,len(self.keybinds)):
			if keyname.keysym == self.keybinds[i]:
				self.buttons[i] = True
		
	def turn_key_off(self,keyname):
		for i in range(0,len(self.keybinds)):
			if keyname.keysym == self.keybinds[i]:
				self.buttons[i] = False
				self.buttons_release_wait[i] = True

	def paint_hold(self):
		paint_canvas(self.hold_canvas,self.hold_display[1],int(not COLORBLIND_MODE)*0,0)

	def paint_board(self):
		paint_canvas(self.board_canvas,self.paint_update_board,int(not COLORBLIND_MODE)*0.5,0.5+int(COLORBLIND_MODE)*2)

	def paint_next_pieces(self):
		for i in range(len(self.next_piece_canvases)):
			paint_canvas(self.next_piece_canvases[i],self.next_pieces_display[i][1],int(not COLORBLIND_MODE)*0,0)
	
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
		self.paint_next_pieces()

