from piece_data import*
from random import choice


paint_update_board = make_board_matrix(BACKGROUND_TILE)


buttons = []
for i in range(0,8):
	buttons.append(False)



framecount = 0

def debug_display_keys():
	curpressed = ""
	for i in range(0,len(buttons)):
		if buttons[i]:
			curpressed+=KEYS[i]+" "
	print(curpressed)
def debug_paint_test():
	global framecount
	global paint_update_board
	paint_update_board[framecount%19][framecount%10] = framecount%8


main_board = make_board_matrix(BACKGROUND_TILE)


def is_occupiable(board,x,y):
	if len(board)<=y:
		return False
	if len(board[y])<=x:
		return False
	if board[y][x] != BACKGROUND_TILE:
		return False
	return True

def can_place_piece(pieceval,board,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			if index_piece(pieceval,ix,iy) != BACKGROUND_TILE:
				if not is_occupiable(board,ix+x,iy+y):
					return False
	return True
	
def place_piece(pieceval,board,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			cur = index_piece(pieceval,ix,iy)
			if cur != BACKGROUND_TILE:
				board[iy+y][ix+x] = cur
				paint_update_board[iy+y][ix+x] = cur

def clear_piece(pieceval,board,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			cur = index_piece(pieceval,ix,iy)
			if cur != BACKGROUND_TILE:
				board[iy+y][ix+x] = BACKGROUND_TILE
				paint_update_board[iy+y][ix+x] = BACKGROUND_TILE
	
	

def get_next_piece():
	return construct_piece(choice(PIECE_INDEX.values()))

def perform_frame_logic():
	global framecount
	global paint_update_board
	debug_paint_test()
	debug_display_keys()
	
	framecount+=1