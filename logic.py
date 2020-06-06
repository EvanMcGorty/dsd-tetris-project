from piece_operations import*
from player_settings import*

buttons = []
for i in range(0,8):
	buttons.append(False)

framecount = 0

	
def get_next_piece():
	return construct_piece(choice(list(PIECE_INDEX.values())))

cur_piece = None
cur_coords = None

def initialize_next_piece():
	global cur_piece
	global cur_coords
	cur_piece = get_next_piece()
	cur_coords = PIECE_SPAWN_COORDS[cur_piece[0]]

initialize_next_piece()

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

def perform_frame_logic():
	global framecount
	global paint_update_board
	#debug_paint_test()
	#debug_display_keys()
	
	framecount+=1