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

def make_matricies(strings,color):
	ret = []
	for i in strings:
		ret.append(make_matrix(i,color))
	return ret

rotations = {
	PIECE_INDEX['i']:make_matricies([
		"""
		oooo.
		xxxx.
		oooo.
		oooo.
		""",
		"""
		ooxo.
		ooxo.
		ooxo.
		ooxo.
		""",
		"""
		oooo.
		oooo.
		xxxx.
		oooo.
		""",
		"""
		oxoo.
		oxoo.
		oxoo.
		oxoo.
		"""],PIECE_INDEX['i']),
	PIECE_INDEX['j']:make_matricies([
		"""
		xoo.
		xxx.
		ooo.
		""",
		"""
		oxx.
		oxo.
		oxo.
		""",
		"""
		ooo.
		xxx.
		oox.
		""",
		"""
		oxo.
		oxo.
		xxo.
		"""
		],PIECE_INDEX['j']),
		PIECE_INDEX['l']:make_matricies([
		"""
		oox.
		xxx.
		ooo.
		""",
		"""
		oxo.
		oxo.
		oxx.
		""",
		"""
		ooo.
		xxx.
		xoo.
		""",
		"""
		xxo.
		oxo.
		oxo.
		"""
		],PIECE_INDEX['l']),
		PIECE_INDEX['o']:make_matricies([
		"""
		oxx.
		oxx.
		ooo.
		""",
		"""
		oxx.
		oxx.
		ooo.
		""",
		"""
		oxx.
		oxx.
		ooo.
		""",
		"""
		oxx.
		oxx.
		ooo.
		"""
		],PIECE_INDEX['o']),
		PIECE_INDEX['s']:make_matricies([
		"""
		oxx.
		xxo.
		ooo.
		""",
		"""
		oxo.
		oxx.
		oox.
		""",
		"""
		ooo.
		oxx.
		xxo.
		""",
		"""
		xoo.
		xxo.
		oxo.
		"""
		],PIECE_INDEX['s']),
		PIECE_INDEX['t']:make_matricies([
		"""
		oxo.
		xxx.
		ooo.
		""",
		"""
		oxo.
		oxx.
		oxo.
		""",
		"""
		ooo.
		xxx.
		oxo.
		""",
		"""
		oxo.
		xxo.
		oxo.
		""",
		],PIECE_INDEX['t']),
		PIECE_INDEX['z']:make_matricies([
		"""
		xxo.
		oxx.
		ooo.
		""",
		"""
		oox.
		oxx.
		oxo.
		""",
		"""
		ooo.
		xxo.
		oxx.
		""",
		"""
		oxo.
		xxo.
		xoo.
		"""
		],PIECE_INDEX['z'])
}
		