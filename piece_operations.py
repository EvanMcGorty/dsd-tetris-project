from piece_data import*
from random import choice


board = make_board_matrix(BACKGROUND_TILE)

paint_update_board = make_board_matrix(BACKGROUND_TILE)


def is_occupiable(x,y):
	if len(board)<=y:
		return False
	if len(board[y])<=x:
		return False
	if board[y][x] != BACKGROUND_TILE:
		return False
	return True

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
	