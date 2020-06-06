def make_board_matrix(initval):
	board = []
	for y in range(0,20):
		nextrow = []
		for x in range(0,10):
			nextrow.append(initval)
		board.append(nextrow)
	return board

PIECE_INDEX = {'z':1,'j':2,'i':3,'s':4,'l':5,'o':6,'t':7}


PAINT_NOTHING = -1

BACKGROUND_TILE = 0

paint_update_board = make_board_matrix(BACKGROUND_TILE)


buttons = []
for i in range(0,8):
	buttons.append(False)

(ROT90,ROT270,ROT180,RIGHT,LEFT,SOFT,HARD,HOLD) = [0,1,2,3,4,5,6,7]
KEYS = ['Up','z','a','Right','Left','Down','space','c']


framecount = 0



