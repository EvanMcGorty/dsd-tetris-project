DISPLAY_SHADOW = True #Whether to display a shadow of where a piece would end up were it to be harddropped
TEXT_DISPLAY_DURATION = 90 #How many frames to display messages such as "tetris!" or "t spin"
COLORBLIND_MODE = False #Changes how block outlines are displayed to make tetris colorblind friendly
DARKMODE = COLORBLIND_MODE #Whether to invert light and dark colors
PIECE_SIZE = 40 #The Display size for pieces.
PIECE_DISPLAY_WIDTH = 4 #How many tiles wide a piece display is
PIECE_DISPLAY_HEIGHT = 2 #How many tiles tall a piece display is
MESSAGE_COLOR = "#78d"
TEXT_COLOR = "#000"
CLOCKCHECK_PERIOD = 12 #length in frames of the period over which fps will be stabilized.
LOG_TIME_OFFSET = False #Whether to log how far off in game time is from real time

SHADOW_TILE = -1 #Used in the color scheme
BACKGROUND_TILE = 0 #Used in the color scheme
PIECE_INDEX = {'z':1,'j':2,'i':3,'s':4,'l':5,'o':6,'t':7} #these numbers correspond to the colors below

COLOR_SCHEME = {
	{True:SHADOW_TILE,False:BACKGROUND_TILE}[DARKMODE]: "#feb", #light color
	{False:SHADOW_TILE,True:BACKGROUND_TILE}[DARKMODE]:"#333", #dark color
	1:"#e21", #red
	2:"#04c", #blue
	3:"#1ec", #light blue
	4:"#0b3", #green
	5:"#f60", #orange
	6:"#fc0", #yellow
	7:"#b2d"  #purple
}
