from piece_operations import*
import random
import math



class GameLogic(GameState):

		
	def __init__(self,rng,keybinds,linegoal,timegoal):

		super().__init__()
		self.level = 1
		self.linecount = 0
		self.score = 0
		self.curframescore = 0
		self.linegoal = linegoal
		self.timegoal = timegoal
		self.rng = rng
		self.keybinds = keybinds
		self.game_finished = False
		self.left_das_countdown = DAS
		self.right_das_countdown = DAS
		self.is_hold_depleted = False
		self.whether_perform_hold = False
		self.cur_piece = None
		self.cur_x,self.cur_y = (None,None)
		self.until_next_fall = None
		self.lock_buffer = None
		self.ultimate_lock_buffer = None
		self.cur_move_offset = None
		self.last_move_direction = None
		self.randomizer_data = None
		self.last_shadow = None
		self.hold_piece = None
		self.next_pieces_buffer = []

		self.buttons = []
		self.buttons_release_wait = []

		for i in range(0,8):
			self.buttons.append(False)

		for i in range(0,8):
			self.buttons_release_wait.append(True)


		self.initialize_next_piece()
		
		self.combo_streak = 0
		self.b2b_streak = 0

	def win_game(self):
		self.game_finished = True
		self.display_message("Game!")

	def frames_per_fall(self):
		return 360/(GRAVITY+self.framecount/60*GRAVITY_INCREASE_PER_SECOND+(self.level-1)*GRAVITY_INCREASE_PER_LEVEL)

	def check_button_press(self,i):
		if self.buttons[i] and self.buttons_release_wait[i]:
			self.buttons_release_wait[i] = False
			return True
		return False




	def generate_next_piece(self):

		if RANDOMIZER_MODE == "random":
			return construct_piece(self.rng.choice(list(PIECE_INDEX.values())))

		elif RANDOMIZER_MODE == "classic":
			tryrandom = self.rng.choice(list(PIECE_INDEX.values()))
			if tryrandom!=self.randomizer_data:
				self.randomizer_data = tryrandom
				return construct_piece(self.randomizer_data)
			else:
				self.randomizer_data = self.rng.choice(list(PIECE_INDEX.values()))
				return construct_piece(self.randomizer_data)

		elif RANDOMIZER_MODE == "7bag":
			if self.randomizer_data == None or len(self.randomizer_data) == 0:
				self.randomizer_data=list(PIECE_INDEX.values())
				self.rng.shuffle(self.randomizer_data)
			return construct_piece(self.randomizer_data.pop())
		
		elif RANDOMIZER_MODE == "14bag":
			if self.randomizer_data == None or len(self.randomizer_data) == 0:
				self.randomizer_data=list(PIECE_INDEX.values())+list(PIECE_INDEX.values())
				self.rng.shuffle(self.randomizer_data)
			return construct_piece(self.randomizer_data.pop())


	def get_next_piece(self):
		while len(self.next_pieces_buffer)<=NEXT_PIECES:
			self.next_pieces_buffer.insert(0,self.generate_next_piece())
		ret = self.next_pieces_buffer.pop()
		for i in range(len(self.next_pieces_display)):
			update_piece_display(PIECE_MATRICIES[self.next_pieces_buffer[i][0]],self.next_pieces_buffer[i][0],self.next_pieces_display[i])
		return ret

	def initialize_next_piece(self):
		if self.whether_perform_hold == True:
			self.is_hold_depleted = True
			if self.hold_piece == None:
				self.hold_piece = self.cur_piece[0]
				self.cur_piece = self.get_next_piece()
			else:
				self.cur_piece,self.hold_piece = construct_piece(self.hold_piece),self.cur_piece[0]
			self.whether_perform_hold = False
			update_piece_display(PIECE_MATRICIES[self.hold_piece],SHADOW_TILE,self.hold_display)
		else:
			if self.is_hold_depleted:
				self.is_hold_depleted = False
				update_piece_display(PIECE_MATRICIES[self.hold_piece],self.hold_piece,self.hold_display)
			self.cur_piece = self.get_next_piece()
			
		self.score+=self.curframescore*self.level
		self.curframescore = 0
		while self.level*(self.level+1) < self.linecount:
			self.level+=1
		self.cur_x = BOARD_WIDTH//2-2+BOARD_WIDTH%2
		self.cur_y = BOARD_HEIGHT-3
		self.until_next_fall = self.frames_per_fall()
		self.lock_buffer = LOCK_DELAY
		self.ultimate_lock_buffer = LOCK_DELAY*ULTIMATE_LOCK_MULTIPLIER
		self.cur_move_offset = 0
		self.last_move_direction = 0
		if not self.can_place_piece(self.cur_piece,self.cur_x,self.cur_y):
			self.display_message("Game Over!")
			self.game_finished = True




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
		ret = True
		for (x,y) in [(1,0),(0,1),(-1,0),(0,-1)]:
			if self.can_place_piece(self.cur_piece,self.cur_x+x,self.cur_y+y):
				ret = False
		return ret

	def regspin(self):
		self.display_message(PIECE_INDEX_INVERSE[self.cur_piece[0]]+"-spin")
		self.score+=200

	def regallclear(self):
		self.display_message("all clear")
		self.score+=4000

	def regcombo(self):
		self.display_message("Combo x"+str(self.combo_streak))
		self.score+=(int(math.sqrt(2*(self.combo_streak-1))))*100

	def regb2b(self):
		self.display_message("B2B x"+str(self.b2b_streak))
		self.score+=(int(math.sqrt(2*(self.b2b_streak+2))))*200

	def regclear(self,rowcount,was_spin):
		self.linecount+=rowcount
		self.display_message({1:"single!",2:"double!",3:"triple!",4:"tetris!"}[rowcount])
		self.score+=2**rowcount*{False:100,True:300}[was_spin and self.cur_piece[0] == PIECE_INDEX['t']]
		if self.linegoal!=None and self.linecount>=self.linegoal:
			self.win_game()

	def manage_clear_info(self,rowcount,was_spin):

		if was_spin:
			self.regspin()	

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
				self.regallclear()
			
			self.combo_streak+=1
			if self.combo_streak>=2:
				self.regcombo()

			if rowcount==4 or (was_spin and self.cur_piece[0] == PIECE_INDEX['t']):
				self.b2b_streak+=1
				if self.b2b_streak>=2:
					self.regb2b()
			else:
				self.b2b_streak=0
			
			self.regclear(rowcount,was_spin)
		else:
			self.combo_streak=0

	def finalize_placement(self):
		if self.lock_buffer<=0 or self.ultimate_lock_buffer<=0:
			was_spin = self.check_spins()
			self.place_piece(self.cur_piece,self.cur_x,self.cur_y)
			self.manage_clear_info(self.clear_rows(),was_spin)
			self.initialize_next_piece()
		else:
			self.lock_buffer-=1
			self.ultimate_lock_buffer-=1
			self.until_next_fall = 1

	def try_dropping(self):

		if self.check_button_press(HARD):
			self.until_next_fall=-1*BOARD_HEIGHT*self.frames_per_fall()
			self.lock_buffer = 0
		elif self.buttons[SOFT]:
			self.until_next_fall-=SDF
		else:
			self.until_next_fall-=1


	def try_falling(self):
		while self.until_next_fall<=0:
			self.until_next_fall+=self.frames_per_fall()
			if self.can_place_piece(self.cur_piece,self.cur_x,self.cur_y-1):
				self.cur_y-=1
			else:
				self.finalize_placement()
	
	def try_hold(self):
		if self.is_hold_depleted or not self.check_button_press(HOLD):
			return
		else:
			self.whether_perform_hold = True
			self.initialize_next_piece()




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

		if self.game_finished:
			return

		self.clear_piece(self.cur_piece,self.cur_x,self.cur_y)
		self.shadow_off()

		self.manage_lr_movement()

		self.try_dropping()
		
		self.try_falling()

			
		self.framecount+=1

		if self.timegoal!=None and self.framecount>=int(self.timegoal):
			self.win_game()
		
		if self.game_finished:
			self.place_piece(self.cur_piece,self.cur_x,self.cur_y)
			return

		if PIECE_HOLDS:
			self.try_hold()

		self.try_rotate()

		self.shadow_on()
		self.place_piece(self.cur_piece,self.cur_x,self.cur_y)


	def get_info_string(self):
		ret = ""
		ret+="Time: "
		if self.framecount>=60*60:
			ret+=str(self.framecount//(60*60)) + ":"
		if self.framecount%(60*60)/60<10:
			ret+="0"
		ret+=str(int((self.framecount%(60*60))/6)/10) + "\n"
		ret+="Lines: " + str(self.linecount) + "\n"
		ret+="Score: " + str(self.score) + "\n"
		ret+="Level " + str(self.level)
		
		return ret