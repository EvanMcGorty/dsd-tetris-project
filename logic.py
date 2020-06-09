from piece_operations import*
from random import choice, shuffle



FRAMES_PER_FALL = 360/GRAVITY

class Logic(GameState):

		
	def __init__(self):

		super().__init__()

		self.cur_piece = None
		self.cur_x,self.cur_y = (None,None)
		self.until_next_fall = None
		self.game_over = None
		self.lock_buffer = None
		self.ultimate_lock_buffer = None
		self.left_das_countdown = None
		self.right_das_countdown = None
		self.cur_move_offset = None
		self.last_move_direction = None
		self.randomizer_data = None
		self.last_shadow = None

		self.buttons = []
		self.buttons_release_wait = []

		for i in range(0,8):
			self.buttons.append(False)

		for i in range(0,8):
			self.buttons_release_wait.append(True)


		self.initialize_next_piece()
		
		

	def check_button_press(self,i):
		if self.buttons[i] and self.buttons_release_wait[i]:
			self.buttons_release_wait[i] = False
			return True
		return False




	def get_next_piece(self):

		if RANDOMIZER_MODE == "random":
			return construct_piece(choice(list(PIECE_INDEX.values())))

		elif RANDOMIZER_MODE == "classic":
			tryrandom = choice(list(PIECE_INDEX.values()))
			if tryrandom!=self.randomizer_data:
				self.randomizer_data = tryrandom
				return construct_piece(self.randomizer_data)
			else:
				self.randomizer_data = choice(list(PIECE_INDEX.values()))
				return construct_piece(self.randomizer_data)

		elif RANDOMIZER_MODE == "7bag":
			if self.randomizer_data == None or len(self.randomizer_data) == 0:
				self.randomizer_data=list(PIECE_INDEX.values())
				shuffle(self.randomizer_data)
			return construct_piece(self.randomizer_data.pop())
		
		elif RANDOMIZER_MODE == "14bag":
			if self.randomizer_data == None or len(self.randomizer_data) == 0:
				self.randomizer_data=list(PIECE_INDEX.values())+list(PIECE_INDEX.values())
				shuffle(self.randomizer_data)
			return construct_piece(self.randomizer_data.pop())




	def initialize_next_piece(self):
		self.cur_piece = self.get_next_piece()
		self.cur_x,self.cur_y = PIECE_SPAWN_COORDS[self.cur_piece[0]]
		self.until_next_fall = FRAMES_PER_FALL
		self.game_over = False
		self.lock_buffer = LOCK_DELAY
		self.ultimate_lock_buffer = LOCK_DELAY*ULTIMATE_LOCK_MULTIPLIER
		self.left_das_countdown = DAS
		self.right_das_countdown = DAS
		self.cur_move_offset = 0
		self.last_move_direction = 0
		if not self.can_place_piece(self.cur_piece,self.cur_x,self.cur_y):
			self.game_over = True




	def move(self,frame_dist,direction):
		self.cur_move_offset+=frame_dist*direction

		if not(frame_dist == 0 and ARR == 0):
			if self.cur_move_offset<0:
				direction = -1
			elif self.cur_move_offset >= 0:
				direction = 1

		self.last_move_direction = direction

		abs_distance = self.cur_move_offset*direction
		
		while abs_distance>=ARR:
			if self.can_place_piece(self.cur_piece,self.cur_x+direction,self.cur_y):
				self.cur_x+=direction
				abs_distance-=ARR
				self.cur_move_offset -= ARR*direction
				self.lock_buffer = LOCK_DELAY
			else:
				abs_distance = 0
				self.cur_move_offset = 0
			if frame_dist == 0 or abs_distance == 0:
				break

	def manage_lr_movement(self):
		if self.buttons[LEFT]:
			if self.left_das_countdown>0:
				self.left_das_countdown-=1
				if self.check_button_press(LEFT):
					self.cur_move_offset = 0
					self.move(ARR,-1)
			elif not(self.buttons[RIGHT] and self.last_move_direction==1):
				if self.left_das_countdown<0:
					self.move(1-self.left_das_countdown,-1)
					self.left_das_countdown = 0
				else:
					self.move(1,-1)
		else:
			self.left_das_countdown = DAS

		if self.buttons[RIGHT]:
			if self.right_das_countdown>0:
				self.right_das_countdown-=1
				if self.check_button_press(RIGHT):
					self.cur_move_offset = 0
					self.move(ARR,1)
			elif not(self.buttons[LEFT] and self.last_move_direction==-1):
				if self.right_das_countdown<0:
					self.move(1-self.right_das_countdown,1)
					self.right_das_countdown = 0
				else:
					self.move(1,1)
		else:
			self.right_das_countdown = DAS

	def shadow_on(self):
		if DISPLAY_SHADOW:
			y = 0
			while self.can_place_piece(self.cur_piece,self.cur_x,self.cur_y+y):
				y-=1
			y+=1
			self.place_piece(self.cur_piece,self.cur_x,self.cur_y+y,SHADOW_TILE)
			self.last_shadow = (self.cur_piece,self.cur_x,self.cur_y+y)
			

	def shadow_off(self):
		if self.last_shadow == None:
			return
		(p,x,y) = self.last_shadow
		self.clear_piece(p,x,y)
		self.last_shadow = None
		

	def check_spins(self):
		was_spin = True
		for (x,y) in [(1,0),(0,1),(-1,0),(0,-1)]:
			if self.can_place_piece(self.cur_piece,self.cur_x+x,self.cur_y+y):
				was_spin = False
		if was_spin:
			self.display_message(PIECE_INDEX_INVERSE[self.cur_piece[0]]+"-spin")


	def manage_clear_info(self,rowcount):
		if rowcount>0:
			all_clear = True
			for row in self.board:
				for x in row:
					if x!=BACKGROUND_TILE:
						all_clear = False
						break
				if not all_clear:
					break
			if all_clear:
				self.display_message("all clear")
			self.display_message({1:"single!",2:"double!",3:"triple!",4:"tetris!"}[rowcount])


	def finalize_placement(self):
		if self.lock_buffer<=0 or self.ultimate_lock_buffer<=0:
			self.check_spins()
			self.place_piece(self.cur_piece,self.cur_x,self.cur_y)
			self.manage_clear_info(self.clear_rows())
			self.initialize_next_piece()
		else:
			self.lock_buffer-=1
			self.ultimate_lock_buffer-=1
			self.until_next_fall = 1

	def try_dropping(self):

		if self.check_button_press(HARD):
			self.until_next_fall=-21*FRAMES_PER_FALL
			self.lock_buffer = 0
		elif self.buttons[SOFT]:
			self.until_next_fall-=SDF
		else:
			self.until_next_fall-=1


	def try_falling(self):

		while self.until_next_fall<=0:
			self.until_next_fall+=FRAMES_PER_FALL
			if self.can_place_piece(self.cur_piece,self.cur_x,self.cur_y-1):
				self.cur_y-=1
			else:
				self.finalize_placement()

	def try_rotate(self):
		for i in [ROT90,ROT270,ROT180]:
			if self.check_button_press(i):
				for kickind in range(KICK_ATTEMPT_COUNT):
					(x,y) = kick_table_index(self.cur_piece[1],i,KICK_LOOKUP[self.cur_piece[0]],kickind)
					rotated = rotate_piece(self.cur_piece,i)
					if self.can_place_piece(rotated,self.cur_x+x,self.cur_y+y):
						self.cur_piece = rotated
						self.cur_x+=x
						self.cur_y+=y
						self.lock_buffer = LOCK_DELAY
						break
				return



	def perform_frame_logic(self):

		if self.game_over:
			return

		self.clear_piece(self.cur_piece,self.cur_x,self.cur_y)
		self.shadow_off()

		self.manage_lr_movement()

		self.try_dropping()
		
		self.try_falling()

			
		self.increment_framecount()

		
		if self.game_over:
			self.place_piece(self.cur_piece,self.cur_x,self.cur_y)
			self.display_message("GAME OVER!")
			return

		self.try_rotate()

		self.shadow_on()
		self.place_piece(self.cur_piece,self.cur_x,self.cur_y)
