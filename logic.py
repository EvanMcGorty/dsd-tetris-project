from piece_operations import*
from player_settings import*

buttons = []
for i in range(0,8):
	buttons.append(False)

buttons_release_wait = []
for i in range(0,8):
	buttons_release_wait.append(True)

framecount = 0

	
def get_next_piece():
	return construct_piece(choice(list(PIECE_INDEX.values())))

cur_piece = None
cur_x,cur_y = (None,None)
until_next_fall = None
game_over = False

def initialize_next_piece():
	global cur_piece
	global cur_x
	global cur_y
	global until_next_fall
	global game_over
	cur_piece = get_next_piece()
	cur_x,cur_y = PIECE_SPAWN_COORDS[cur_piece[0]]
	until_next_fall = GRAVITY
	if not can_place_piece(cur_piece,cur_x,cur_y):
		game_over = True

initialize_next_piece()

def finalize_placement():
		place_piece(cur_piece,cur_x,cur_y)
		initialize_next_piece()


'''
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
'''

def perform_frame_logic():
	if game_over:
		return
	global framecount
	global paint_update_board
	global until_next_fall
	global cur_x
	global cur_y
	clear_piece(cur_piece,cur_x,cur_y)

	if buttons[HARD] and buttons_release_wait[HARD]:
		buttons_release_wait[HARD] = False
		until_next_fall=-21*GRAVITY
	elif buttons[SOFT]:
		until_next_fall-=SDF
	else:
		until_next_fall-=1

	
	while until_next_fall<=0:
		until_next_fall+=GRAVITY
		if can_place_piece(cur_piece,cur_x,cur_y-1):
			cur_y-=1
		else:
			finalize_placement()

	place_piece(cur_piece,cur_x,cur_y)

		
	framecount+=1