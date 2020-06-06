from constants import*

def make_board_matrix(initval):
	board = []
	for y in range(0,20):
		nextrow = []
		for x in range(0,10):
			nextrow.append(initval)
		board.append(nextrow)
	return board



paint_update_board = make_board_matrix(BACKGROUND_TILE)


buttons = []
for i in range(0,8):
	buttons.append(False)



framecount = 0



