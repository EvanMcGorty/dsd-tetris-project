from piece_data import*



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


board = make_board_matrix(BACKGROUND_TILE)

def perform_frame_logic():
	global framecount
	global paint_update_board

	
	framecount+=1