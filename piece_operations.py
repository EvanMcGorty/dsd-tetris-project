from piece_data import*
from random import choice



def construct_piece(ind):
	return (ind,0)

def rotate_piece(pieceval,rot):
	turn_count = {ROT90:1,ROT180:2,ROT270:3}[rot]
	return (pieceval[0],(pieceval[1]+turn_count)%4)

def index_piece(pieceval,x,y):
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
	return matrix[newy][newx]
		


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
	
def place_piece(pieceval,x,y):
	for ix in range(MATRIX_SIZE[pieceval[0]]):
		for iy in range(MATRIX_SIZE[pieceval[0]]):
			cur = index_piece(pieceval,ix,iy)
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
	