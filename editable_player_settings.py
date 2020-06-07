ARR = 3 #Auto Repeat Rate: How many frames it takes for a piece to move while auto shifting
DAS = 8 #Delayed Auto Shift: How many frames a direction must be held to begin auto shifting
SDF = 5 #Soft Drop Multiplier: Fall speed mulitplier when soft dropping
GRAVITY = 24 #Base fall speed, 360/gravity is the number of frames it takes to fall once
LOCK_DELAY = 30 #The number of extra frames a piece touching the floor has before locking, resets when it is moved
ULTIMATE_LOCK_MULTIPLIER = 10 #Multiplier for the amount of lock delay that doesnt reset when the piece is moved
DISABLE_KICKS = False #Whether to disable kicks that try allow a piece to spin when there isnt room by shifting it
COLORBLIND_MODE = False #Changes how block outlines are displayed to make tetris colorblind friendly