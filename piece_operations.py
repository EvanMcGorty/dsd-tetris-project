from piece_data import*


framecount = 0

def increment_framecount():
	global framecount
	framecount+=1
def get_curframe():
	return framecount

TEXT_DISPLAY_DURATION = 90

text_to_display = ("",-TEXT_DISPLAY_DURATION)

def get_text_display_string():
	return text_to_display[0]

def get_text_display_time():
	return text_to_display[1]
	

def display_message(string):
	global text_to_display
	global framecount
	if text_to_display[1] == framecount:
		text_to_display = (text_to_display[0]+"\n"+string,framecount)
	else:
		text_to_display = (string,framecount)

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


board = make_board_matrix(BACKGROUND_TILE)

paint_update_board = make_board_matrix(BACKGROUND_TILE)


def is_occupiable(x,y):
	return len(board)>y and y>=0 and len(board[y])>x and x>=0 and board[y][x] == BACKGROUND_TILE
	

def can_place_piece(pieceval,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			if index_piece(pieceval,ix,iy) != BACKGROUND_TILE:
				if not is_occupiable(ix+x,iy+y):
					return False
	return True
	
def place_piece(pieceval,x,y,blocktype = None):
	if blocktype==None:
		blocktype = pieceval[0]
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			cur = index_piece(pieceval,ix,iy,blocktype)
			if cur != BACKGROUND_TILE:
				board[iy+y][ix+x] = cur
				paint_update_board[iy+y][ix+x] = cur

def clear_piece(pieceval,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			cur = index_piece(pieceval,ix,iy)
			if cur != BACKGROUND_TILE:
				board[iy+y][ix+x] = BACKGROUND_TILE
				paint_update_board[iy+y][ix+x] = BACKGROUND_TILE

def rows_to_clear():
	ret = []
	for y in range(len(board)):
		is_row_clearable = True
		for x in range(len(board[y])):
			if board[y][x]==BACKGROUND_TILE:
				is_row_clearable = False
				break
		if is_row_clearable:
			ret.append(y)
	return ret


def clear_rows():
	global board
	rows = rows_to_clear()
	if len(rows)==0:
		return 0
	newboard = []
	for y in range(len(board)):
		newrow = []
		dist = 0
		for i in rows:
			if i<=y+dist:
				dist+=1
		if y+dist >=len(board):
			for i in range(BOARD_WIDTH):
				newrow.append(BACKGROUND_TILE)
			newboard.append(newrow)
			continue
		for x in range(len(board[y+dist])):
			if board[y+dist][x]!=board[y][x]:
				paint_update_board[y][x] = board[y+dist][x]
			newrow.append(board[y+dist][x])
		newboard.append(newrow)
	board = newboard
	return len(rows)
			


	