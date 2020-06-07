from piece_operations import*
from player_settings import*

buttons = []
for i in range(0,8):
	buttons.append(False)

buttons_release_wait = []
for i in range(0,8):
	buttons_release_wait.append(True)

def check_button_press(i):
	if buttons[i] and buttons_release_wait[i]:
		buttons_release_wait[i] = False
		return True
	return False


framecount = 0

	
def get_next_piece():
	return construct_piece(choice(list(PIECE_INDEX.values())))

cur_piece = None
cur_x,cur_y = (None,None)
until_next_fall = None
game_over = None
lock_buffer = None
left_das_countdown = None
right_das_countdown = None
cur_move_offset = None

def initialize_next_piece():
	global cur_piece
	global cur_x
	global cur_y
	global until_next_fall
	global game_over
	global lock_buffer
	global left_das_countdown
	global right_das_countdown
	global cur_move_offset
	cur_piece = get_next_piece()
	cur_x,cur_y = PIECE_SPAWN_COORDS[cur_piece[0]]
	until_next_fall = GRAVITY
	game_over = False
	lock_buffer = LOCK_DELAY
	left_das_countdown = DAS
	right_das_countdown = DAS
	cur_move_offset = 0
	if not can_place_piece(cur_piece,cur_x,cur_y):
		game_over = True

initialize_next_piece()



def move(frame_dist):
	global cur_piece
	global cur_x
	global cur_y
	global cur_move_offset
	cur_move_offset+=frame_dist
	direction = None

	if cur_move_offset<0:
		direction = -1
	elif cur_move_offset >= 0:
		direction = 1

	abs_distance = cur_move_offset*direction
	
	while abs_distance>=ARR:
		if can_place_piece(cur_piece,cur_x+direction,cur_y):
			cur_x+=direction
			abs_distance-=ARR
			cur_move_offset -= ARR*direction
		else:
			abs_distance = 0
			cur_move_offset = 0

def manage_lr_movement():
	global cur_move_offset
	global left_das_countdown
	global right_das_countdown
	if buttons[LEFT]:
		if left_das_countdown>0:
			left_das_countdown-=1
			if check_button_press(LEFT):
				cur_move_offset = 0
				move(-SDF)
		else:
			move(-1)

	if buttons[RIGHT]:
		if right_das_countdown>0:
			right_das_countdown-=1
			if check_button_press(RIGHT):
				cur_move_offset = 0
				move(SDF)
		else:
			move(1)


def finalize_placement():
	global lock_buffer
	global until_next_fall
	if lock_buffer==0:
		place_piece(cur_piece,cur_x,cur_y)
		initialize_next_piece()
	else:
		lock_buffer-=1
		until_next_fall = 1

def try_dropping():
	global until_next_fall
	global lock_buffer

	if check_button_press(HARD):
		until_next_fall=-21*GRAVITY
		lock_buffer = 0
	elif buttons[SOFT]:
		until_next_fall-=SDF
	else:
		until_next_fall-=1


def try_falling():
	global until_next_fall
	global cur_x
	global cur_y

	while until_next_fall<=0:
		until_next_fall+=GRAVITY
		if can_place_piece(cur_piece,cur_x,cur_y-1):
			cur_y-=1
		else:
			finalize_placement()

def try_rotate():
	global cur_x
	global cur_y
	global cur_piece
	for i in [ROT90,ROT270,ROT180]:
		if check_button_press(i):
			if can_place_piece(rotate_piece(cur_piece,i),cur_x,cur_y):
				cur_piece = rotate_piece(cur_piece,i)
				break



def perform_frame_logic():
	global framecount
	global cur_x
	global cur_y

	if game_over:
		return

	clear_piece(cur_piece,cur_x,cur_y)

	manage_lr_movement()

	try_dropping()
	
	try_falling()

	try_rotate()

	place_piece(cur_piece,cur_x,cur_y)

		
	framecount+=1