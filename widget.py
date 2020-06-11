import tkinter as tk
import tkinter.font
import time

from logic import*
import editable_keybinds_settings as p1controls

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

class GameWidget(tk.Frame,GameLogic):

	def __init__(self, master=None,rng=random.Random(),keybinds = p1controls.keybinds,linegoal=None,timegoal=None):
		tk.Frame.__init__(self,master)
		GameLogic.__init__(self,rng,keybinds,linegoal,timegoal)
		self.master = master

		self.time0 = time.clock()
		self.wait_longer = False

		self.piece_display_height = PIECE_DISPLAY_HEIGHT*PIECE_SIZE
		self.piece_display_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		self.left_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		self.right_width = self.piece_display_width
		self.middle_width = BOARD_WIDTH*PIECE_SIZE
		self.middle_height = BOARD_HEIGHT*PIECE_SIZE
		self.next_pieces_height = PIECE_DISPLAY_HEIGHT*PIECE_SIZE*NEXT_PIECES
		self.next_pieces_width = PIECE_DISPLAY_WIDTH*PIECE_SIZE
		self.largest_height = max(self.middle_height,self.piece_display_height,self.next_pieces_height)
		self.right_info_height = self.largest_height-self.next_pieces_height
		self.left_info_height = self.largest_height-self.piece_display_height

		self.configure(width = self.left_width+self.middle_width+self.right_width,height=self.largest_height)

		if PIECE_HOLDS:
			self.left_panel = tk.Frame(self,width=self.left_width,height=self.largest_height)
			self.left_panel.grid(row=0,column=0,sticky=tk.N)
			self.hold_canvas = tk.Canvas(self.left_panel,width=self.piece_display_width,height=self.piece_display_height)
			self.hold_canvas.grid(row=0,column=0)
			self.left_info_canvas = tk.Canvas(self.left_panel,width=self.left_width,height=self.left_info_height)
			self.left_info_canvas.grid(row=1,column=0)

		self.board_canvas = tk.Canvas(self,width=self.middle_width,height=self.largest_height)
		self.board_canvas.grid(row=0,column=1,sticky=tk.N)

		if NEXT_PIECES>0:
			self.right_panel = tk.Frame(self,width=self.right_width,height=self.largest_height)
			self.right_panel.grid(row=0,column=2,sticky=tk.N)
			self.next_pieces_frame = tk.Frame(self.right_panel,width=self.next_pieces_width,height=self.next_pieces_height)
			self.next_pieces_frame.grid(row=0,column=0)
			self.right_info_canvas = tk.Canvas(self.right_panel,width=self.right_width,height=self.right_info_height)
			self.right_info_canvas.grid(row=1,column=0)
			self.next_piece_canvases = []
			for i in range(NEXT_PIECES):
				cur = tk.Canvas(self.next_pieces_frame,width=self.piece_display_width,height=self.piece_display_height)
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
		if PIECE_HOLDS:
			paint_canvas(self.hold_canvas,self.hold_display[1],int(not COLORBLIND_MODE)*0,0)

	def paint_board(self):
		paint_canvas(self.board_canvas,self.paint_update_board,int(not COLORBLIND_MODE)*0.5,0.5+int(COLORBLIND_MODE)*2)

	def paint_next_pieces(self):
		if NEXT_PIECES>0:
			for i in range(len(self.next_piece_canvases)):
				paint_canvas(self.next_piece_canvases[i],self.next_pieces_display[i][1],int(not COLORBLIND_MODE)*0,0)
	
	def paint_messages(self):
		tag = "messagetext"
		oldtext = self.board_canvas.find_withtag(tag)
		if len(oldtext)!=0:
			self.board_canvas.delete(oldtext)
		if self.get_text_display_time()+TEXT_DISPLAY_DURATION>self.framecount:
			self.board_canvas.create_text(self.middle_width/2,self.middle_height/2,text=self.get_text_display_string().upper(),
			font = tk.font.Font(family="bahnschrift",size=int(self.middle_width/10),weight="bold"),fill=MESSAGE_COLOR,tags=(0,tag))

	def paint_info(self):
		tag = "info"
		oldtext = self.left_info_canvas.find_withtag(tag)
		if len(oldtext)!=0:
			self.left_info_canvas.delete(oldtext)
		text=self.get_info_string()
		if LOG_TIME_OFFSET:
			text+="\nIGT-RT="+ str(int((self.framecount/60-(time.clock()-self.time0))*100)/100)
		self.left_info_canvas.create_text(0,0,
		anchor = tk.NW,
		text=text,
		font = tk.font.Font(family="bahnschrift",size=int(PIECE_SIZE*BOARD_WIDTH/20),weight="bold"),fill=TEXT_COLOR,tags=(0,tag))

	def run_frame(self):
		if not self.game_finished:
			if self.wait_longer:
				self.after(17,self.run_frame)
			else:
				self.after(16,self.run_frame)

		if CLOCKCHECK_PERIOD!=0 and self.framecount%CLOCKCHECK_PERIOD == 0:
			self.timel = time.clock()
		self.wait_longer = (self.framecount%CLOCKCHECK_PERIOD)/60>(time.clock()-self.timel)

		self.perform_frame_logic()
		self.paint_board()
		self.paint_messages()
		self.paint_info()
		self.paint_hold()
		self.paint_next_pieces()
