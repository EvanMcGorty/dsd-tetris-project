PIECE_INDEX = {'z':1,'j':2,'i':3,'s':4,'l':5,'o':6,'t':7}

PAINT_NOTHING = -1

BACKGROUND_TILE = 0

(ROT90,ROT270,ROT180,RIGHT,LEFT,SOFT,HARD,HOLD) = [0,1,2,3,4,5,6,7]
KEYS = ['Up','z','a','Right','Left','Down','space','c']


def make_board_matrix(initval):
	board = []
	for y in range(0,20):
		nextrow = []
		for x in range(0,10):
			nextrow.append(initval)
		board.append(nextrow)
	return board


def make_matrix(string,color):
	ret = []
	currow = []
	for i in string:
		if i=='o':
			currow.append(BACKGROUND_TILE)
		elif i=='x':
			currow.append(color)
		else:
			ret.insert(0,currow)
			currow = []
	return ret


pieces = {
PIECE_INDEX['i']:make_matrix(
"""oooo
xxxx
oooo
oooo
""",PIECE_INDEX['i']),
	PIECE_INDEX['j']:make_matrix(
"""xoo
xxx
ooo
""",PIECE_INDEX['j']),
PIECE_INDEX['l']:make_matrix(
		"""oox
xxx
ooo
""",PIECE_INDEX['l']),
PIECE_INDEX['o']:make_matrix(
"""xx
xx
""",PIECE_INDEX['o']),
PIECE_INDEX['s']:make_matrix(
"""oxx
xxo
ooo
""",PIECE_INDEX['s']),
PIECE_INDEX['t']:make_matrix(
"""oxo
xxx
ooo
""",PIECE_INDEX['t']),
PIECE_INDEX['z']:make_matrix(
"""xxo
oxx
ooo
""",PIECE_INDEX['z'])
}
