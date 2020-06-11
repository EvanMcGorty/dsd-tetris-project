from editable_player_settings import*
from editable_visual_settings import*

PIECE_INDEX_INVERSE = {v: k for k, v in PIECE_INDEX.items()}

PAINT_NOTHING = -2

(ROT90,ROT270,ROT180,RIGHT,LEFT,SOFT,HARD,HOLD) = [0,1,2,3,4,5,6,7]


def make_board_matrix(initval,width,height):
	board = []
	for y in range(0,height):
		nextrow = []
		for x in range(0,width):
			nextrow.append(initval)
		board.append(nextrow)
	return board


def make_matrix(string):
	ret = []
	currow = []
	for i in string:
		if i=='o':
			currow.append(False)
		elif i=='x':
			currow.append(True)
		else:
			ret.insert(0,currow)
			currow = []
	return ret


PIECE_MATRICIES = {
PIECE_INDEX['i']:make_matrix(
"""\
oooo
xxxx
oooo
oooo
"""),
	PIECE_INDEX['j']:make_matrix(
"""\
xoo
xxx
ooo
"""),
PIECE_INDEX['l']:make_matrix(
"""\
oox
xxx
ooo
"""),
PIECE_INDEX['o']:make_matrix(
"""\
oooo
oxxo
oxxo
oooo
"""),
PIECE_INDEX['s']:make_matrix(
"""\
oxx
xxo
ooo
"""),
PIECE_INDEX['t']:make_matrix(
"""\
oxo
xxx
ooo
"""),
PIECE_INDEX['z']:make_matrix(
"""\
xxo
oxx
ooo
""")
}

JLSTZ_KICKS = [
	[(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)],
	[(0,0),(1,0),(1,-1),(0,2),(1,2)],
	[(0,0),(1,0),(1,1),(0,-2),(1,-2)],
	[(0,0),(-1,0),(-1,-1),(0,2),(-1,2)]
]

I_KICKS = [
	[( 0, 0),(-2, 0),(1, 0),(-2,-1),(1,2)],
	[( 0, 0),(-1, 0),(2, 0),(-1,2),(2,-1)],
	[( 0, 0),(2, 0),(-1, 0),(2,1),(-1,-2)],
	[( 0, 0),(1, 0),(-2, 0),(1,-2),(-2,1)]
]

O_KICKS = [
	[(0,0),(0,0),(0,0),(0,0),(0,0),],
	[(0,0),(0,0),(0,0),(0,0),(0,0),],
	[(0,0),(0,0),(0,0),(0,0),(0,0),],
	[(0,0),(0,0),(0,0),(0,0),(0,0),]
]

KICK_ATTEMPT_COUNT = 5
if DISABLE_KICKS:
	KICK_ATTEMPT_COUNT = 1

KICK_LOOKUP = {
	PIECE_INDEX['i']:I_KICKS,
	PIECE_INDEX['j']:JLSTZ_KICKS,
	PIECE_INDEX['l']:JLSTZ_KICKS,
	PIECE_INDEX['o']:O_KICKS,
	PIECE_INDEX['s']:JLSTZ_KICKS,
	PIECE_INDEX['t']:JLSTZ_KICKS,
	PIECE_INDEX['z']:JLSTZ_KICKS
}


MATRIX_SIZE = {
	PIECE_INDEX['i']:4,
	PIECE_INDEX['j']:3,
	PIECE_INDEX['l']:3,
	PIECE_INDEX['o']:4,
	PIECE_INDEX['s']:3,
	PIECE_INDEX['t']:3,
	PIECE_INDEX['z']:3
}
