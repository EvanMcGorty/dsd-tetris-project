from piece_data import*



def construct_piece(ind):
	return (ind,0)

def rotate_piece(pieceval,rot):
	turn_count = {ROT90:1,ROT180:2,ROT270:3}[rot]
	return (pieceval[0],(pieceval[1]+turn_count)%4)

def index_piece(pieceval,x,y,blocktype = None):
	if blocktype==None:
		blocktype = pieceval[0]
	rotation = pieceval[1]
	piece = pieceval[0]
	matrix = PIECE_MATRICIES[piece]
	newy = y
	newx = x
	if rotation == 1:
		newy = x
		newx = MATRIX_SIZE[piece]-1-y
	if rotation == 2:
		newy = MATRIX_SIZE[piece]-1-y
		newx = MATRIX_SIZE[piece]-1-x
	if rotation == 3:
		newy = MATRIX_SIZE[piece]-1-x
		newx = y
	return {False:BACKGROUND_TILE,True:blocktype}[matrix[newy][newx]]
		

def kick_table_index(cur_orientation,rotation,table,attempt):
	if rotation==ROT180:
		return (0,0)
	if rotation==ROT90:
		return table[cur_orientation][attempt]
	if rotation==ROT270:
		(x,y) = table[(cur_orientation+3)%4][attempt]
		return (-x,-y)



def assign_update(val,raw,update,x,y):
	if val != raw[y][x]:
		raw[y][x] = val
		update[y][x] = val

def make_piece_display():
	return (make_board_matrix(BACKGROUND_TILE,PIECE_DISPLAY_WIDTH,PIECE_DISPLAY_HEIGHT),make_board_matrix(BACKGROUND_TILE,PIECE_DISPLAY_WIDTH,PIECE_DISPLAY_HEIGHT))


def update_piece_display(matrix,piece,display):
	found_bottom = -1
	for y in range(len(matrix)):
		if found_bottom == -1:
			for x in matrix[y]:
				if x:
					found_bottom = y
		for x in range(len(matrix[y])):
			if found_bottom != -1 and y-found_bottom<PIECE_DISPLAY_HEIGHT and x<PIECE_DISPLAY_WIDTH:
				cur = {True:piece,False:BACKGROUND_TILE}[matrix[y][x]]
				assign_update(cur,display[0],display[1],x,y-found_bottom)
		for x in range(len(matrix[y]),PIECE_DISPLAY_WIDTH):
			assign_update(BACKGROUND_TILE,display[0],display[1],x,y-found_bottom)
	for y in range(len(matrix),PIECE_DISPLAY_HEIGHT):
		for x in range(PIECE_DISPLAY_WIDTH):
			assign_update(BACKGROUND_TILE,display[0],display[1],x,y-found_bottom)


class GameState:


	def __init__(self):
		self.framecount = 0
		self.text_to_display = ("",-TEXT_DISPLAY_DURATION)
		
		self.board = make_board_matrix(BACKGROUND_TILE,BOARD_WIDTH,BOARD_HEIGHT)

		self.paint_update_board = make_board_matrix(BACKGROUND_TILE,BOARD_WIDTH,BOARD_HEIGHT)

		self.hold_display = make_piece_display()

		self.next_pieces_display = []
		for i in range(NEXT_PIECES):
			self.next_pieces_display.append(make_piece_display())


	def increment_framecount(self):
		self.framecount+=1
	def get_curframe(self):
		return self.framecount

	def get_text_display_string(self):
		return self.text_to_display[0]

	def get_text_display_time(self):
		return self.text_to_display[1]
		

	def display_message(self,string):
		if self.text_to_display[1] == self.framecount:
			self.text_to_display = (self.text_to_display[0]+"\n"+string,self.framecount)
		else:
			self.text_to_display = (string,self.framecount)


	def is_occupiable(self,x,y):
		if ALLOW_PIECES_ABOVE_CEILING:
			return y>=0 and BOARD_WIDTH>x and x>=0 and (y>=BOARD_HEIGHT or self.board[y][x] == BACKGROUND_TILE)
		else:
			return len(self.board)>y and y>=0 and len(self.board[y])>x and x>=0 and self.board[y][x] == BACKGROUND_TILE


	def can_place_piece(self,pieceval,x,y):
		for ix in range(MATRIX_SIZE[pieceval[0]]):
			for iy in range(MATRIX_SIZE[pieceval[0]]):
				if index_piece(pieceval,ix,iy) != BACKGROUND_TILE:
					if not self.is_occupiable(ix+x,iy+y):
						return False
		return True
		
	def place_piece(self,pieceval,x,y,blocktype = None):
		if blocktype==None:
			blocktype = pieceval[0]
		for ix in range(MATRIX_SIZE[pieceval[0]]):
			for iy in range(MATRIX_SIZE[pieceval[0]]):
				if y+iy >= BOARD_HEIGHT:
					continue
				cur = index_piece(pieceval,ix,iy,blocktype)
				if cur != BACKGROUND_TILE:
					assign_update(cur,self.board,self.paint_update_board,ix+x,iy+y)

	def clear_piece(self,pieceval,x,y):
		for ix in range(MATRIX_SIZE[pieceval[0]]):
			for iy in range(MATRIX_SIZE[pieceval[0]]):
				if y+iy >= BOARD_HEIGHT:
					continue
				cur = index_piece(pieceval,ix,iy)
				if cur != BACKGROUND_TILE:
					assign_update(BACKGROUND_TILE,self.board,self.paint_update_board,ix+x,iy+y)

	def rows_to_clear(self):
		ret = []
		for y in range(len(self.board)):
			is_row_clearable = True
			for x in range(len(self.board[y])):
				if self.board[y][x]==BACKGROUND_TILE:
					is_row_clearable = False
					break
			if is_row_clearable:
				ret.append(y)
		return ret


	def clear_rows(self):
		rows = self.rows_to_clear()
		if len(rows)==0:
			return 0
		newboard = []
		for y in range(len(self.board)):
			newrow = []
			dist = 0
			for i in rows:
				if i<=y+dist:
					dist+=1
			if y+dist >=len(self.board):
				for i in range(BOARD_WIDTH):
					newrow.append(BACKGROUND_TILE)
				newboard.append(newrow)
				continue
			for x in range(len(self.board[y+dist])):
				if self.board[y+dist][x]!=self.board[y][x]:
					self.paint_update_board[y][x] = self.board[y+dist][x]
				newrow.append(self.board[y+dist][x])
			newboard.append(newrow)
		self.board = newboard
		return len(rows)
				


		