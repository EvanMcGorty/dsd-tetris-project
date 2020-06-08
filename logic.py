from piece_operations import*
from random import choice, shuffle

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


randomizer_data = None


def get_next_piece():
	global randomizer_data

	if RANDOMIZER_MODE == "random":
		return construct_piece(choice(list(PIECE_INDEX.values())))

	elif RANDOMIZER_MODE == "classic":
		tryrandom = choice(list(PIECE_INDEX.values()))
		if tryrandom!=randomizer_data:
			randomizer_data = tryrandom
			return construct_piece(randomizer_data)
		else:
			randomizer_data = choice(list(PIECE_INDEX.values()))
			return construct_piece(randomizer_data)

	elif RANDOMIZER_MODE == "7bag":
		if randomizer_data == None or len(randomizer_data) == 0:
			randomizer_data=list(PIECE_INDEX.values())
			shuffle(randomizer_data)
		return construct_piece(randomizer_data.pop())
	
	elif RANDOMIZER_MODE == "14bag":
		if randomizer_data == None or len(randomizer_data) == 0:
			randomizer_data=list(PIECE_INDEX.values())+list(PIECE_INDEX.values())
			shuffle(randomizer_data)
		return construct_piece(randomizer_data.pop())


FRAMES_PER_FALL = 360/GRAVITY


cur_piece = None
cur_x,cur_y = (None,None)
until_next_fall = None
game_over = None
lock_buffer = None
ultimate_lock_buffer = None
left_das_countdown = None
right_das_countdown = None
cur_move_offset = None
last_move_direction = None


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
	global last_move_direction
	global ultimate_lock_buffer
	cur_piece = get_next_piece()
	cur_x,cur_y = PIECE_SPAWN_COORDS[cur_piece[0]]
	until_next_fall = FRAMES_PER_FALL
	game_over = False
	lock_buffer = LOCK_DELAY
	ultimate_lock_buffer = LOCK_DELAY*ULTIMATE_LOCK_MULTIPLIER
	left_das_countdown = DAS
	right_das_countdown = DAS
	cur_move_offset = 0
	last_move_direction = 0
	if not can_place_piece(cur_piece,cur_x,cur_y):
		game_over = True
		display_message("GAME OVER!")

initialize_next_piece()



def move(frame_dist):
	global cur_piece
	global cur_x
	global cur_y
	global cur_move_offset
	global last_move_direction
	global lock_buffer
	cur_move_offset+=frame_dist
	direction = None

	if cur_move_offset<0:
		direction = -1
	elif cur_move_offset >= 0:
		direction = 1

	last_move_direction = direction

	abs_distance = cur_move_offset*direction
	
	while abs_distance>=ARR:
		if can_place_piece(cur_piece,cur_x+direction,cur_y):
			cur_x+=direction
			abs_distance-=ARR
			cur_move_offset -= ARR*direction
			lock_buffer = LOCK_DELAY
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
		elif not(buttons[RIGHT] and last_move_direction==1):
			move(-1)
	else:
		left_das_countdown = DAS

	if buttons[RIGHT]:
		if right_das_countdown>0:
			right_das_countdown-=1
			if check_button_press(RIGHT):
				cur_move_offset = 0
				move(SDF)
		elif not(buttons[LEFT] and last_move_direction==-1):
			move(1)
	else:
		right_das_countdown = DAS

last_shadow = None

def shadow_on():
	global last_shadow
	if DISPLAY_SHADOW:
		y = 0
		while can_place_piece(cur_piece,cur_x,cur_y+y):
			y-=1
		y+=1
		place_piece(cur_piece,cur_x,cur_y+y,SHADOW_TILE)
		last_shadow = (cur_piece,cur_x,cur_y+y)
		

def shadow_off():
	global last_shadow
	if last_shadow == None:
		return
	(p,x,y) = last_shadow
	clear_piece(p,x,y)
	last_shadow = None
	

def check_spins():
	was_spin = True
	for (x,y) in [(1,0),(0,1),(-1,0),(0,-1)]:
		if can_place_piece(cur_piece,cur_x+x,cur_y+y):
			was_spin = False
	if was_spin:
		display_message(PIECE_INDEX_INVERSE[cur_piece[0]]+"-spin")


def manage_clear_info(rowcount):
	if rowcount>0:
		all_clear = True
		for row in board:
			for x in row:
				if x!=BACKGROUND_TILE:
					all_clear = False
					break
			if not all_clear:
				break
		if all_clear:
			display_message("all clear")
		display_message({1:"single!",2:"double!",3:"triple!",4:"tetris!"}[rowcount])


def finalize_placement():
	global lock_buffer
	global ultimate_lock_buffer
	global until_next_fall
	if lock_buffer<=0 or ultimate_lock_buffer<=0:
		check_spins()
		place_piece(cur_piece,cur_x,cur_y)
		manage_clear_info(clear_rows())
		initialize_next_piece()
	else:
		lock_buffer-=1
		ultimate_lock_buffer-=1
		until_next_fall = 1

def try_dropping():
	global until_next_fall
	global lock_buffer

	if check_button_press(HARD):
		until_next_fall=-21*FRAMES_PER_FALL
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
		until_next_fall+=FRAMES_PER_FALL
		if can_place_piece(cur_piece,cur_x,cur_y-1):
			cur_y-=1
		else:
			finalize_placement()

def try_rotate():
	global cur_x
	global cur_y
	global cur_piece
	global lock_buffer
	for i in [ROT90,ROT270,ROT180]:
		if check_button_press(i):
			for kickind in range(KICK_ATTEMPT_COUNT):
				(x,y) = kick_table_index(cur_piece[1],i,KICK_LOOKUP[cur_piece[0]],kickind)
				rotated = rotate_piece(cur_piece,i)
				if can_place_piece(rotated,cur_x+x,cur_y+y):
					cur_piece = rotated
					cur_x+=x
					cur_y+=y
					lock_buffer = LOCK_DELAY
					break
			return



def perform_frame_logic():
	global cur_x
	global cur_y

	if game_over:
		return

	clear_piece(cur_piece,cur_x,cur_y)
	shadow_off()

	manage_lr_movement()

	try_dropping()
	
	try_falling()

	try_rotate()

	shadow_on()
	place_piece(cur_piece,cur_x,cur_y)

		
	increment_framecount()