ARR = 2 #Auto Repeat Rate: How many frames it takes for a piece to move while auto shifting
DAS = 7 #Delayed Auto Shift: How many frames a direction must be held to begin auto shifting
SDF = 5 #Soft Drop Multiplier: Fall speed mulitplier when soft dropping
GRAVITY = 24 #Base fall speed, 360/gravity is the number of frames it takes to fall once
LOCK_DELAY = 30 #The number of extra frames a piece touching the floor has before locking, resets when it is moved
ULTIMATE_LOCK_MULTIPLIER = 10 #Multiplier for the amount of lock delay that doesnt reset when the piece is moved
DISABLE_KICKS = False #Whether to disable kicks that try allow a piece to spin when there isnt room by shifting it
RANDOMIZER_MODE = "7bag" #Random piece generator options: "random", "classic", "7bag", "14bag"
DISPLAY_SHADOW = True #Whether to display a shadow of where a piece would end up were it to be harddropped
TEXT_DISPLAY_DURATION = 90 #How many frames to display messages such as "tetris!" or "t spin"
COLORBLIND_MODE = False #Changes how block outlines are displayed to make tetris colorblind friendly
BOARD_WIDTH = 10 #How many tiles are across the board. Would you really try changing this?
BOARD_HEIGHT = 20 #How many tiles tall the board is. I suppose this could be a fun challenge?
PIECE_SIZE = 40 #The Display size for pieces.

